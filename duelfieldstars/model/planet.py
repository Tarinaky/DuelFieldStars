"""
Contains the planet class, containing all data defining a world in the game's Galaxy.
"""

import random
import unittest

class Planet(object):
    def __init__(self, position):
        self.baseValue = None # The planet's base value expressed as a percentile.
        self.realisedValue = None # The planet's presently realised value expressed as a percentile.
        
        self.improvementLevels = [] # The planet's five mining improvement levels. 
        
        self.type = None # The planet's type, expressed as one of the letters A, B, C, D or E.
        
        self.position = position # The planet's position expressed as an (x,y) tuple.
        return
    
    def generate(self,prng):
        self.baseValue = prng.randint(50,150)
        self.realisedValue = 0
        
        accumulator = prng.randint(1,20)
        self.improvementLevels = [accumulator]
        for _ in range(4):
            accumulator = accumulator + prng.randint(5,20)
            self.improvementLevels.append(accumulator)
        
        self.type = prng.choice(['A','B','C','D','E'])
        return

class PlanetTest(unittest.TestCase):
    def setUp(self):
        self.fixture = Planet((0,0) )
        return
    
    def test_generation(self):
        self.fixture.generate(random.Random(0xDEADBEEF) )   
        return
