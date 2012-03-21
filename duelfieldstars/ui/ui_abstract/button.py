import pygame

from widget import Widget

class Button (Widget):
    """
    This class implements a simple button built from two similarly sized surfaces that
    the widget switches between depending on whether or not the widget is selected.
    """
    
    def __init__(self, rect, activeSurface, passiveSurface, method, *arguments):
        super(Button,self).__init__(rect)
        
        self.activeSurface = activeSurface
        self.passiveSurface = passiveSurface
        self.active = False
                
        self.add_mouse_handler(method, pygame.MOUSEBUTTONDOWN, 1, *arguments)
        
    def _tick(self,deltaTime):
        super(Button,self)._tick(deltaTime)
        
        (x,y) = pygame.mouse.get_pos()
        if self.rect.collidepoint(x,y):
            if not self.active:
                self.active = True
                self.update()
        else:
            if self.active:
                self.active = False
                self.update()
                
        
    def _draw(self):
        """Note, this method does not (and cannot) blit the surface to the screen. You -must- set on_draw to do so!"""
        
        if self.active:
            self.surface = self.activeSurface # Set active surface to be displayed.
        else:
            self.surface = self.passiveSurface # Set passive surface to be displayed.
            
        