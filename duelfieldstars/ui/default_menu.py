"""
Implementation of Menu on_draw. Inherit this instead of the
abstract one.
"""
import pygame
from color import COLORS
from ui.ui_abstract.menu import Menu

class DefaultMenu(Menu):
    
    def __init__(self, rect):
        super(DefaultMenu,self).__init__(rect)
    
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