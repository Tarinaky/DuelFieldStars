"""List of items that can be built at a world."""
from ui.ui_abstract.menu import Menu
import pygame
from ui.ui_abstract.text import Text
from color import COLORS
from model import game

class BuildMenu(Menu):
    
    def __init__(self,rect,destination):
        """Destination is an (x,y) tuple addressing the
        world the item will be built at."""
        super(BuildMenu,self).__init__(rect)
        
        self.destination = destination
        
        font = pygame.font.Font(pygame.font.get_default_font(), 12)
        dy = 0
        dx = 14
        
        "Label"
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["white"],
                      "Build at "+game.galaxy.planets[destination].name)
        self.add_option(widget,None)
        dy += widget.height
        
        dx = 28
        
        "Cruiser"
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "Cruiser [2/1]")
        self.add_option(widget, None)
        dy += widget.height
        
        "Marine Transport"
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "Marine Transport [1/1 Ground 1]")
        self.add_option(widget, None)
        dy += widget.height
        
        "Colony Transport"
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "Colony Transport [0/1]")
        self.add_option(widget, None)
        dy += widget.height
        
        
    def on_draw(self):
        "Calculate the size of the surface needed."
        width = 0
        height = 0
        for (widget,_,_) in self.options:
            if (widget.width+28) > width:
                width = widget.width + 28
            height += widget.height
            
        self.surface = pygame.Surface((width,height))
        self.rect.width = self.surface.get_width()
        self.rect.height = self.surface.get_height() 
        self.surface.fill(COLORS["darkGray"])
        