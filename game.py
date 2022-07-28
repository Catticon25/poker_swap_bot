""" game.py
Class game that containts all functions related to poker and discord commands
#TODO: Leave the poker related commands in this class, move the discord commands
somewhere else
"""

import itertools
import random
import pickle
import datetime
import numpy as np
from collections import Counter
from messages import *
from constants import *
from traits import *
from player import *
from logs import logger

START_DELAY_MSG=START_DELAY_MSG.format(START_DELAY)

class Game:
    """Contains all functions and variables related to poker and discord commands"""
    def __init__(self):
      self.players=[]
      self.has_started=False
      self.index=0
      self.deck = list(itertools.product(range(2,15),['♠ (S)','♥ (H)','♦ (D)','♣ (C)']))
      self.winner=None
      self.task_delay=None
      self.task_st_force=None
      self.restart_hands()


    def restart_game(self):
      self.restart_hands()
      self.players=[]
      self.has_started=False
      self.task_delay=None
      self.task_st_force=None

      
    def draw_cards(self):
      content='__**Cards:**__'
      cards=[]
      # Draw cards
      for _ in range(5):
          card=self.deck[self.index]
          cards.append(card)
          str_number=self.get_card_number(card[0])
          content+='\r\n'+str_number+' '+card[1]
          self.index+=1
      return cards, content


    def check_poker_hand(self, cards):
      card_numbers=[card[0] for card in cards]
      card_numbers.sort()
      card_counter_vals=Counter(card_numbers).values()
      card_suits=[card[1] for card in cards]
      if((set(card_numbers)=={10,11,12,13,14}) and (len(set(card_suits))==1)):
         return 'Royal Flush',1,[max(card_numbers)]
      elif((list(np.diff(card_numbers))==[1,1,1,1] or set(card_numbers)=={2,3,4,5,14}) 
                                                and (len(set(card_suits))==1)):
         return 'Straight Flush',2,[max(card_numbers)]
      elif(max(card_counter_vals)==4):
         card_counter=dict(Counter(card_numbers))
         max_card1=list(card_counter.keys())[list(card_counter.values()).index(4)]
         max_card2=list(card_counter.keys())[list(card_counter.values()).index(1)]
         return 'Four of a Kind',3,[max_card1,max_card2]
      elif((max(card_counter_vals)==3) and (min(card_counter_vals)==2)):
         card_counter=dict(Counter(card_numbers))
         max_card1=list(card_counter.keys())[list(card_counter.values()).index(3)]
         max_card2=list(card_counter.keys())[list(card_counter.values()).index(2)]
         return 'Full House',4,[max_card1,max_card2]
      elif(len(set(card_suits))==1):
         max_card=card_numbers.copy()
         max_card.sort(reverse=True)
         return 'Flush',5,max_card
      elif(list(np.diff(card_numbers))==[1,1,1,1] or set(card_numbers)=={2,3,4,5,14}):
         max_card=card_numbers.copy()
         max_card.sort(reverse=True)
         return 'Straight',6,max_card
      elif((max(card_counter_vals)==3) and (min(card_counter_vals)==1)):
         card_counter=dict(Counter(card_numbers))
         max_card1=list(card_counter.keys())[list(card_counter.values()).index(3)]
         other_cards = [card for card in card_numbers if card != max_card1]
         other_cards.sort(reverse=True)
         max_card=[max_card1]+other_cards
         return 'Three of a Kind',7,max_card
      elif((max(Counter(card_counter_vals).values())==2) and (min(Counter(card_counter_vals).values())==1)):
         card_counter=dict(Counter(card_numbers))
         max_card3=list(card_counter.keys())[list(card_counter.values()).index(1)]
         other_cards = [card for card in card_numbers if card != max_card3]
         other_cards.sort(reverse=True)
         max_card=other_cards+[max_card3]
         return 'Two Pair',8,max_card
      elif((max(Counter(card_counter_vals).values())==3) and (min(Counter(card_counter_vals).values())==1)):
         card_counter=dict(Counter(card_numbers))
         max_card1=list(card_counter.keys())[list(card_counter.values()).index(2)]
         other_cards = [card for card in card_numbers if card != max_card1]
         other_cards.sort(reverse=True)
         max_card=[max_card1]+other_cards
         return 'One Pair',9,max_card
      else:
         max_card=card_numbers.copy()
         max_card.sort(reverse=True)
         return 'High Card',10,max_card


    def get_card_number(self, card):
      return SPECIAL_CARDS[card] if card in SPECIAL_CARDS else str(card)
        
        
    def get_trait(self, content, keyword):
      content='|'+content.replace('$player','').strip()+'|'
      lowercase_content=content.lower()
      if lowercase_content.find(keyword)>=0:
         start=content.find(keyword)+len(keyword)+1
         end=content.find('|',start)
         return content[start:end].strip()
      else:
         return None


    def get_traits_from_message(self,content):
      dict_traits={}
      modifiable_traits=MODIFIABLE_TRAITS if self.has_started else ALL_TRAITS
      for trait in modifiable_traits:
         dict_traits[trait]=self.get_trait(content, '|'+trait)
      return dict_traits


    async def get_current_player(self, players_name, message=None):
      logger.debug("Get current player")
      curr_player = next(filter(lambda p: p.name==players_name, self.players),None)
      if (message is not None) and (curr_player is None):
            await message.channel.send(PLAYER_NO_EXIST)
      return curr_player


    def find_possible_winners(self, i, winners):
      possible_winners=[]
      curr_max_card=0
      for winner in winners:
         if winner.curr_hand[2][i]>curr_max_card:
            possible_winners=[winner]
            curr_max_card=winner.curr_hand[2][i]
         elif winner.curr_hand[2][i]==curr_max_card:
            possible_winners.append(winner)
      return possible_winners




    def find_winner(self):
      active_players=[player for player in self.players if player.active]
      curr_hands=[player.curr_hand[1] for player in active_players]
      winner_indexes=[index for index,item in enumerate(curr_hands) if item==min(curr_hands)]
      logger.info("Winner indexes found: "+str(winner_indexes))
      if len(winner_indexes)==1:
         self.winner = [active_players[winner_indexes[0]]]
         self.winner[0].winning_hands+=1
      else:
         winners=[active_players[index] for index in winner_indexes]
         for i in range(len(active_players[winner_indexes[0]].curr_hand[3])):
            winners=self.find_possible_winners(i, winners)
            logger.debug("Winners found for "+str(i+1)+"th card: "+str(winners))
            if len(winners)==1: break
         self.winner=winners
            
      logger.debug("Winners found: "+str(self.winner))
      if len(self.winner)==1:
         player_name=self.get_player_name(self.winner[0])
         for winner in self.winner:
            winner.winning_hands+=1
         return CARDS_WINNER.format(
            player_name,self.winner[0].curr_hand[0],
            self.get_card_number(self.winner[0].curr_hand[2][0]))
      else:
         player_names=[]
         for winner in self.winner:
            winner.tied_hands+=1
            player_names.append(self.get_player_name(winner))
         return CARDS_TIE.format(
            ",".join(player_names),self.winner[0].curr_hand[0],
            self.get_card_number(self.winner[0].curr_hand[2][0]))


    def get_player_name(self, player):
      if player.traits.name is not None:
         return player.traits.name
      else:
         return player.name

    async def validate_game_has_started(self, message):
       if not self.has_started:
            await message.channel.send(CARDS_NO_START_GAME_MSG)
            return True
       return False


    async def validate_swapped_player(self,swapped_player_name,swapped_trait): 
      swapped_player=next(filter(lambda p: p.traits.name==swapped_player_name, 
                                                   self.players),None)
      if swapped_player is None:
         swapped_player=await self.get_current_player(swapped_player_name)
         if swapped_player is None:
            return SWAP_PLAYER_NO_FOUND_MSG,None
      if (not swapped_player.active) or (swapped_player.is_fold):
         return SWAP_PLAYER_FOLD_MSG,None
      if getattr(swapped_player.traits, swapped_trait) is None:
         return SWAP_SW_PLAYER_TRAIT_NONE_MSG,None
      if swapped_trait in swapped_player.permanent_swaps:
         return SWAP_PERM_TRAIT_MSG.format(swapped_trait),None
         
      return SWAP_OK_MSG,swapped_player



    async def validate_swap_message(self, splitted_msg, player):
      if len(splitted_msg)!=3:
         return SWAP_INVALID_MSG,None
      swapped_trait=splitted_msg[1]
      swapped_player_name=splitted_msg[2]
      # Trait validations
      if not hasattr(player.traits, swapped_trait):
         return SWAP_INVALID_TRAIT_MSG,None
      elif getattr(player.traits, swapped_trait) is None:
         return SWAP_TRAIT_NONE_MSG,None
      if swapped_trait in player.permanent_swaps:
         return SWAP_PERM_TRAIT_MSG.format(swapped_trait),None
      # Swapped player validations
      return await self.validate_swapped_player(swapped_player_name,swapped_trait)


    async def validate_royal_swap_message(self, splitted_msg, player):
      if len(splitted_msg)!=4 and len(splitted_msg)!=5:
         return SWAP_INVALID_MSG,None,None
      if len(splitted_msg)==4:
         swapped_trait=splitted_msg[1]
         swapped_player1_name=splitted_msg[2]
         swapped_player2_name=splitted_msg[3]
         if(swapped_player1_name=="myself"):
            swapped_player1_name=player.name
         if(swapped_player2_name=="myself"):
            swapped_player2_name=player.name
         # Swapped player 1 validations
         swapped_player1=next(filter(lambda p: p.traits.name==swapped_player1_name, 
                                                      self.players),None)
         if swapped_player1 is None:
            swapped_player1=await self.get_current_player(swapped_player1_name)
            if swapped_player1 is None:
               return SWAP_PLAYER_NO_FOUND_MSG,None,None
         if (not swapped_player1.active) or (swapped_player1.is_fold):
            return SWAP_PLAYER_FOLD_MSG,None,None
         if swapped_trait not in ["body","mental","full"]:
            if not hasattr(swapped_player1.traits, swapped_trait):
               return ROYAL_SWAP_INVALID_TRAIT_MSG,None,None
            elif getattr(swapped_player1.traits, swapped_trait) is None:
               return SWAP_SW_PLAYER_TRAIT_NONE_MSG,None,None
         # Swapped player 2 validations
         swapped_player2=next(filter(lambda p: p.traits.name==swapped_player2_name, 
                                                      self.players),None)
         if swapped_player2 is None:
            swapped_player2=await self.get_current_player(swapped_player2_name)
            if swapped_player2 is None:
               return SWAP_PLAYER_NO_FOUND_MSG,None,None
         if (not swapped_player2.active) or (swapped_player2.is_fold):
            return SWAP_PLAYER_FOLD_MSG,None,None
         if swapped_trait not in ["body","mental","full"]:
            if not hasattr(swapped_player1.traits, swapped_trait):
               return ROYAL_SWAP_INVALID_TRAIT_MSG,None,None
            elif getattr(swapped_player2.traits, swapped_trait) is None:
               return SWAP_SW_PLAYER_TRAIT_NONE_MSG,None,None
      else:
         if splitted_msg[1]!="permanent" and splitted_msg[1]!="temporal":
            return ROYAL_INVALID_PERM_SWAP,None,None
         swapped_trait=splitted_msg[2]
         swapped_player1_name=splitted_msg[3]
         swapped_player2_name=splitted_msg[4]
         if(swapped_player1_name=="myself"):
            swapped_player1_name=player.name
         if(swapped_player2_name=="myself"):
            swapped_player2_name=player.name
         # Swapped player 1 validations
         swapped_player1=await self.get_current_player(swapped_player1_name)
         if swapped_player1 is None:
            active_players=[player for player in self.players if player.active]
            swapped_player1=next(filter(lambda p: p.traits.name==swapped_player1_name, 
                                                         active_players),None)
            if swapped_player1 is None:
               return SWAP_PLAYER_NO_FOUND_MSG,None,None
         if getattr(swapped_player1.traits, swapped_trait) is None:
            return SWAP_SW_PLAYER_TRAIT_NONE_MSG,None,None
         # Swapped player 2 validations
         swapped_player2=await self.get_current_player(swapped_player2_name)
         if swapped_player2 is None:
            active_players=[player for player in self.players if player.active]
            swapped_player2=next(filter(lambda p: p.traits.name==swapped_player2_name, 
                                                         active_players),None)
            if swapped_player2 is None:
               return SWAP_PLAYER_NO_FOUND_MSG,None,None
         if getattr(swapped_player2.traits, swapped_trait) is None:
            return SWAP_SW_PLAYER_TRAIT_NONE_MSG,None,None

      return SWAP_OK_MSG,swapped_player1,swapped_player2


    def set_winner_by_fold_default(self):
       winner_name=""
       for player in self.players:
         if player.is_fold:
            player.is_fold=False
            player.is_active=True
         else:
            winner_name=self.get_player_name(player)
            self.winner=[player]
       return winner_name



    def restart_hands(self):
      random.shuffle(self.deck)
      random.shuffle(self.deck)
      self.index=0
      self.winner=None
      for player in self.players:
         player.restart_hand()
         player.played_hands+=1


    def save_players_state(self):
        for player in self.players:
            with open(player.name+".info", 'wb') as file:
                pickle.dump(player, file)


    async def load_player(self,players_name,message):
        commands=message.content.split(" ")
        if len(commands)==1:
            curr_player=await self.get_current_player(players_name)
            if curr_player:
                self.players.remove(curr_player)
            with open(players_name+".info", 'rb') as file:
                self.players.append(pickle.load(file))
            curr_player=await self.get_current_player(players_name)
            curr_player.restart_hand()
            return LOAD_PLAYER_MSG
        elif commands[1]=="traits_only":
            curr_player=await self.get_current_player(players_name)
            if curr_player:
               with open(players_name+".info", 'rb') as file:
                  player=pickle.load(file)
                  curr_player.traits=player.traits
            else:
               with open(players_name+".info", 'rb') as file:
                  player=pickle.load(file)
                  self.players.append(Player(players_name,player.traits))

            return LOAD_TRAITS_ONLY_MSG
        else:
            return LOAD_INVALID_MSG


    async def load(self, message, players_name):
        if self.has_started:
            content=LOAD_BUT_GAME_STARTED
        else:
            content=await self.load_player(players_name, message)
        await message.channel.send(content)


    async def player(self, message, players_name):
        logger.info("Create player for "+players_name)
        content=message.content
        dict_traits=self.get_traits_from_message(content)
        logger.debug("Traits found: "+str(dict_traits))
        curr_player=await self.get_current_player(players_name)
        if not curr_player:
            traits=Traits(**dict_traits)
            self.players.append(Player(players_name,traits))
            await message.channel.send(PLAYER_CREATED, reference=message)
        else:
            for key in dict_traits:
                if dict_traits[key] is None: continue
                setattr(curr_player.traits, key, dict_traits[key])
            await message.channel.send(PLAYER_TRAITS_UPDATED, reference=message)

    
    async def ready(self, message, players_name):
      if self.has_started:
         await message.channel.send(START_GAME_HAS_STARTED)
         return
      curr_player=await self.get_current_player(players_name)
      if curr_player is None:
            await message.channel.send(PLAYER_NO_EXIST)
            return
      curr_player.ready=True
      await message.channel.send(READY_MSG.format(players_name), reference=message)
      # Check if everyone is ready
      all_ready=True
      for player in self.players:
         if not player.ready:
            all_ready=False
            break
      if all_ready:
         self.has_started=True
         self.index=0
         self.winner=None
         await message.channel.send(READY_ALL_MSG)


    async def restart(self, message, players_name):
        # Check that game is started
        if await self.validate_game_has_started(message): return

        curr_player=await self.get_current_player(players_name)
        if curr_player is None:
            await message.channel.send(PLAYER_NO_EXIST)
            return
        curr_player.wants_restart=True
        players_want_restart=sum([player.wants_restart for player in self.players])
        if players_want_restart>=len(self.players)/2:
            self.restart_game()
            await message.channel.send(RESTART_MSG)
        else:
            num_players_restart=sum([player for player in self.players if player.wants_restart])
            await message.channel.send(RESTART_ADDED_PLAYER.format(num_players_restart))


    async def fold(self, message, players_name):
         # Check that game is started
         if await self.validate_game_has_started(message): return
         # Check if winners have swapped yet
         if self.winner:
            await message.channel.send(CARDS_WINNERS_NOT_SWAPPED_MSG)
            return
         curr_player=await self.get_current_player(players_name)
         if curr_player.curr_hand is None:
            await message.channel.send(FOLD_NO_HAND_MSG, reference=message)
            return
         curr_player.is_fold=True
         await message.channel.send(FOLD_MSG, reference=message)
         # If everyone but one player has folded, this player wins
         active_players=[player for player in self.players if player.active]
         playing_players=[player for player in active_players if not player.is_fold]
         if len(playing_players)==1:
            winner_name=self.set_winner_by_fold_default()
            await message.channel.send(FOLD_DEFAULT_WINNER.format(winner_name), reference=message)


    async def swap(self, message, players_name):
         # Check that game is started
         if await self.validate_game_has_started(message): return
         curr_player=await self.get_current_player(players_name, message)
         if curr_player is None: return
         # Validate winner
         if self.winner is None:
            await message.channel.send(SWAP_NO_WINNER, reference=message)
            return
         if curr_player not in self.winner:
            await message.channel.send(SWAP_NO_WINNER, reference=message)
            return
         # Is it royal swap
         if curr_player.curr_hand[0] in ROYAL_HANDS:
            await message.channel.send(SWAP_USE_ROYAL, reference=message)
            return
         # Validate message
         splitted_msg=message.content.split(" ")
         validate_message,swapped_player=await self.validate_swap_message(splitted_msg, curr_player)
         if validate_message!=SWAP_OK_MSG:
            await message.channel.send(validate_message, reference=message)
            return
         # Swap traits
         swapped_trait=splitted_msg[1]
         temp_trait=getattr(swapped_player.traits, swapped_trait)
         setattr(swapped_player.traits, swapped_trait, 
               getattr(curr_player.traits, swapped_trait))
         setattr(curr_player.traits, swapped_trait, temp_trait)
         # Restart hands
         self.winner.remove(curr_player)
         if not self.winner:
            self.restart_hands()
         if swapped_trait in BODY_TRAITS:
            content=SWAP_BODY_DONE_MSG.format(swapped_trait,
               getattr(curr_player.traits,swapped_trait),getattr(swapped_player.traits,swapped_trait))
         elif swapped_trait in MENTAL_TRAITS:
            content=SWAP_MENTAL_DONE_MSG.format(getattr(curr_player.traits,swapped_trait))
         else:
            content=SWAP_GEN_DONE_MSG.format(swapped_trait)
         await message.channel.send(content, reference=message)
         if not self.winner:
            await message.channel.send(SWAP_USE_CARD_MSG)
         self.save_players_state()


    async def royal_swap(self, message, players_name):
         # Check that game is started
         if await self.validate_game_has_started(message): return
         curr_player=await self.get_current_player(players_name, message)
         if curr_player is None: return
         # Validate winner
         if self.winner is None:
            await message.channel.send(SWAP_NO_WINNER, reference=message)
            return
         if curr_player not in self.winner:
            await message.channel.send(SWAP_NO_WINNER, reference=message)
            return
         # Is it royal swap
         if curr_player.curr_hand[0] not in ROYAL_HANDS:
            await message.channel.send(ROYAL_USE_SWAP, reference=message)
            return
         # Validate message
         splitted_msg=message.content.split(" ")
         validate_message,swapped_player1,swapped_player2=await self.validate_royal_swap_message(splitted_msg, curr_player)
         if validate_message!=SWAP_OK_MSG:
            await message.channel.send(validate_message)
            return
         # Swap traits
         if len(splitted_msg)==4:
            swapped_trait=splitted_msg[1]
            if swapped_trait=="body":
               for trait in BODY_TRAITS:
                  temp_trait=getattr(swapped_player1.traits, trait)
                  setattr(swapped_player1.traits, trait, 
                        getattr(swapped_player2.traits, trait))
                  setattr(swapped_player2.traits, trait, temp_trait)
            elif swapped_trait=="mental":
               for trait in MENTAL_TRAITS:
                  temp_trait=getattr(swapped_player1.traits, trait)
                  setattr(swapped_player1.traits, trait, 
                        getattr(swapped_player2.traits, trait))
                  setattr(swapped_player2.traits, trait, temp_trait)
            elif swapped_trait=="full":
               temp_traits=swapped_player1.traits
               swapped_player1.traits=swapped_player2.traits
               swapped_player2.traits=temp_traits
            else:
               temp_trait=getattr(swapped_player1.traits, swapped_trait)
               setattr(swapped_player1.traits, swapped_trait, 
                     getattr(swapped_player2.traits, swapped_trait))
               setattr(swapped_player2.traits, swapped_trait, temp_trait)
         else:
            permanence=splitted_msg[1]
            swapped_trait=splitted_msg[2]
            temp_trait=getattr(swapped_player1.traits, swapped_trait)
            setattr(swapped_player1.traits, swapped_trait, 
                  getattr(swapped_player2.traits, swapped_trait))
            setattr(swapped_player2.traits, swapped_trait, temp_trait)
            if permanence=='permanent':
               if swapped_trait not in swapped_player1.permanent_swaps:
                  swapped_player1.permanent_swaps.append(swapped_trait)
               if swapped_trait not in swapped_player2.permanent_swaps:
                  swapped_player2.permanent_swaps.append(swapped_trait)
            else:
               if swapped_trait in swapped_player1.permanent_swaps:
                  swapped_player1.permanent_swaps.remove(swapped_trait)
               if swapped_trait in swapped_player2.permanent_swaps:
                  swapped_player2.permanent_swaps.remove(swapped_trait)
         # Restart hands
         self.winner.remove(curr_player)
         if not self.winner:
            self.restart_hands()

         content=SWAP_GEN_DONE_MSG.format(swapped_trait)
         await message.channel.send(content, reference=message)
         self.save_players_state()


    async def describe(self, message, players_name):
         logger.info("Describe started for player's name: "+players_name)
         curr_player=await self.get_current_player(players_name, message)
         if curr_player is None: return

         split_content=message.content.split(" ")
         if len(split_content)!=2:
            logger.info("Invalid use of command $describe")
            await message.channel.send(DESCRIBE_INVALID_MSG, reference=message)
            return
         describe_player_name=split_content[1]
         logger.debug("Described player's name found: "+describe_player_name)
         if "myself"==describe_player_name:
            describe_player_name=players_name
         describe_player=await self.get_current_player(describe_player_name)
         logger.debug("Described player: "+str(describe_player))
         if describe_player is None:
            describe_player=next(filter(lambda p: p.traits.name==describe_player_name, 
                                                         self.players),None)
            logger.debug("Described player: "+str(describe_player))
            if describe_player is None:
               logger.debug("Described player not found")
               await message.channel.send(DESCRIBE_PLAYER_NO_FOUND_MSG, reference=message)
               return
         traits=describe_player.traits
         describe_dict=traits.dict()
         describe_dict["player"]=describe_player_name
         describe_dict["played_hands"]=describe_player.played_hands
         describe_dict["winning_hands"]=describe_player.winning_hands
         describe_dict["tied_hands"]=describe_player.tied_hands
         # Add permanent tag
         for permanent_swap in describe_player.permanent_swaps:
            describe_dict[permanent_swap]+=" *(permanent)*"
         description=DESCRIBE_MSG.format(**describe_dict)
         await message.channel.send(description, reference=message)


    async def look(self, message, players_name):
         # Check that game is started
         if await self.validate_game_has_started(message): return
         curr_player=await self.get_current_player(players_name, message)
         if curr_player is None: return

         split_content=message.content.split(" ")
         if len(split_content)!=2:
            await message.channel.send(DESCRIBE_INVALID_MSG, reference=message)
            return
         describe_player_name=split_content[1]
         look_description=LOOK_MSG
         actions={"body_actions":LOOK_BODY_ACTIONS, 
            "pers_actions":LOOK_PERSONALITY_ACTIONS,
            "skill_actions":LOOK_SKILL_ACTIONS}
         if "myself"==describe_player_name or describe_player_name==players_name:
            describe_player_name=players_name
            look_description=LOOK_MYSELF_MSG
            actions={"body_actions":LOOK_MYSELF_BODY_ACTIONS, 
               "pers_actions":LOOK_MYSELF_PERSONALITY_ACTIONS,
               "skill_actions":LOOK_MYSELF_SKILL_ACTIONS}
         describe_player=await self.get_current_player(describe_player_name)
         if describe_player is None:
            describe_player=next(filter(lambda p: p.traits.name==describe_player_name, 
                                                         self.players),None)
            if describe_player is None:
               await message.channel.send(DESCRIBE_PLAYER_NO_FOUND_MSG, reference=message)
               return
         # Fill body action
         body_trait=getattr(describe_player.traits,random.choice(BODY_TRAITS))
         body_action=random.choice(actions["body_actions"]).format(body_trait)
         # Fill personality action
         pers_trait=getattr(describe_player.traits,random.choice(PERSONALITY_TRAITS))
         pers_action=random.choice(actions["pers_actions"]).format(pers_trait)
         # Fill skill action
         skill_trait=getattr(describe_player.traits,random.choice(SKILL_TRAITS))
         skill_action=random.choice(actions["skill_actions"]).format(skill_trait)
         description=look_description.format(body_action,pers_action,skill_action)
         await message.channel.send(description, reference=message)


    async def change_order(self, message, players_name):
       logger.info("Change order command called by player "+players_name)
       # Check that game is started
       if await self.validate_game_has_started(message): return
       # Get player
       curr_player=await self.get_current_player(players_name, message)
       if curr_player is None: return
       # Validate message
       split_content=message.content.split(" ")
       if len(split_content)!=3:
          await message.channel.send(CHANGE_ORDER_INVALID_MSG, reference=message)
          return
       if split_content[1][:-1]!=split_content[2][:-1]:
          await message.channel.send(CHANGE_ORDER_INVALID_MSG, reference=message)
          return
       if (split_content[1] not in CH_ORDER_TRAITS) or (split_content[2] not in CH_ORDER_TRAITS):
          await message.channel.send(CHANGE_ORDER_USE_CH_ORDER_MSG.format(
                              ",".join(CH_ORDER_TRAITS)), reference=message)
          return
       # Change order
       temp_trait=getattr(curr_player.traits, split_content[1])
       setattr(curr_player.traits, split_content[1], getattr(curr_player.traits, split_content[2]))
       setattr(curr_player.traits, split_content[2], temp_trait)
       await message.channel.send(CHANGE_ORDER_SUCCESS_MSG, reference=message)



    async def cards(self, message, players_name, client, start_force_func):
         logger.info("Cards command called by player "+players_name)
         # Check that game is started
         if await self.validate_game_has_started(message): return
         # Check that you're not the only player
         if len(self.players)==1:
            await message.channel.send(CARDS_ONLY_1_PLAYER_MSG)
            return
         # Check if winners have swapped yet
         if self.winner:
            await message.channel.send(CARDS_WINNERS_NOT_SWAPPED_MSG)
            return
         # If first hand, start timeout
         active_players=[player for player in self.players if player.active]
         if len(active_players)==0:
            client.loop.create_task(start_force_func(message))
         # Get and set important variables
         curr_player=await self.get_current_player(players_name, message)
         if curr_player is None: return
         curr_player.active=True
         curr_player.last_active=datetime.datetime.now()
         # Check if user already played
         if curr_player.curr_hand is not None:
               player_name=self.get_player_name(curr_player)
               await message.channel.send(CARDS_PLAYER_HAS_PLAYED.format(player_name))
               return
         # Play hand
         cards,content=self.draw_cards()
         logger.info("Cards drawn: "+str(cards))
         # Check poker hand
         hand,score,max_card=self.check_poker_hand(cards)
         logger.debug("Poker summary: "+str([hand,score,max_card,cards]))
         curr_player.curr_hand=[hand,score,max_card,cards]
         # Response
         await message.author.send(content)
         # Check if all players have played
         active_players=[player for player in self.players if player.active]
         played_hands=sum([player.curr_hand is not None for player in active_players])
         if played_hands==len(self.players):
            win_message=self.find_winner()
            # Show the hands of all players
            summary="**Hands:**\r\n"
            for player in active_players:
               card_summary=", ".join([self.get_card_number(card[0])+' '+card[1] 
                                                for card in player.curr_hand[3]])
               summary+=CARDS_SUMMARY.format(player.traits.name,card_summary)+"\r\n"
            await message.channel.send(summary)
            await message.channel.send(win_message)


    async def all_players(self, message):
       content=ALL_PLAYERS
       for player in self.players:
          player_name=self.get_player_name(player)
          status="Fold" if player.is_fold else ("Playing" if player.active else "Inactive")
          content+="\r\n"+player_name+" -> "+status
       await message.channel.send(content)


    async def start(self, message, client, start_delay_func, start_force_func):
      if self.has_started:
         await message.channel.send(START_GAME_HAS_STARTED)
         return
      all_ready=True
      for player in self.players:
            if not player.ready:
               all_ready=False
               break
      if all_ready:
            self.has_started=True
            self.index=0
            self.winner=None
            await message.channel.send(START_MSG)
      else:
            if self.task_delay is None:
               self.task_delay=client.loop.create_task(start_delay_func(message))
            if self.task_st_force is None:
               self.task_st_force=client.loop.create_task(start_force_func(message))
            #if self.task_check_active is None:
            #   self.task_check_active=client.loop.create_task(check_active_func(message))
            await message.channel.send(START_DELAY_MSG)


    def create_test_player(self):
      dict_traits={}
      for trait in ALL_TRAITS:
         dict_traits[trait]="Test "+trait
      traits = Traits(**dict_traits)
      player=Player("Test",traits)
      self.players.append(player)
      player.ready=True
      player.active=True
      player.curr_hand=['One Pair',9,[3,7,4,2],[(3,'♣ (C)'),(3,'♠ (S)'),(4,'♦ (D)'),(7,'♦ (D)'),(2,'♣ (C)')]]