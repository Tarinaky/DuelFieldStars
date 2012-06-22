import random
import color

import name

import model
from model import tech
import logging

log = logging.getLogger(__name__)

class Faction(object):
    """
    Represents a player controlled faction in the game.
    Stores lists of all their assets.
    """
    def __init__(self):

        self.name = "Foo Imperium"
        self.flag = (color.COLORS["white"],color.COLORS["white"])
        self.type = 'X'

        self.rez = 0 # Resources
        self.planets = [] # List of planets owned
        self.ships = [] # List of ships owned
        
        self.ready = False

        self.tech = self.basic_tech() # Table of tech levels by key
        self.research = []
        self.special_choice = {} # Used for storing colony types to accumulate or
        # Special Tech upgrades.
        self.colony_types = ['X']

    @property
    def income(self):

        income = 0
        for planet in self.planets:
            income += planet.income
        return income
    
    @property 
    def upkeep(self):
        i = 0
        for parsec in model.game.ships.values():
            for ship in parsec:
                if ship.owner == self:
                    i+=1
        return i

    def tick(self):
        """Update the faction by 1 turn."""
        self.rez -= self.upkeep
        self.rez += self.income

        for planet in self.planets:
            planet.tick
        
        # Research technology    
        for technology in self.research:
            self.tech[technology] +=1
        self.research = []
        for technology in self.special_choice.keys():
            if technology == "Colony Technology": # Gain new colony types
                self.colony_types.append(self.special_choice[technology])
            else:
                log.debug("Unknown special tech "+tech)
        self.special_choice = {}
            
    def generate(self):
        self.name = name.faction_name()
        self.rez = 2
        "Set flag"
        backgroundColor = color.random()
        while backgroundColor == color.COLORS["black"]:
            backgroundColor = color.random()
        forgroundColor = color.random()
        while forgroundColor == backgroundColor:
            forgroundColor = color.random()
        self.flag = (forgroundColor,backgroundColor)
        "Set type"
        self.type = random.choice(['A','B','C','D','E'])
        self.colony_types.append(self.type)
         
    
    def add_planet(self, planet):
        self.planets.append(planet)
        
    def remove_planet(self, planet):
        self.planets.remove(planet)
        
    def add_ship(self, ship):
        self.ships.append(ship)
        
    def remove_ship(self, ship):
        self.ships.remove(ship)
        
    def basic_tech(self):
        a = {}
        for item in tech.a:
            if item.advanced == False:
                a[item.name] = 1
        #a["Mining Enhancement Technology"] = 24
        return a


PLAYERFACTION = None

