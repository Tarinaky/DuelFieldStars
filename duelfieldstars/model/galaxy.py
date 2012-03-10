"""
Contains the Galaxy class, containing the data pertaining to a game map.
"""

import random
import unittest

class Galaxy(object):
    def __init__(self, width=50, height=50, density=1.0/3, seed=None):
        self.width = None # This galaxies width in pc.
        self.height = None # This galaxies height in pc.
        
        self.planets = {} # A dictionary of planets in the Galaxy, 
        # sorted according to an (x,y) tuple of their coordinates in pc.
        
        self.generate(width, height, density, seed)
        return
        
    def generate(self, width=50, height=50, density=1.0/3, seed=None):
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
                self.planets[(x,y)] = "TODO: Implement planets."
        return
    
class GalaxyTest(unittest.TestCase):
    def setUp(self):
        self.fixture = Galaxy()
        return
    
    def test_generation(self):
        self.fixture.generate(50, 50, 1.0/3, None)
        
        self.assertTrue(len(self.fixture.planets) == (50-2)**2 / 3, "Galaxy has the wrong number of planets.")  
        