"""
Contains the Galaxy class, containing the data pertaining to a game map.
"""

import random
import unittest

import name

from planet import Planet
import game
from faction import Faction

class Galaxy(object):
    def __init__(self, width=50, height=50, density=1.0/25, seed=None):
        self.width = None # This galaxies width in pc.
        self.height = None # This galaxies height in pc.
        
        self.planets = {} # A dictionary of planets in the Galaxy, 
        # sorted according to an (x,y) tuple of their coordinates in pc.

        for y in range (height):
            for x in range (width):
                game.ships[(x,y)] = [] # Add a list to each coordinate position.

        
        self.generate(width, height, density, seed)
        self.add_player()
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
    
    def add_player(self):
        faction = Faction()
        faction.generate()
        game.factions.append(faction)
        
        homeworld = random.choice(self.planets.values() )
        homeworld.set_(150,150,150,[1,5,10,15,20],1,faction.type)
        homeworld.set_owner(faction)
        # Give the planet the faction's name.
        homeworld.name = faction.name.split(" ",1)[0]
    
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
        
