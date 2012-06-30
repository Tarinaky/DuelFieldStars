"""
Utility methods for writing game state and reading
it back.
"""

import jsonpickle
from model import game
from logging import getLogger
import os

log = getLogger(__name__)

class SaveFormat(object):
    def __init__(self):
        self.factions = game.factions
        self.ships = game.ships
        self.galaxy = game.galaxy

def pack():
    
    return SaveFormat()
            
def save(filename):
    data = pack()
    data = jsonpickle.encode(data)
    f = open(filename,"w")
    f.write(data)
    log.debug("State written to "+filename)
    
def unpack(data):
    game.factions = data.factions
    game.ships = data.ships
    game.galaxy = data.galaxy
    
def load(filename):
    f = open(filename,"r")
    data = f.read()
    data = jsonpickle.decode(data)
    unpack(data)
    log.debug("State read from "+filename)
    
if __name__ == '__main__':
    os.chdir("..")
    # Check folder exists
    if not os.path.exists("save"):
        os.mkdir("save")
    
    game.init()
    print game.factions[0].name
    save("save/test.json")
    load("save/test.json")
    print game.factions[0].name