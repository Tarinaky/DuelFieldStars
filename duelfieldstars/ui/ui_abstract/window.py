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
        self.focusedWidget = None
        
        self.clock = pygame.time.Clock()
        self.nice = False
        
    def run(self):
        """Entry point into the class. Executes the window's main loop."""
        self.runControl = True
        self.return_value = False # Return value to be returned upon completion.
        while self.runControl == True:
            self._tick()
        return self.return_value
    
    def _tick(self):
        """Executes a single 'tick' or frame."""
        "Dispatch to widget's tick methods"
        deltaTime = self.clock.tick()
        self.on_tick(deltaTime)
        for widget in self.widgets:
            widget._tick(deltaTime)
        "Event dispatcher."
        if self.nice == True:
            event = pygame.event.wait() # Wait for events.
            if self._event(event) == False:
                log.debug("Unknown event "+str(event) )
        for event in pygame.event.get(): # Run event handler
            if self._event(event) == False:
                log.debug("Unknown event "+str(event) )
        "Frame renderer"
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
        if (event.type == pygame.KEYDOWN or event.type == pygame.KEYUP):
            return self._keyboard(event)
        log.debug("Unknown event "+str(event) )
        return False
    
    def _keyboard(self,event):
        """Dispatches keyboard events to widgets.
        Returns True if the event is handled, else false."""
        if self.on_keyboard(event):
            return True
        if self.focusedWidget is not None:
            return self.focusedWidget._keyboard(event)
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
        
    def on_tick(self,deltaTime):
        """Override this with custom behavior to be performed each tick.
        deltaTime contains the amount of time since the last frame - allowing integrator behavior."""
    
    def on_draw(self):
        self.surface.fill((0,0,0))
        
    def on_event(self, event):
        """Override this with custom event handler.
        Must return True if the event is handled, else False."""
        return False
    
    def on_mouse(self, event):
        """Override this with custom mouse-event handler.
        Must return True if the event is handled, else False."""
        
    def on_keyboard(self, event):
        """Override this with custom key-event handler.
        Must return True if the event is handled, else false."""
        
    def add_widget(self, widget, getFocus=True):
        """Add a widget to the window, and automatically focus on it."""
        self.widgets.append(widget)
        if getFocus == True:
            self.focusedWidget = widget
    def remove_widget(self, widget):
        if widget in self.widgets:
            self.widgets.remove(widget)
    def flip(self):
        pygame.display.flip()           
    @property
    def surface(self):
        return pygame.display.get_surface()    
    @property
    def width(self):
        """Return the width of the drawable area."""
        return self.surface.get_width()
    @property
    def height(self):
        """Return the height of the drawable area"""
        return self.surface.get_height()
