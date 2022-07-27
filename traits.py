""" traits.py
Dataclass Traits
"""

from dataclasses import dataclass,fields

@dataclass
class Traits():
    """Dataclass to map Traits (body features, personality traits,...)"""
    name:str=None
    hair:str=None
    eyes:str=None
    mouth:str=None
    nose:str=None
    ears:str=None
    face:str=None
    chest:str=None
    arms:str=None
    hands:str=None
    waist:str=None
    hips:str=None
    ass:str=None
    groin:str=None
    legs:str=None
    feet:str=None
    phys_trait1:str=None
    phys_trait2:str=None
    phys_trait3:str=None
    clothing:str=None
    age:int=None
    ethnicity:str=None
    gender:str=None
    sexuality:str=None
    wallet:str=None
    skill1:str=None
    skill2:str=None
    skill3:str=None
    relationships:str=None
    pers_trait1:str=None
    pers_trait2:str=None
    pers_trait3:str=None
    other1:str=None
    other2:str=None

    def dict(self):
        return {field.name: str(getattr(self,field.name)) for field in fields(self)}
                  
