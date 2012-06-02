"""
Module to contain globals. 
Since only one game can be played at once a singleton seems appropriate.
"""
import logging

galaxy = None
factions = None
ships = None

log = logging.getLogger(__name__)

def do_end_of_turn():
    """End of turn processing."""
    log.debug("End of turn.")


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
        do_end_of_turn()
        for faction in factions:
            faction.ready = False
    return
    