""" player.py
Class player to manage player's attributes
"""

import datetime

class Player:
    """Represents a player in the poker game"""
    def __init__(self, name:str, traits):
       self.name=name
       self.active=False
       self.last_active=datetime.datetime.now()
       self.ready=False
       self.is_fold=False
       self.orig_traits=traits
       self.traits=traits
       self.permanent_swaps=[]
       self.wants_restart=False
       self.curr_hand=None
       self.force_inactive_count=0
       self.winning_hands=0
       self.tied_hands=0
       self.played_hands=0
       
    def __str__(self):
        return self.name

    def __repr__(self) -> str:
        return "Player({})".format(self.name)

    def __eq__(self, other):
       if(type(other)==str):
           return self.name==other
       else:
           return super().__eq__(other) 

    def restart_hand(self):
        self.curr_hand=None
        self.active=False
        self.is_fold=False
        self.wants_restart=False
