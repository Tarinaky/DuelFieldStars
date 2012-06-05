"""
Module to contain globals. 
Since only one game can be played at once a singleton seems appropriate.
"""
import logging

from galaxy import Galaxy
import ship

factions = []
ships = {}
galaxy = Galaxy()

def init():
    global galaxy, factions, ships
    factions = []
    ships = {}
    galaxy = Galaxy()

log = logging.getLogger(__name__)

def _do_end_of_turn():
    """End of turn processing."""
    log.debug("End of turn.")
    
    for planet in galaxy.planets.values():
        planet.tick()
    for faction in factions:
        faction.tick()
    ship.ShipTurnProcessor(sum(ships.values(),[]))


def end_of_turn(faction):
    """
    Mark a given faction's turn as complete.
    When all factions are marked as complete process the turn and resume.
    """
    faction.ready = True
    log.debug(faction.name+" marked ready.")
    
    def check():
        for faction in factions:
            if faction.ready == False:
                return False
            else:
                return True
            
    if check():
        _do_end_of_turn()
        for faction in factions:
            faction.ready = False
    return
    