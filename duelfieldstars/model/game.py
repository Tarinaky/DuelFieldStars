"""
Module to contain globals. 
Since only one game can be played at once a singleton seems appropriate.
"""
import logging
import pygame

from galaxy import Galaxy
import ship

factions = []
ships = {}
galaxy = Galaxy()
turn_count = 1

def init():
    global galaxy, factions, ships, turn_count
    factions = []
    ships = {}
    galaxy = Galaxy()
    turn_count = 1

log = logging.getLogger(__name__)

def _do_end_of_turn():
    """End of turn processing."""
    global turn_count
    log.debug("End of turn "+str(turn_count)+".")
    turn_count += 1
    
    for planet in galaxy.planets.values():
        planet.tick()
    for faction in factions:
        faction.tick()
    ship.ShipTurnProcessor(sum(ships.values(),[]))
    
    event = pygame.event.Event(pygame.USEREVENT, action="End of Turn")
    pygame.event.post(event)


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
    