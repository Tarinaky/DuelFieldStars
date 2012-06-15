"""
Module to contain globals. 
Since only one game can be played at once a singleton seems appropriate.
"""
import logging
import pygame

from galaxy import Galaxy
import ship
import faction

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
    faction.PLAYERFACTION = factions[0]
    
    for y in range(galaxy.height):
        for x in range(galaxy.width):
            ships[x,y] = []

log = logging.getLogger(__name__)

def _do_end_of_turn():
    """End of turn processing."""
    global turn_count, ships
    log.debug("End of turn "+str(turn_count)+".")
    turn_count += 1
    
    for faction in factions:
        faction.tick()
    for planet in galaxy.planets.values():
        planet.tick()
    ships = ship.process_ship_turn(ships)
    
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
    
