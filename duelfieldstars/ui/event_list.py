"""
Displays all events witnessed during the last
resolution phase.
"""
from model import game
from ui.ui_abstract.widget import Widget
from color import COLORS
from ui.ui_abstract.text import Text
from ui import texture_cache

class EventList(Widget):
    
    def __init__(self,rect):
        super(EventList,self).__init__()
        
        self.scroll = 0
        self.events = game.event_log.get_list(game.factions[0])
        
        self.scrollUpRect = None
        self.scrollDownRect = None
        
    def on_draw(self):
        self.surface.fill(COLORS["black"])
        
        dy = y = 0
        
        for event in self.events:
            dy = 0
            texture = texture_cache.text(None,12,COLORS["white"],
                                         event.description)
            self.surface.blit(texture, (0,dy))
            dy += texture.get_height()