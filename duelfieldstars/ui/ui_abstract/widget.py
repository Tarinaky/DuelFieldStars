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
        self.alwaysDirty = False
        
        self._event_junction = {}
        
    def _draw(self):
        """Calls on_draw if this widget needs redrawing."""
        if self.changed or self.alwaysDirty:
            self.on_draw()
            self.changed = False
        return
    
    def _mouse(self,event):
        if (event.type == pygame.MOUSEBUTTONUP or event.type == pygame.MOUSEBUTTONDOWN):
            if (event.type, event.button) in self._event_junction:
                (function,args) = self._event_junction[(event.type, event.button)]
                function(*args)
                return True
        if self.on_mouse(event):
            return True
        return False
        
    def _keyboard(self, event):
        if (event.type, event.key, event.mod) in self._event_junction:
            (handler,args) = self._event_junction[(event.type,event.key,event.mod)]
            handler(*args)
            return True 
        if (event.type, event.key, None) in self._event_junction:
            (handler,args) = self._event_junction[(event.type,event.key,None)]
            handler(*args)
            return True
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
    
    def add_keyboard_handler(self, function, type_, key, modifier=None, *args):
        """Use this method to register a function to be called when a particular keyboard event is received."""
        self._event_junction[(type_, key, modifier)] = (function,args) 
    def add_mouse_handler(self, function, type_, button, *args):
        """Use this method to register a function to be called when a particular mouse button event is received."""
        self._event_junction[(type_, button)] = (function,args)
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
        (x0,_,_,_) = self.rect
        return x0
    @property
    def y0(self):
        (_,y0,_,_) = self.rect
        return y0

