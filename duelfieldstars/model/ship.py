import name

import game
import logging
import math
import random
from model.faction import Faction
from model import event_log

log = logging.getLogger(__name__)

sensor_map = (None,{}) # ( faction, map ) tuple.
# Faction is the current faction being controlled.
def get_euclidian_range(x0,y0,x1,y1):
    """Return the euclidian distance between two points.
    Note, this does not use pythagorean threorum and a
    diagonal is simple worth 1 (not sqrt(2))."""
    dx = dy = 0
    dx = abs(x0-x1)
    dy = abs(y0-y1)
    if dx > dy:
        return dx
    else:
        return dy
    
sensor_map = (None, {})
sensor_map_dirty = True

def get_sensor_value(faction, (x,y), cache = True):
    global sensor_map, sensor_map_dirty
    (map_faction, map) = sensor_map
    if map_faction == faction and cache and not sensor_map_dirty: # Does the map need updating?
        return map[(x,y)]
    # Build a list of 'sensors'.
    sensor_map_dirty = False
    sensors = [] # A list of (position, level) tuples.
    for ship in sum(game.ships.values(),[]): # Ships
        if ship.faction == faction:
            sensors.append((ship.position,ship.sensor))
    for world in game.galaxy.planets.values():
        if world.owner == faction: # Worlds
            sensors.append((world.position, faction.tech["Sensor Technology"]))
            
    
    # If not cached, just get the value at the interesting location
    def find_closest_sensor(x,y):
        i = None
        for (position,sensor) in sensors:
            if i == None:
                i = sensor - get_euclidian_range(x,y,*position)
            else:
                new = sensor - get_euclidian_range(x,y,*position)
                if new > i:
                    i = new
        return i
    if not cache:
        return find_closest_sensor(x,y)
    else:
        def build_map():
            for x in xrange (game.galaxy.width):
                for y in xrange (game.galaxy.height):
                    i = find_closest_sensor(x,y)
                    map[(x,y)] = i
        build_map()
        sensor_map = (faction,map)
        return map[(x,y)]
                
            
        
    
    

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
    defenseValue = 2
    max_kill_chance = 0.5
    marines = False
    colony = False
    missile = False
    service = False
        
    def __init__(self,faction,position):
        self.faction = faction
        self.position = position # Position in pc
        self.name = name.ship_name()
        
        self.path = []
        
        self.damaged = False # True if the ship is damaged.
        
        #self.destination = self.position # Target destination.
        self.orders = [] # List of orders.
        
        game.ships[position].append(self)
                
    @property
    def attack(self): 
        """Returns the attack value modified by tech levels."""
        return round(self.offenseValue * math.sqrt(self.faction.tech["Space Weapons Technology"]),2)
    @property
    def owner(self):
        return self.faction
    @property
    def defence(self): 
        """Returns the defence value modified by tech levels."""
        return round(self.defenseValue * math.sqrt(self.faction.tech["Space Defence Technology"]),2)
    @property
    def speed(self): 
        """Speed in pc, modified by tech levels."""
        return 2 + self.faction.tech["Engine Technology"]
    
    @property
    def sensor(self):
        """Sensor range."""
        return self.faction.tech["Sensor Technology"]
    @property
    def stealth(self):
        """Stealth capability"""
        return self.faction.tech["Stealth Technology"]
    
    def invisible(self,scanning_faction,cache=True):
        """Can this ship be seen by scanning_faction?
        Cache indicates whether to optimise this search with
        a map."""
        if scanning_faction == self.faction:
            return False # You can always see yourself.
        sensor_value = get_sensor_value(scanning_faction,self.position,cache)
        if self.stealth > sensor_value + 1:
            return True
        return False
    
    @property
    def ground_combat_value(self):
        if self.marines:
            return 2 * math.sqrt(self.faction.tech["Ground Combat Technology"])
        return 0
    
    def tick(self):
        """Process a turn."""
        return
    
    def beligerant(self):
        """Returns true if the ship is not trying to 'flee'.
        This is determined by the top order in the queue
        being "move to" or some similar instruction.
        Bombard, Assault and similar 'beligerant' actions cannot
        be taken if enemy ships are in system.
        """
        if self.orders == [] and self.attack >0:
            return True # Ships with no orders, and positive attack
        # are beligerant.
        
        if self.attack == 0:
            return False # Noncombatants are never beligerant.
        (order,_) = self.orders[0]
        if order == "move to":
            return False # Moving ships are 'evasive'.
    

def check_for_combat(x, y):
    ships = game.ships[(x,y)]
    factions = []
    for ship in ships:
        if ship.faction in factions:
            continue
        factions.append(ship.faction)
        if len(factions) > 1:
            return True # There will be a fight!
    return False
             
        
def resolve_combat(x, y):
    fleets = {} # Group ships by their faction.
    ships = game.ships[(x,y)]
    for ship in ships:
        ship.end_of_turn = True # Fighting ships take no
        # other action.
        if ship.faction in fleets.keys():
            fleets[ship.faction].append(ship)
        else:
            fleets[ship.faction] = [ship]
    attack_value = {} # Calculate per-fleet attack value
    defence_value = {} # Calculate per-fleet defence
    
    destroyed_ships = [] # Place ships to be killed here.
    damaged_ships = []
    
    for (faction,fleet) in fleets.items(): # Calculate per-fleet values
        fleet_attack = 0
        fleet_defence = 0
        for ship in fleet:
            fleet_attack += ship.attack
            fleet_defence += ship.defence
        attack_value[faction] = fleet_attack
        defence_value[faction] = fleet_defence
    
    for attacker in fleets.keys(): # Resolve your attack.
        for defender in fleets.keys():
            if attacker == defender:
                continue # Don't attack yourself.
            
            kill_chance = attack_value[attacker] / defence_value[faction]
            
            for ship in fleets[defender]:
                hits = 0
                a = kill_chance
                while a > 0:
                    if a > ship.max_kill_chance:
                        if random.random() < ship.max_kill_chance: # score a hit
                            hits += 1
                    else:
                        if random.random() < a: # score a hit
                            hits +=1
                    a -= ship.max_kill_chance
                
                log.debug(str(hits)+" hits scored on "+ship.name+" ("+ship.faction.name+")")
                for _ in range (hits):
                    if random.random() < 0.5: # Destroy
                        destroyed_ships.append(ship)
                        log.debug("----She is destroyed.")
                    else: # Damage
                        ship.damaged = True
                        damaged_ships.append(ship)
                        log.debug("----She is damaged.")
                        
    # Report event
    string = "Battle at "+str((x,y))
    event_log.add(event_log.Event(string, (x,y), None))
    for ship in destroyed_ships: # Remove destroyed ships from play.
        try:
            game.ships[ship.position].remove(ship)
            event_log.add(event_log.Event(ship.name+" destroyed.", (x,y), ship.faction))
        except:
            pass
    # Report event
    #string = str(len(destroyed_ships))+" ships destroyed, "+str(len(damaged_ships))+" ships damaged by fighting."
    #event_log.add(event_log.Event(string, (x,y)))
                    
def resolve_ground_attack(ship):
    ship.end_of_turn = True # Attacking ends your movement.
    (x,y) = ship.position
    planet = game.galaxy.at(x,y)
    planet.sieged = True
    attacker = ship.ground_combat_value
    defender = planet.ground_combat_value
    
    kill_chance = float(attacker) / defender
    
    def hit_scored(attacker,planet):
        if attacker == planet.owner:
            return # Don't kill your own marines!
        log.debug("Defender on "+planet.name+" died gallantly.")
        planet.marines -= 1
        planet.realisedValue -= 1
        if planet.marines < 1:
            log.debug("Planet has been captured!")
            planet.owner = attacker
            planet.marines = 1
    while kill_chance > 0:
        if kill_chance > ship.max_kill_chance:
            if random.random() < ship.max_kill_chance:
                hit_scored(ship.faction, planet)
        else:
            if random.random() < kill_chance:
                hit_scored(ship.faction, planet)
        kill_chance -= ship.max_kill_chance
    
    if attacker == planet.owner:
        string = "Planet "+planet.name+" was captured by marines."
        faction = ship.faction
    else:
        string = "Garrison on "+planet.name+" resisted enemy marines."
        faction = planet.owner
    event_log.add(event_log.Event(string, planet.position, faction))
                
    
    
                    
    
        



def bombard(ship):
    (x,y) = ship.position
    planet = game.galaxy.at(x,y)
    
    ship.end_of_turn = True # Bombarding ends your turn.
    
    if planet.owner != None:
        defence = math.sqrt(planet.owner.tech["Space Defence Technology"])
    else:
        defence = 1
    
    damage = int(ship.attack / defence)
    
    planet.baseValue -= damage # Deal damage.
    if planet.baseValue < 0:
        planet.baseValue = 0
    planet.currentValue -= 2*damage
    if planet.currentValue < 1:
        planet.currentValue = 1
    planet.realisedValue -= 5*damage
    if planet.realisedValue <0:
        planet.realisedValue = 0
    
    log.debug("Planet "+planet.name+" ("+str(planet.position)+") took "+str(damage)+" damage.")
    
    if random.randint(0,100) < damage:
        planet.type = random.choice(['A','B','C','D','E'])
        log.debug("----An ecological disaster caused it to change to type "+planet.type+" permanently.")
    
    string = planet.name+" was bombarded from space."
    event_log.add(event_log.Event(string, planet.position, ship.owner))


def process_ship_turn(ships):
        """Takes a list of ships and iterates over them to produce the new ship state."""
        # Get the top speed to determine how many microticks there will be.
        def get_fastest(ships):
            fastest = 0
            for ship in sum(ships.values(),[]):
                ship.micro_movement = 0 # prepare them for the next step.
                ship.end_of_turn = False
                ship.path = [] # Force repopulation in the next step.
                if ship.speed > fastest:
                    fastest = ship.speed
                    
            return fastest
        top_speed = float(get_fastest(ships))
        
        # Iterate over all ships and perform a single microtick/move. 
        def do_microtick(top_speed, ships):
            for ship in sum(ships.values(),[]):
                ship.micro_movement += ship.speed / top_speed
                if ship.micro_movement < 1:
                    continue # Skip the rest of this function if the ship isn't
                    # fast enough
                if ship.end_of_turn:
                    continue # Skip the rest of this function if
                    # the ship engaged in combat.
                ship.micro_movement -= 1
                
                # Check tactics and combat
                (x,y) = ship.position
                if check_for_combat(x,y):
                    if not ship.beligerant:
                        pass # Ships with certain orders escape.
                    else:
                        resolve_combat(x,y)
                        continue # Forfeit rest of turn.
                
                # Perform orders
                if ship.orders != []:
                    try:
                        (order, target) = ship.orders[0]
                    except ValueError:
                        (order) = ship.orders[0]
                        target = None
                    if order == "scrap": # Scrap ship.
                        ships[ship.position].remove(ship)
                        ship.faction.rez += 2 # Refund part of the cost, adjusted for upkeep taken.
                        continue
                    if order == "move to": # Do movement
                        if ship.path == []:
                            ship.path = get_path(ship.position, target)
                            ship.path.pop(0)
                    
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
                        def colonisable(ship,target):
                            return game.galaxy.at(*target).type_ in ship.owner.colony_types
                        if target == ship.position and colonisable(ship,target):
                            game.galaxy.at(*target).set_owner(ship.faction)
                            game.galaxy.at(*target).realisedValue = 1
                            game.galaxy.at(*target).name = ship.name.split(' ',1)[1]
                            ships[ship.position].remove(ship)
                            string = "Planet at "+str(target)+" colonised."
                            event_log.add(event_log.Event(string,target,ship.faction))
                            continue
                        ship.orders.pop(0) # If all else fails, skip the order.
                    if order == "assault planet": # Space Marine attack
                        if game.galaxy.at(*target).realisedValue == 0:
                            log.debug("Planet at "+str(target)+" seems to have been glassed.")
                            ship.orders.pop(0) # If colony destroyed then cycle to
                            # next order.
                            continue
                        resolve_ground_attack(ship)
                        if game.galaxy.at(*target).owner == ship.faction: # Were we successful?
                            ship.orders.pop(0) # End the attack once we have won.
                    if order == "bombard planet": # Ortillery attack
                        bombard(ship)
                        if game.galaxy.at(*target).baseValue <= 0: # Planet glassed.
                            ship.orders.pop(0) # End the attack once the planet is dead.
                            continue
                        
                            
                    
                    
            return ships
        for i in range (0, int(top_speed)):
            ships = do_microtick(top_speed, ships)
        
        return ships
    
class Cruiser(Ship):
    """This class represents a Cruiser"""
    type_ = "Cruiser"
    offenseValue = 2
    defenseValue = 2
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
    defenseValue = 2
    marines = True
    colony = False
    
    def __init__(self,faction,position):
        super(MarineTransport,self).__init__(faction,position)
        
class ColonyTransport(Ship):
    """This class represents a colony ship."""
    type_ = "Colony Transport"
    offenseValue = 0
    defenseValue = 2
    marines = False
    colony = True
    
    def __init__(self,faction,position):
        super(ColonyTransport,self).__init__(faction,position)

if __name__ == '__main__': # Test combat resolution.
    print "Test combat resolution."
    logging.basicConfig(level=logging.DEBUG)
    game.init()
    Cruiser(Faction(),(0,0))
    Cruiser(Faction(),(0,0))
    resolve_combat(0,0)
