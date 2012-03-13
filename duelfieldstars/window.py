import pygame

class Window(object):
    """
    A window with internal widget manager to control the pygame display in an OO way.
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
            self.tick()
    
    def tick(self):
        """Executes a single 'tick' or frame."""
        "TODO: Events"
        "TODO: game rules"
        self.draw()
        
    def draw(self):
        """Draw a frame."""
        self.screen.fill((0,0,0))
        
        for widget in self.widgets:
            widget.draw()
        
        self.flip()
        
    
    def flip(self):
        pygame.display.flip()            
    @property
    def screen(self):
        return pygame.display.get_surface()    
    @property
    def width(self):
        """Return the width of the drawable area."""
        return self.screen.get_width()
    @property
    def height(self):
        """Return the height of the drawable area"""
        return self.screen.get_height()