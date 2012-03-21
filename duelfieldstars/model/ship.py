import name

import game

from faction import Faction, NOFACTION

class Ship(object):
    """Abstract class for space ships."""
    type_ = "error"
    offenseValue = 0
    defenseValue = 1
    marines = False
    colony = False
        
    def __init__(self,faction,position):
        self.faction = faction
        self.position = position # Position in pc
        self.name = name.ship_name()
        
        self.destination = self.position # Target destination.
                
    @property
    def attack(self): # Returns the attack value modified by tech levels.
        return self.offenseValue
    @property
    def defence(self): # Returns the defence value modified by tech levels.
        return self.defenseValue
    @property
    def speed(self): # Speed in pc, modified by tech levels.
        return 3
        
    
class Cruiser(Ship):
    """This class represents a Cruiser"""
    type_ = "Cruiser"
    offenseValue = 1
    defenseValue = 2
    marines = False
    colony = False
    
    def __init__(self,faction,position):
        super(Cruiser,self).__init__(faction,position)
        
class MarineLander(Ship):
    """This class represents a ground assault ship."""
    type_ = "Marine Lander"
    offenseValue = 0.5
    defenseValue = 2
    marines = True
    colony = False
    
    def __init__(self,faction,position):
        super(MarineLander,self).__init__(faction,position)
        
class ColonyTransport(Ship):
    """This class represents a colony ship."""
    type_ = "Colony Transport"
    offenseValue = 0
    defenseValue = 1
    marines = False
    colony = True
    
    def __init__(self,faction,position):
        super(ColonyTransport,self).__init__(faction,position)
