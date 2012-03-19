import random
import color

import name

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

        self.tech = {} # Table of tech levels by key

    @property
    def income(self):

        income = 0
        for planet in self.planets:
            income += planet.income
        return income

    def tick(self):
        """Update the faction by 1 turn."""
        self.rez += self.income

        for planet in self.planets:
            planet.tick
            
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
         
    
    def add_planet(self, planet):
        self.planets.append(planet)
        
    def remove_planet(self, planet):
        self.planets.remove(planet)


NOFACTION = Faction()

