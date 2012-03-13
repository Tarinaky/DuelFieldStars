import pygame

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
        runControl = True
        while runControl == True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runControl = False
            self._tick()
    
    def _tick(self):
        """Executes a single 'tick' or frame."""
        "TODO: Events"
        "TODO: game rules"
        self._draw()
        
    def _draw(self):
        """Draw a frame."""
        self.on_draw()
        
        for widget in self.widgets:
            widget._draw()
        
        self.flip()
        
    def on_draw(self):
        self.surface.fill((0,0,0))
    
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