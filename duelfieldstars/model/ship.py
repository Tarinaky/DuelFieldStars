import name

import game

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
        
        game.ships[position].append(self)
                
    @property
    def attack(self): 
        """Returns the attack value modified by tech levels."""
        return self.offenseValue
    @property
    def defence(self): 
        """Returns the defence value modified by tech levels."""
        return self.defenseValue
    @property
    def speed(self): 
        """Speed in pc, modified by tech levels."""
        return 3
    
    def tick(self):
        """Process a turn."""
        return
    
def process_ship_turn(ships):
        """Takes a list of ships and iterates over them to produce the new ship state."""
        return {}
    
class Cruiser(Ship):
    """This class represents a Cruiser"""
    type_ = "Cruiser"
    offenseValue = 2
    defenseValue = 1
    marines = False
    colony = False
    
    def __init__(self,faction,position):
        super(Cruiser,self).__init__(faction,position)
        
class MarineTransport(Ship):
    """This class represents a ground assault ship."""
    type_ = "Marine Transport"
    offenseValue = 1
    defenseValue = 1
    marines = True
    colony = False
    
    def __init__(self,faction,position):
        super(MarineTransport,self).__init__(faction,position)
        
class ColonyTransport(Ship):
    """This class represents a colony ship."""
    type_ = "Colony Transport"
    offenseValue = 0
    defenseValue = 1
    marines = False
    colony = True
    
    def __init__(self,faction,position):
        super(ColonyTransport,self).__init__(faction,position)
