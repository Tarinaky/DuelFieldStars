"""
Utility methods for writing game state and reading
it back.
"""

import jsonpickle
from model import game
from logging import getLogger
import os

log = getLogger(__name__)

save_path = "~/.duelfieldstars/save/"

class SaveFormat(object):
    def __init__(self):
        self.factions = game.factions
        self.ships = game.ships
        self.galaxy = game.galaxy
        self.turn_count = game.turn_count
        self.game_mode = game.game_mode

def pack():
    
    return SaveFormat()
            
def save(filename):
    # Check if dir exists
    if not os.path.exists(os.path.expanduser(save_path+game.game_mode)):
        os.makedirs(os.path.expanduser(save_path+game.game_mode))
    
    
    filename = os.path.expanduser(save_path + game.game_mode +"/" +filename)
    data = pack()
    data = jsonpickle.encode(data)
    f = open(filename,"w")
    f.write(data)
    log.debug("State written to "+filename)
    
def unpack(data):
    game.factions = data.factions
    game.ships = data.ships
    game.galaxy = data.galaxy
    game.turn_count = data.turn_count
    game.game_mode = data.game_mode
    
def load(filename):
    filename = os.path.expanduser(save_path + filename)
    f = open(filename,"r")
    data = f.read()
    data = jsonpickle.decode(data)
    unpack(data)
    log.debug("State read from "+filename)
    
if __name__ == '__main__':
    os.chdir("..")

    
    game.init()
    print game.factions[0].name
    save("test.json")
    load("test.json")
    print game.factions[0].name