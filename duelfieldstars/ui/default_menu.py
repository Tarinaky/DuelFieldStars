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
        
        # Check that this surface is completely within the display,
        # else nudge it
        def check_rect_in_display(rect):
            (x0,y0,w,h) = (rect.left, rect.top, rect.width, rect.height)
            display_width = pygame.display.get_surface().get_width()
            display_height = pygame.display.get_surface().get_height()
            
            if x0 < 0:
                x0 = 0
            if y0 < 0:
                y0 = 0
            if x0+w > display_width:
                x0 = display_width - w
            if y0+h > display_height:
                y0 = display_height - h
            
            (rect.left, rect.top, rect.width, rect.height) = (x0,y0,w,h)
            return rect
        
        self.rect = check_rect_in_display(self.rect)
                
            