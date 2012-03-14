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
        return False
        
    def _keyboard(self, event):
        if self.on_keyboard(event):
            return True
        return False
    
    def _tick(self,deltaTime):
        self.on_tick(deltaTime)
        
    def on_tick(self, deltaTime):
        """Is called for each frame. deltaTime contains the time taken since the last frame, allowing
        for integration."""
    
    def on_mouse(self,event):
        """Handles mouse events for this widget. Overload if you want to respond to mouse events."""
        return False
    
    def on_keyboard(self, event):
        """Handles keyboard events for this widget. Overload if you want to respond to key events."""
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

