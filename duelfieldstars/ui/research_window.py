"""
Control research for your faction.
"""
from ui.ui_abstract.window import Window
import logging
import pygame
from ui.ui_abstract.widget import Widget
from ui import texture_cache
from color import COLORS

log = logging.getLogger(__name__)

class ResearchWindow(Window):
    def __init__(self, faction):
        super(ResearchWindow, self).__init__()
        
        log.debug("Openning research window for "+faction.name)
        
        self.faction = faction
        
        self.tech_items = []
        
        
    def on_draw(self):
        self.tech_items = []
        # List unlocked research items.
        self.surface.fill((0x0,0x0,0x0))
        
        
        def draw_research_items():
            texture = texture_cache.text(None, 16, COLORS["white"],
                                         "Known tech fields...")
            self.surface.blit(texture, (0,0))
            dy = texture.get_height()
            for technology in self.faction.tech.keys():
                texture = texture_cache.text(None, 16, COLORS["light blue"], 
                                             "    "+technology)
                self.surface.blit(texture, (0,dy))
                dx = texture.get_width()
                texture = texture_cache.text(None, 16, COLORS["white"],
                                             " "+str(self.faction.tech[technology]))
                self.surface.blit(texture, (dx,dy))
                dx += texture.get_width()
                self.tech_items.append(pygame.Rect(0,dy,dx,texture.get_height()))
                
                dy += texture.get_height() +2
        draw_research_items()
        
        
        
         
        
        
    
    