"""
Message to be displayed as a menu to indicate to the user
that they do not have enough 'Rez' to complete an action.
"""
import pygame
from ui.ui_abstract.text import Text
from color import COLORS
from ui.ui_abstract.menu import Menu

class InsufficientRezMenu(Menu):
    message = "Insufficient Rez"
    def __init__(self, rect):
        super(InsufficientRezMenu,self).__init__(rect)
        
        font = pygame.font.Font(pygame.font.get_default_font(),12)
        widget = Text(pygame.Rect(0,0,0,0), font, COLORS["red"],
                      "    "+self.message+"    "
                      )
        self.add_option(widget, None)
    
    def on_draw(self):
        "Calculate the size of the surface needed."
        width = 0
        height = 0
        for (widget,_,_) in self.options:
            if (widget.width) > width:
                width = widget.width
            height += widget.height
            
        self.surface = pygame.Surface((width,height))
        self.rect.width = self.surface.get_width()
        self.rect.height = self.surface.get_height() 
        self.surface.fill(COLORS["darkGray"])