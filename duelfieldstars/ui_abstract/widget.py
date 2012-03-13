import pygame

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

