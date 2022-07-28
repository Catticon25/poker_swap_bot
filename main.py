""" main.py
Discord bot to play poker swap
"""
import discord
import asyncio
import datetime
import os
import traceback
from messages import *
from constants import *
from game import Game
from logs import logger
#from dotenv import load_dotenv

#load_dotenv()
client = discord.Client()
games={}


async def start_delay_msg(message):
   """Executed when $start command is run, but not all players are 'ready'"""
   logger.info("Start delay message")
   await asyncio.sleep(START_DELAY*60)
   game=games[message.channel.id]
   if not game.has_started:
      game.has_started=True
      game.index=0
      game.winner=None
      await message.channel.send(START_MSG)


async def start_force_play_timeout(message):
   """Executed when $cards command is run, it forces a winner after some time has passed"""
   logger.info("Start force play timeout")
   await asyncio.sleep(FORCE_PLAY_DELAY*60)
   game=games[message.channel.id]
   if game.winner is None:
      # Check if players have folded
      active_players=[player for player in game.players if player.active]
      playing_players=[player for player in active_players if not player.is_fold]
      if len(playing_players)==1 or len(active_players)==1:
         winner_name=game.set_winner_by_fold_default()
         await message.channel.send(FOLD_DEFAULT_WINNER.format(winner_name), reference=message)
      elif len(playing_players)==1 or len(active_players)==0:
         for player in game.players:
            player.restart_hand()
         await message.channel.send(FOLD_NO_WINNER, reference=message)
      else:
         win_message=game.find_winner()
         await message.channel.send(win_message)



@client.event
async def on_ready():
    """on_ready discord event"""
    logger.info('We have logged in as {0.user}'.format(client))
    

@client.event
async def on_message(message):
   """on_message discord event. Parses discord's commands"""
   try:
      if not hasattr(message, "author"):
         return
      elif message.author == client.user:
         return

      # Create game
      if message.channel.id not in games:
         games[message.channel.id]=Game()

      players_name=message.author.name
      game=games[message.channel.id]
      ##### START #####
      if message.content.startswith('$start'):
         await game.start(message, client, start_delay_msg, 
            start_force_play_timeout)
      ##### LOAD #####
      elif message.content.startswith('$load'):
         await game.load(message, players_name)
      ##### HELP ATTRIBUTES #####
      elif message.content.startswith('$help_attributes'):
         await message.channel.send(HELP_ATTRIBUTES_MSG)
      ##### HELP #####
      elif message.content.startswith('$help'):
         await message.channel.send(HELP_MSG_PART_1)
         await message.channel.send(HELP_MSG_PART_2.format(str(BODY_TRAITS),str(MENTAL_TRAITS)))
      ##### SEE ALL PLAYERS #####
      elif message.content.startswith('$all_players'):
         await game.all_players(message)
      ##### PLAYER #####
      elif message.content.startswith('$player'):
         await game.player(message, players_name)
      ##### READY #####
      elif message.content.startswith('$ready'):
         await game.ready(message, players_name)
      ##### RESTART #####
      elif message.content.startswith('$restart'):
         await game.restart(message, players_name)
      ##### FOLD #####
      elif message.content.startswith('$fold'):
         await game.fold(message, players_name)
      ##### CARDS #####
      elif message.content.startswith('$cards'):
         await game.cards(message, players_name, client, start_force_play_timeout)
      ##### SWAP #####
      elif message.content.startswith('$swap'):
         await game.swap(message,players_name)
      ##### ROYAL SWAP #####
      elif message.content.startswith('$royal_swap'):
         await game.royal_swap(message,players_name)
      elif message.content.startswith('$describe'):
         await game.describe(message, players_name)
      ##### LOOK #####
      elif message.content.startswith('$look'):
         await game.look(message, players_name)
      ##### CHANGE ORDER #####
      elif message.content.startswith('$change_order'):
         await game.change_order(message, players_name)

   except Exception as error:
      print("Program failed with error: "+str(error))
      print(traceback.format_exc())
        
        
def main():
   """main"""
   token=os.getenv('DISC_TOKEN')   # Put token here
   client.run(token)

if __name__ == "__main__":
    main()