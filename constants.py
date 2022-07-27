""" constants.py
Constant variables used during the program
"""

START_DELAY=5
FORCE_PLAY_DELAY=10

SPECIAL_CARDS={14:'Ace',11:'Jack',12:'Queen',13:'King'}

ROYAL_HANDS=["Royal Flush","Straight Flush","Four of a Kind","Full House"]

BODY_TRAITS=["hair","eyes","mouth","nose","ears","face","chest","arms",
   "hands","waist","hips","ass","groin","legs","feet","phys_trait1",
   "phys_trait2","phys_trait3","age","ethnicity"]

PERSONALITY_TRAITS=["pers_trait1","pers_trait2","pers_trait3"]

SKILL_TRAITS=["skill1","skill2","skill3"]

MENTAL_TRAITS=["gender","sexuality"]+PERSONALITY_TRAITS+SKILL_TRAITS

MODIFIABLE_TRAITS=["clothing","relationships"]

OTHER_TRAITS=["name","other1","other2"]

ALL_TRAITS=BODY_TRAITS+MENTAL_TRAITS+MODIFIABLE_TRAITS+OTHER_TRAITS

CH_ORDER_TRAITS=["phys_trait1","phys_trait2","phys_trait3",
   "pers_trait1","pers_trait2","pers_trait3","skill1","skill2",
   "skill3","other1","other2"]