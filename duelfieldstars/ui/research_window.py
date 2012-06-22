"""
Control research for your faction.
"""
from ui.ui_abstract.window import Window
import logging
import pygame
from ui.ui_abstract.widget import Widget
from ui import texture_cache
from color import COLORS
from model import tech

log = logging.getLogger(__name__)

class ResearchWindow(Window):
    def __init__(self, faction):
        super(ResearchWindow, self).__init__()
        
        log.debug("Openning research window for "+faction.name)
        
        self.faction = faction
        
        self.tech_items = [] # A list of (rect, technology) 2-tuples.
        self.special_choice_rect = [] # A list of (rect, technology) 2-tuples.
        self.selected = faction.research # Load and persist research goals.
        
        self.quitrect = pygame.Rect((0,0,0,0))
        
        self.error = ""
        
        
    def on_draw(self):
        self.tech_items = [] # List unlocked research items.
        self.rects = []
        dy = 0

        self.surface.fill((0x0,0x0,0x0))
        
        # Finance for the faction.
        texture = texture_cache.text(None,16, COLORS["blue"],
                               "    "+str(self.faction.rez)+" rez available. It will cost "+str((len(self.selected)+1)**2)+" rez for another technology this turn.")
        self.surface.blit(texture,(0,dy+texture.get_height()))
        dx = texture.get_width() + 4
        
        # Back button
        texture = texture_cache.text(None, 20, COLORS["red"],
                                     "Back to Viewport")
        top_right = (self.width - texture.get_width(), 0)
        self.surface.blit(texture,top_right)
        
        self.quitrect = pygame.Rect(self.width-texture.get_width(),0, texture.get_width(), texture.get_height())
        
        
        dy += texture.get_height()*2
        
        texture = texture_cache.text(None, 16, COLORS["white"],
                                         "Known tech fields...")
        self.surface.blit(texture, (0,dy))
        dy += texture.get_height()
        for technology in self.faction.tech.keys():
            texture = texture_cache.text(None, 16, COLORS["light blue"], 
                                         "    "+technology)
            self.surface.blit(texture, (0,dy))
            dx = texture.get_width()
            
            # Is a choice needed from the player?
            if tech.by_name[technology].check_special_func != None:
                if tech.by_name[technology].check_special_func(1+self.faction.tech[technology]):
                    if technology in self.faction.special_choice.keys():
                        texture = texture_cache.text(None, 16, COLORS["blue"],
                                                     " "+self.faction.special_choice[technology])
                    else:
                        texture = texture_cache.text(None, 16, COLORS["blue"],
                                                     " (a choice must be made to advance)")
                    self.surface.blit(texture, (dx,dy))
                    self.special_choice_rect.append((pygame.Rect(0,dy,dx,texture.get_height()), technology))
                    dy += texture.get_height() +2
                    continue
            
            # Check for max tech level.
            if tech.by_name[technology].max_level == self.faction.tech[technology]:
                texture = texture_cache.text(None, 16, COLORS["gray"],
                                             " MAX")
                self.surface.blit(texture, (dx,dy))
                dy += texture.get_height() +2
                continue
            
            
            texture = texture_cache.text(None, 16, COLORS["white"],
                                             " "+str(self.faction.tech[technology]))
            self.surface.blit(texture, (dx,dy))
            dx += texture.get_width()
            
            if technology in self.selected:
                texture = texture_cache.text(None, 16, COLORS["light blue"],
                                             " -> "+str(self.faction.tech[technology]+1) )
                self.surface.blit(texture, (dx,dy))
                dx += texture.get_width()
                
            
            self.tech_items.append((pygame.Rect(0,dy,dx,texture.get_height()), technology))
            
            
                
            dy += texture.get_height() +2
            
        texture = texture_cache.text(None, 16, COLORS["red"],
                                     self.error)
        self.surface.blit(texture, (0,dy))
        
    def on_mouse(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.quitrect.collidepoint((event.pos)):
                self.runControl = False
                return True
            
            for (rect,technology) in self.special_choice_rect:
                ((mouse_x, mouse_y), button) = (event.pos, event.button)
                if rect.colliderect(pygame.Rect(mouse_x, mouse_y, 0,0)) and button == 1:
                    if technology == "Colony Technology":
                        pass # Display options for Colony Tech.
            
            for (rect, technology) in self.tech_items:
                ((mouse_x, mouse_y), button) = (event.pos, event.button)
                if rect.colliderect(pygame.Rect(mouse_x, mouse_y,0,0)) and button == 1:
                    if technology in self.selected:
                        self.faction.rez += (len(self.selected))**2
                        self.selected.remove(technology)
                        self.error=""
                    elif self.faction.rez >= (len(self.selected)+1)**2:
                        self.faction.rez -= (len(self.selected)+1)**2
                        self.selected.append(technology)
                        self.error=""
                    else:
                        self.error = "Insufficient rez."
                    return True
        self.faction.research = self.selected # Save research goals.
        
        
         
        
        
    
    