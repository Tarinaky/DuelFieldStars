import name

import game
import logging

log = logging.getLogger(__name__)

def get_path(source,destination):
    """
    Obtain and return a list of the coordinates of all tiles between two points.
    """
    values = []
    (x0,y0) = source
    (x1,y1) = destination
    
    dx = x1 - x0
    dy = y1 - y0
    if dx == 0:
        gradient = dy
    else:
        if dx > 0:
            gradient = float(dy)/dx
        else:
            gradient = -float(dy)/dx
    error = 0.0
    y = y0
    
    def my_range(a,b):
        if a < b:
            return range(a,b)
        if a > b:
            return range(a,b,-1)
        if a == b:
            return [a]
    
    #print (x0,x1)
    #print gradient
    #print my_range(x0,x1)
    for x in my_range(x0,x1):
        values.append((x,y))
        error += gradient
        while error > 0.5:
            y +=1
            if error > 1.5:
                values.append((x,y))
            error -=1
        while error < -0.5:
            y -=1
            if error < -1.5:
                values.append((x,y))
            error +=1
    values.append(destination)
    return values
        
    
class Ship(object):
    """Abstract class for space ships."""
    type_ = "error"
    offenseValue = 0
    defenseValue = 1
    marines = False
    colony = False
    missile = False
    service = False
        
    def __init__(self,faction,position):
        self.faction = faction
        self.position = position # Position in pc
        self.name = name.ship_name()
        
        self.path = []
        
        #self.destination = self.position # Target destination.
        self.orders = [] # List of orders.
        
        game.ships[position].append(self)
                
    @property
    def attack(self): 
        """Returns the attack value modified by tech levels."""
        return self.offenseValue
    @property
    def owner(self):
        return self.faction
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
        # Get the top speed to determine how many microticks there will be.
        def get_fastest(ships):
            fastest = 0
            for ship in sum(ships.values(),[]):
                ship.micro_movement = 0 # prepare them for the next step.
                ship.path = [] # Force repopulation in the next step.
                if ship.speed > fastest:
                    fastest = ship.speed
                    
            return fastest
        top_speed = get_fastest(ships)
        
        # Iterate over all ships and perform a single microtick/move. 
        def do_microtick(top_speed, ships):
            for ship in sum(ships.values(),[]):
                ship.micro_movement += ship.speed / top_speed
                if ship.micro_movement < 1:
                    continue # Skip the rest of this function if the ship isn't
                    # fast enough
                ship.micro_movement -= 1
                
                if ship.orders != []:
                    (order, target) = ship.orders[0]
                    if ship.path == []:
                        ship.path = get_path(ship.position, target)
                        ship.path.pop(0)
                    if order == "move to": # Do movement
                        ships[ship.position].remove(ship)
                        ship.position = ship.path.pop(0)
                        ships[ship.position].append(ship)
                        if target == ship.position:
                            ship.orders.pop(0) # If position = target, cycle to next order.
                    if order == "colony here": # Do colonisation
                        if game.galaxy.at(*target).owner != None:
                            log.debug("Planet at "+str(target)+" already colonised.")
                            ship.orders.pop(0) # If planet is already colonised
                            # then cycle to next order.
                            continue
                        if target == ship.position:
                            game.galaxy.at(*target).set_owner(ship.faction)
                            game.galaxy.at(*target).name = ship.name.split(' ',1)[1]
                            ships[ship.position].remove(ship)
                            continue
                        ship.orders.pop(0) # If all else fails, skip the order.
                            
                    
                    
            return ships
        for i in range (0, top_speed):
            ships = do_microtick(top_speed, ships)
        
        return ships
    
class Cruiser(Ship):
    """This class represents a Cruiser"""
    type_ = "Cruiser"
    offenseValue = 2
    defenseValue = 1
    marines = False
    colony = False
    service = False
    missile = False
    
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
