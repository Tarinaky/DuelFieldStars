"""
Utility methods for saving and loading game state.
"""
from model import game
import os
import json
from logging import getLogger
from model.faction import Faction
from model.planet import Planet
from model.ship import Cruiser, MarineTransport, ColonyTransport

log = getLogger(__name__)

version = 1.0
save_path = "~/.duelfieldstars/save/"

class SaveFormat(object):
    def __init__(self):
        pass
    
    def pack(self):
        self.state = {
                      'version': version,
                      'turn_count': game.turn_count,
                      'game_mode': game.game_mode,
                      'width': game.galaxy.width,
                      'height': game.galaxy.height
                      }
        self._pack_factions()
        self._pack_ships()
        self._pack_worlds()
        self._pack_events()
        return self.state
    
    def _pack_events(self):
        self.state["event log"] = []
        for faction in game.factions:
            self._pack_event_log(game.event_log.get_list(faction),self._faction_id(faction))
    
    def _pack_event_log(self,event_list,faction_id):
        for event in event_list:
            self.state["event log"].append(self._pack_event(event,faction_id))
    
    def _pack_event(self,event,faction_id):
        return {
                "description": event.description,
                "location": event.location,
                "emitter faction": self._faction_id(event.faction),
                "receiver faction": faction_id
                }
        
    def _unpack_events(self):
        for faction in game.factions:
            game.event_log.by_faction[faction] = []
        for event in self.state["event log"]:
            self._unpack_event(event)
    
    def _unpack_event(self,event):
        receiver = self._get_faction_by_id(event["receiver faction"])
        unpacked = game.event_log.Event(event["description"],
                             event["location"],
                             self._get_faction_by_id(event["emitter faction"]))
        
        game.event_log.by_faction[receiver].append(unpacked)
        
    
    def unpack(self,state):
        self.state = state
        game.turn_count = self.state["turn_count"]
        game.game_mode = self.state["game_mode"]
        game.galaxy.width = self.state["width"]
        game.galaxy.height = self.state["height"]
        # Reset data structures
        game.galaxy.planets.clear()
        game.factions = []
        game.ships = {}
        game.event_log.by_faction = {}
        for y in xrange(game.galaxy.height):
            for x in xrange(game.galaxy.width):
                game.ships[(x,y)] = []
        # Unpack.
        self._unpack_factions(self.state["factions"])
        self._unpack_worlds(self.state["worlds"])
        self._unpack_ships(self.state["ships"])
        self._unpack_events()
        
    def _unpack_ships(self,ships):
        for ship in ships:
            self._unpack_ship(ship)
        
    def _unpack_factions(self,factions):
        unpacked = []
        for faction in factions:
            unpacked.append(self._unpack_faction(faction))
        game.factions = unpacked
        
    def _unpack_faction(self,faction):
        unpacked = Faction()
        unpacked.unique_id = faction["ID"]
        unpacked.name = faction["name"]
        unpacked.flag = faction["flag"]
        unpacked.type = faction["type"]
        unpacked.rez = faction["rez"]
        unpacked.ready = faction["ready"]
        unpacked.tech = faction["tech"]
        unpacked.research = faction["research"]
        unpacked.special_choice = faction["special choice"]
        unpacked.colony_types = faction["colony types"]
        return unpacked
        
    def _unpack_worlds(self,worlds):
        for world in worlds:
            self._unpack_world(world)
        
    def _faction_id(self, faction):
        if faction is None:
            return 0
        if faction is False:
            return 0
        return faction.unique_id
    
    def _pack_faction(self, faction):
        self._faction_index += 1
        faction.unique_id = self._faction_index
        
        return {
                "ID": faction.unique_id,
                "name": faction.name,
                "flag": faction.flag,
                "type": faction.type,
                "rez": faction.rez,
                "ready": faction.ready,
                "tech": faction.tech,
                "research": faction.research,
                "special choice": faction.special_choice,
                "colony types": faction.colony_types
                }
        
    def _pack_factions(self):
        self._faction_index = 0
        self.state["factions"] = []
        for faction in game.factions:
            self.state["factions"].append(self._pack_faction(faction))
    
    def _unpack_ship(self, ship):
        position = ship["position"]
        faction = self._get_faction_by_id(ship["faction"])
        type = ship["type"]
        if type == "Cruiser":
            unpacked = Cruiser
        if type == "Marine Transport":
            unpacked = MarineTransport
        if type == "Colony Transport":
            unpacked = ColonyTransport
        unpacked = unpacked(faction,position)
        unpacked.name = ship["name"]
        unpacked.damaged = ship["damaged"]
        unpacked.orders = ship["orders"]
        
        game.ships[unpacked.position].append(unpacked)
    
    def _pack_ship(self, ship):
        return {
                "faction": self._faction_id(ship.faction),
                "type": ship.type_,
                "position": ship.position,
                "name": ship.name,
                "damaged": ship.damaged,
                "orders": ship.orders,
                }
        
    def _pack_ships(self):
        self.state["ships"] = [
                               self._pack_ship(ship)
                               for ship in sum(game.ships.values(), [])
                               ]
    
    def _unpack_world(self,world):
        position = world["position"]
        unpacked = Planet(*position)
        unpacked.owner = self._get_faction_by_id(world["faction"])
        unpacked.name = world["name"]
        homeworld = self._get_faction_by_id(world["homeworld"])
        if homeworld:
            unpacked.is_homeworld = homeworld
        else:
            unpacked.is_homeworld = False
        unpacked.baseValue = world["base value"]
        unpacked.currentValue = world["current value"]
        unpacked.realisedValue = world["realised value"]
        unpacked.marines = world["marines"]
        unpacked.sieged = world["sieged"]
        unpacked.blockaded = world["blockaded"]
        unpacked.improvementLevels = world["improvement levels"]
        unpacked.realisedImprovement = world["realised improvement"]
        unpacked.type_ = world["type"]
        
        game.galaxy.planets[unpacked.position] = unpacked
            
        
    def _get_faction_by_id(self,id):
        for faction in game.factions:
            if faction.unique_id == id:
                return faction
        return None
    
    def _pack_world(self, world):
        return {
                "faction": self._faction_id(world.owner),
                "name": world.name,
                "homeworld": self._faction_id(world.is_homeworld),
                "base value": world.baseValue,
                "current value": world.currentValue,
                "realised value": world.realisedValue,
                "marines": world.marines,
                "sieged": world.sieged,
                "blockaded": world.blockaded,
                "improvement levels": world.improvementLevels,
                "realised improvement": world.realisedImprovement,
                "type": world.type_,
                "position": world.position
                }
        
    def _pack_worlds(self):
        self.state["worlds"] = []
        for world in game.galaxy.planets.values():
            self.state["worlds"].append(self._pack_world(world))
            
def save(filename):
    path = os.path.expanduser(save_path + str(game.game_mode))
    if not os.path.exists(path):
        os.makedirs(path)
    
    path = path + "/" + filename
    
    data = SaveFormat()
    data = data.pack()
    
    f = open(path,"w")
    
    json.dump(data,f)
    log.debug("Game state written to "+path)
    
def load(folder,filename):
    path = os.path.expanduser(save_path + folder +"/" + filename)
    f = open(path,"r")
    data = json.load(f)
    SaveFormat().unpack(data)
    log.debug("Game state read from "+path)
    
if __name__ == "__main__":
    game.init()
    print game.factions[0].name
    save("test.json")
    load("None","test.json")
    print game.factions[0].name