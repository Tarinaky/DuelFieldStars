import pygame
import logging

log = logging.getLogger(__name__)

class Widget(object):
    """Abstract class defining a region of the UI. 
    You must define on_draw in your specialisations."""
    def __init__(self,rect):
        self.rect = rect
        self.surface = pygame.Surface((rect.width,rect.height))
        self.changed = True
        
    def _draw(self):
        """Calls on_draw if this widget needs redrawing."""
        if self.changed:
            self.on_draw()
            self.changed = False
        return
    
    def _mouse(self,event):
        if self.on_mouse(event):
            return True
        log.debug("Unknown event "+str(event) )
    
    def on_mouse(self,event):
        """Handles mouse events for this widget. Overload if you want to respond to mouse events."""
        return False
    
    def update(self):
        """Mark this widget as 'dirty' and in need of redrawing."""
        self.changed = True
        return
    
    @property
    def width(self):
        return self.rect.width
    @property
    def height(self):
        return self.rect.height
    @property
    def x0(self):
        return self.rect.left
    @property
    def y0(self):
        return self.rect.top

