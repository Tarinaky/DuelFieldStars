"""
Each faction has a list of events that they have seen during
the last resolution phase.
"""
import logging
import model

log = logging.getLogger(__name__)

by_faction = {}


def reset():
    """Reset the log before the resolution phase."""
    from model import game
    global by_faction
    by_faction = {}
    for faction in game.factions:
        by_faction[faction] = []
        
def add(event):
    """Add an event of type Event to any faction who can see the event."""
    for faction in by_faction.keys():
        location = event.location
        if location == None:
            sensing = 1
        else:
            sensing = model.ship.get_sensor_value(faction, location, False)
        if sensing > 0:
            by_faction[faction].append(event)
            log.debug(event.description+" "+str(event.location)+" "+str(event.faction))
        
    
        
def get_list(faction):
    """Get a particular faction's 'list'."""
    return by_faction[faction]


class Event(object):
    def __init__(self, description, location, faction):
        self.description = description
        self.location = location
        self.faction = faction

        