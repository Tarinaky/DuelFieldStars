"""
Displays all events witnessed during the last
resolution phase.
"""
from model import game
from ui.ui_abstract.widget import Widget
from color import COLORS
from ui.ui_abstract.text import Text
from ui import texture_cache
import pygame

class EventList(Widget):
    
    def __init__(self,rect):
        super(EventList,self).__init__(rect)
        
        self.scroll = 0
        self.events = game.event_log.get_list(game.factions[0])
        
        self.scrollUpRect = None
        self.scrollDownRect = None
        
        self.tile_height = 1
        
    def on_mouse(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Jump to target
            (x,y) = event.pos
            (x,y) = (x-self.x0, y-self.y0)
            (x,y) = (x, y/self.tile_height)
            try:
                (x,y) = self.events[y].location
            except:
                return False
            event = pygame.event.Event(pygame.USEREVENT, action="go to", goto=(x,y))
            pygame.event.post(event)
        
        
    def on_draw(self):
        self.surface.fill(COLORS["black"])
        
        dy = y = 0
        
        for event in self.events:
            dy = 0
            texture = texture_cache.text(None,16,COLORS["white"],
                                         event.description)
            self.surface.blit(texture, (0,y+dy))
            dy += texture.get_height()
            
            # Save dy.
            self.tile_height = dy
            y += dy