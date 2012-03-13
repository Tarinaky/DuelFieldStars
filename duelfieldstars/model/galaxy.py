"""
Contains the Galaxy class, containing the data pertaining to a game map.
"""

import random
import unittest

from planet import Planet

class Galaxy(object):
    def __init__(self, width=50, height=50, density=1.0/25, seed=None):
        self.width = None # This galaxies width in pc.
        self.height = None # This galaxies height in pc.
        
        self.planets = {} # A dictionary of planets in the Galaxy, 
        # sorted according to an (x,y) tuple of their coordinates in pc.
        
        self.generate(width, height, density, seed)
        return
        
    def generate(self, width, height, density, seed=None):
        """
        Setup this galaxy with the correct width, height and generate the new planets.
        """
        self.width = width
        self.height = height
        
        maxPlanets = (self.width-2) * (self.height-2) * density
        prng = random.Random(seed)
        while len(self.planets) < maxPlanets:
            x = prng.randint(1, self.width-1)
            y = prng.randint(1, self.height-1)
            if (x,y) not in self.planets:
                newPlanet = Planet(x,y)
                newPlanet.generate(prng)
                self.planets[(x,y)] = newPlanet
        return
    
    def at(self,x,y):
        if (x,y) in self.planets:
            return self.planets[(x,y)]
        else:
            return None
    
class GalaxyTest(unittest.TestCase):
    def setUp(self):
        self.fixture = Galaxy()
        return
    
    def test_generation(self):
        self.fixture.generate(50, 50, 1.0/3, None)
        
        self.assertTrue(len(self.fixture.planets) == (50-2)**2 / 3, "Galaxy has the wrong number of planets.")  
        