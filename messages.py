""" messages.py
Modify all messages to be returned by discord bot
"""

START_MSG="Game started"
START_DELAY_MSG="Not all players are ready. Game will start in "+ \
   "{} minutes"
HELP_MSG_PART_1="""The game is played in the following way: first create a character using $player command. When all players are created, use $start to begin the game. Use $cards to take 5 cards from the deck. The winner is the one who gets the higher poker hand. Use $fold if you want to skip this hand. The winner can use $swap to choose whom to swap with.
__List of commands part 1:__
   **$help:** Shows this window message
   **$help_attributes:** Shows the list of possible attributes
   **$start:** Begins poker game if all players are ready, if not, it will start a countdown before the game starts
   **$player:** Creates a character (player). All characters must be 18+. To see a list of attributes use $help_attributes. 
       No all attributes need to be set, but only set attributes can be swapped. Attributes need to be separated either 
       by symbol '|'
       __*Example of use:*__ $player name:John | hair:long,brown | face: plump, bearded
       It's possible to update an attribute by calling the command again: $player gender: male, this will update the 
       player's gender to male, leave empty to erase value. This can be done only before the game starts. When it 
       starts, only attributes clothing, relationships, other1 and other2 can be changed
   **$all_players:** Shows all players and their status
   **$ready:** Sets the player status to ready
   **$restart:** Restarts game. All players traits reset back to normal. Half of the players should agree
"""
HELP_MSG_PART_2="""__List of commands part 2:__
   **$cards:** Plays a poker hand. The winner will be decided after all players play
   **$fold:** Folds a poker hand. The player won't be included as a swappable player for this turn, unless everyone else has
       folded too.
   **$swap:** Swaps two traits between the winner and another player 
       $swap {{trait}} {{player}}
       __*Example of use:*__ $swap eyes John
   **$royal_swap:** If you win with a 'Royal Flush', 'Straight Flush', Four of a Kind or a Full House, you can do a permanent swap, 
       a body swap, a mental swap, or a full swap (all traits) between you and other players. 
       *List of body traits:* {}. 
       *List of mental traits:* {}. 
       Permanent swaps can only be reversed with another permanent swap. Permanent swaps can only be done to  
       individual traits (not body, personality or full swaps). To remove the permanence of a permanent swap, use temporal  
       $royal_swap {{permanent|temporal}} {{trait}} {{player1}} {{player2}}
       *Example of use:* $royal_swap body John Sally, $royal_swap permanent hair myself Sally
   **$describe:** Enumerates all traits of a player - $describe {{player}}
       __*Example of use:*__ $describe Sally. Also valid: $describe myself
   **$look:** Madlibs that describe a player - $look {{player}}
       __*Example of use:*__ $look Sally. Also valid: $look myself
   **$change_order:** Change two traits within the same category. You only change traits for yourself. For example skill1 
       with skill3. Use it to align a swap with another player.
       __*Example of use:*__ $change_order pers_trait1 pers_trait2
"""

HELP_ATTRIBUTES_MSG="""LIST OF ATTRIBUTES:
   -name: e.g. John, Sally
   -hair: e.g. long, brown and curly
   -eyes: e.g. brown, good eyesight
   -mouth: e.g. small, rosy, upbeat smile
   -nose: e.g. thin, runny
   -ears: e.g. small, pointy
   -face: e.g. plump, bearded
   -chest: e.g. D cup breast
   -arms: e.g. long, muscular
   -hands: e.g. dainty, manicured
   -waist: e.g. narrow
   -hips: e.g. wide, boyish, average
   -ass: e.g. tight, curvy
   -groin: e.g. vagina, penis
   -legs: e.g. skinny, hairless
   -feet: e.g. small, arched, nails painted blue
   -phys_trait1: Anything physical not mentioned before e.g. tatoos
   -phys_trait2: e.g. birthmarks, moles
   -phys_trait3: e.g. bunny ears, tail
   -clothing: e.g. t-shirt, top, dress, pijama, bra, glasses, watches
   -age: e.g. 25,40
   -ethnicity: e.g. American, Indian, Hispanic
   -gender: e.g. male, female, non binary
   -sexuality: e.g. heterosexual, homosexual, asexual
   -wallet: Economical situation. e.g. Rich, poor, belongings
   -skill1: e.g. Speak French
   -skill2: e.g. Gymnastics
   -skill3: e.g. Singing
   -relationships: e.g. Has boyfriend, has family, single
   -pers_trait1: Personality trait e.g. bookworm
   -pers_trait2: e.g. talkative
   -pers_trait3: e.g. assertive
   -other1: Any other thing that can be swapped. e.g. education level / intelligence
   -other2: e.g. a memory"""

DESCRIBE_MSG="""**Player: {player}**
   - Name: {name}
   - Hair: {hair}
   - Eyes: {eyes}
   - Mouth: {mouth}
   - Nose: {nose}
   - Ears: {ears}
   - Face: {face}
   - Chest: {chest}
   - Arms: {arms}
   - Hands: {hands}
   - Waist: {waist}
   - Hips: {hips}
   - Ass: {ass}
   - Groin: {groin}
   - Legs: {legs}
   - Feet: {feet}
   - Physical Trait 1: {phys_trait1}
   - Physical Trait 2: {phys_trait2}
   - Physical Trait 3: {phys_trait3}
   - Clothing: {clothing}
   - Age: {age}
   - Ethnicity: {ethnicity}
   - Gender: {gender}
   - Sexuality: {sexuality}
   - Wallet: {wallet}
   - Skill 1: {skill1}
   - Skill 2: {skill2}
   - Skill 3: {skill3}
   - Relationships: {relationships}
   - Personality trait 1: {pers_trait1}
   - Personality trait 2: {pers_trait2}
   - Personality trait 3: {pers_trait3}
   - Other 1: {other1}
   - Other 2: {other2}
   - Rounds played: {played_hands}
   - Rounds won: {winning_hands}
   - Rounds tied: {tied_hands}
"""

LOOK_BODY_ACTIONS=["his/her/their {} grabs your attention", 
   "you stare at his/her/their {}", 
   "you notice his/her/their {}"]
LOOK_PERSONALITY_ACTIONS=["he/she/they seems to be {}",
   "he/she/they is quite {}",
   "his/her/their {} personality catches your interest"]
LOOK_SKILL_ACTIONS=["he/she/they is showing off her {}",
   "his/her/their ability to {} is quite interesting"]
LOOK_MSG="You gaze at {}, {}, {}, {}"

LOOK_MYSELF_BODY_ACTIONS=["your {} grabs your attention", 
   "you stare at your {}", 
   "you notice your {}"]
LOOK_MYSELF_PERSONALITY_ACTIONS=["you seem to be {}",
   "you are quite {}",
   "your {} personality catches your interest"]
LOOK_MYSELF_SKILL_ACTIONS=["you show off your {}",
   "your ability to {} is quite interesting"]
LOOK_MYSELF_MSG="You gaze at yourself in the mirror, {}, {}, {}"

ALL_PLAYERS="__Players__ -> __Status__"
PLAYER_CREATED="Player created"
PLAYER_TRAITS_UPDATED="Traits have been updated"
PLAYER_NO_EXIST="Player doesn't exist or inactive. To create a player use command $player"
RESTART_MSG='Game restarted'
RESTART_ADDED_PLAYER='Num of players who wants restart: {}. Half of the players should use command restart to restart game'
FORCE_INACTIVE_MSG="Player {} has folded/will fold automatically due to inactivity. Use command $cards to activate"
FORCE_WARNING_INACTIVE_MSG="Player {} hasn't played in the last three turns. Next time, it'll be removed from game"
FORCE_PLAYER_REMOVE_MSG="Player {} has been removed from the game"

LOAD_BUT_GAME_STARTED="No loading can't be done after game has started"
LOAD_INVALID_MSG="Use of load command is invalid"
LOAD_TRAITS_ONLY_MSG="Traits have been loaded"
LOAD_PLAYER_MSG="Player has been loaded"

START_GAME_HAS_STARTED='Game has already started'
READY_MSG='{} is ready'
READY_ALL_MSG='All players are ready. Game has started'
FOLD_MSG='You have folded'
FOLD_NO_HAND_MSG='You have no hand to fold'
FOLD_NO_WINNER='Everyone folded or is inactive. Starting next round...'
CARDS_NO_START_GAME_MSG="Game hasn't started yet"
CARDS_WINNERS_NOT_SWAPPED_MSG="Winners must swap first, before starting next round"
CARDS_PLAYER_HAS_PLAYED="{} has already played a hand"
CARDS_SUMMARY="__{}__: {}"
CARDS_WINNER="**{}** has won with {} and highest card {}"
CARDS_TIE="Tie between players {} with {} and highest card {}"
CARDS_ONLY_1_PLAYER_MSG="You need more than 1 player to play. Restart the game with more players"
FOLD_DEFAULT_WINNER="Player {} has won by default because everybody else has folded"

SWAP_INVALID_MSG="Use of swap command is invalid"
SWAP_OK_MSG="Swap is valid"
SWAP_USE_ROYAL="You won with a Royal Flush or Straight Flush. Congratulations! Use $royal_swap instead"
SWAP_INVALID_TRAIT_MSG="This trait doesn't exist"
SWAP_PERM_TRAIT_MSG="You concentrate to swap {}, but it doesn't work. It must be a perma swap"
SWAP_TRAIT_NONE_MSG="You can only swap traits that have a value"
SWAP_PLAYER_NO_FOUND_MSG="The player to swap with might not be active or might not exist"
SWAP_PLAYER_FOLD_MSG="Can't swap with palyer who has folded or is inactive"
SWAP_SW_PLAYER_TRAIT_NONE_MSG="Swapped player doesn't have a value for this trait"
SWAP_BODY_DONE_MSG="*Whoosh!* You look at your {} in the mirror and see {}, instead of your usual {}"
SWAP_MENTAL_DONE_MSG="*Whoosh!* You feel different. It seems you are/can do {}"
SWAP_GEN_DONE_MSG="*Whoosh!* {} have been swapped"
SWAP_NO_WINNER="Only winner can swap"
SWAP_USE_CARD_MSG="Congratulations to the winner. Use $cards to play next round"

ROYAL_SWAP_INVALID_TRAIT_MSG="This trait doesn't exist. Special traits are body, mental or full"
ROYAL_USE_SWAP="This command is only used when you win a Royal Flush"
ROYAL_INVALID_PERM_SWAP="Permanent swap detected, but use of command is invalid. Use keys permanent or temporal"

DESCRIBE_INVALID_MSG="Invalid use of command '$describe'. Use $help for more information"
DESCRIBE_PLAYER_NO_FOUND_MSG="Player to describe was not found"

CHANGE_ORDER_INVALID_MSG="Invalid use of command '$change_order'. Use $help for more information"
CHANGE_ORDER_USE_CH_ORDER_MSG="Only the following traits can change order: {}"
CHANGE_ORDER_SUCCESS_MSG="The traits have changed places"