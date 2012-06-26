"""
Each faction has a list of events that they have seen during
the last resolution phase.
"""
from model import game

by_faction = {}

def reset():
    """Reset the log before the resolution phase."""
    global by_faction
    by_faction = {}
    for faction in game.factions:
        by_faction[faction] = []
        
def add(event):
    """Add an event of type Event to any faction who can see the event."""
    for faction in by_faction.keys():
        by_faction[faction].append(event)
        
def get_list(faction):
    """Get a particular faction's 'list'."""
    return by_faction[faction]


class Event(object):
    def __init__(self, title, description, location):
        self.title = title
        self.description = description
        self.location = location

        