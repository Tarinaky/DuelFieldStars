"""
Contains the planet class, containing all data defining a world in the game's Galaxy.
"""

import random
import unittest
import math

import name

class Planet(object):
    def __init__(self, *position):
        self.name = name.planet_name()
        self.owner = None
        self.is_homeworld = False

        self.construction = None
        
        self.baseValue = 0 # The planet's base value expressed as a percentile.
        self.currentValue = 0 # The planet's value after terraforming.
        self.realisedValue = 0 # The planet's presently realised value expressed as a percentile.
                
        self.improvementLevels = [] # The planet's five mining improvement levels.
        self.realisedImprovement = 0 
        
        self.type_ = '' # The planet's type, expressed as one of the letters A, B, C, D or E.
        
        self.position = position # The planet's position expressed as an (x,y) tuple.
        return
    
    def set_(self,baseValue, currentValue, realisedValue, improvementLevels, realisedImprovement, type_):
        self.baseValue = baseValue
        self.currentValue = currentValue
        self.realisedValue = realisedValue
        self.improvementLevels = improvementLevels
        self.realisedImprovement = realisedImprovement
        self.type_ = type_
        
    def set_owner(self,faction):
        if self.owner != None:
            self.owner.remove_planet(self)
        self.owner = faction
        self.owner.add_planet(self)
    
    def generate(self,prng):
        self.baseValue = prng.randint(50,150)
        self.currentValue = self.baseValue
        self.realisedValue = 0
        
        accumulator = prng.randint(1,20)
        self.improvementLevels = [accumulator]
        for _ in range(4):
            accumulator = accumulator + prng.randint(5,20)
            self.improvementLevels.append(accumulator)
                
        self.type_ = prng.choice(['A','B','C','D','E'])
        return
    
    @property
    def income(self):
        """Calculates this planet's per turn income."""
        income = round(self.realisedValue / float(100) * math.sqrt(self.owner.tech["Production Technology"]),2)
        for level in self.improvementLevels:
            if level <= self.realisedImprovement:
                income += 1
        return income
    
    @property
    def growth(self):
        """Calculates this planet's per turn growth."""
        if self.owner == None:
            return 0
        if self.type_ == self.owner.type:
            return 10
        return 5

    def tick(self):
        """Update the planet by 1 turn."""
        self.realisedValue += self.growth
        if self.realisedValue > self.currentValue:
            self.realisedValue = self.currentValue
        "Build construction item."
        if self.construction != None:
            self.construction(self.owner, self.position)
            self.construction = None

class PlanetTest(unittest.TestCase):
    def setUp(self):
        self.fixture = Planet(0,0)
        return
    
    def test_generation(self):
        self.fixture.generate(random.Random(0xDEADBEEF) )   
        return

NOPLANET = Planet()
