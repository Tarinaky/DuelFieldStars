import pygame
import logging

log = logging.getLogger(__name__)

class Window(object):
    """
    Abstract class defining a window with internal widget manager to control the pygame display in an OO way.
    Your specialisations must define on_draw.
    """
    def __init__(self):
        super(Window,self).__init__()
        
        # List of widgets currently open in this window, sorted from bg to fg.
        self.widgets = []
        
    def run(self):
        """Entry point into the class. Executes the window's main loop."""
        self.runControl = True
        while self.runControl == True:
            self._tick()
    
    def _tick(self):
        """Executes a single 'tick' or frame."""
        for event in pygame.event.get(): # Run event handler
            if self._event(event) == False:
                log.debug("Unknown event "+str(event) )
        "TODO: game rules"
        self._draw() # Draw a frame.
        
    def _event(self,event):
        """Handles all events received by this window or dispatches them to an overridable 'on_event(e)'.
        Returns True if the event is handled."""
        if self.on_event(event):
            return True
        if event.type == pygame.QUIT:
            self.runControl = False
            return True
        if (event.type == pygame.MOUSEMOTION or event.type == pygame.MOUSEBUTTONDOWN 
            or event.type == pygame.MOUSEBUTTONUP):
            return self._mouse(event)
        "TODO: Keyboard events"
        return False
    
    def _mouse(self,event):
        """Dispatches mouse events to widgets.
        Returns True if the event is handled, else false."""
        if self.on_mouse(event):
            return True
        
        for widget in reversed(self.widgets):
            if widget.rect.collidepoint(event.pos):
                return widget._mouse(event)
        return False
            
        
    def _draw(self):
        """Draw a frame."""
        self.on_draw()
        
        for widget in self.widgets:
            widget._draw()
            self.surface.blit(widget.surface,(widget.x0,widget.y0))
        
        self.flip()
        
    def on_draw(self):
        self.surface.fill((0,0,0))
        
    def on_event(self, event):
        """Override this with custom event handler.
        Must return True if the event is handled, else False."""
        return False
    
    def on_mouse(self, event):
        """Override this with custom mouse-event handler.
        Must return True if the event is handled, else False."""
    
    def flip(self):
        pygame.display.flip()            
    @property
    def surface(self):
        return pygame.display.get_surface()    
    @property
    def width(self):
        """Return the width of the drawable area."""
        return self.screen.get_width()
    @property
    def height(self):
        """Return the height of the drawable area"""
        return self.screen.get_height()