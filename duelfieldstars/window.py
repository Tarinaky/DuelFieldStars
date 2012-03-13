import pygame

class Window(object):
    """
    A window with internal window manager to control the pygame display in an OO way.
    """
    def __init__(self,screenResolution):
        self.screenResolution = screenResolution        
        
    def run(self):
        """Entry point into the class. Executes the window's main loop."""
        runControl = True
        while runControl == True:
            "TODO: Implement"
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    runControl = False
        
    @property
    def width(self):
        """Return the width of the drawable area."""
        (w,_) = self.screenResolution
        return w
    @property
    def height(self):
        """Return the height of the drawable area"""
        (_,h) = self.screenResolution
        return h