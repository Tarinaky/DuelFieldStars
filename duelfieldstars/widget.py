import pygame

class Widget(object):
    """Abstract class defining a region of the UI. You must define on_draw in your specialisations."""
    def __init__(self,rect):
        self.rect = rect
        self.surface = pygame.surface(rect.width,rect.height)
        self.changed = True
        
    def _draw(self):
        """Calls on_draw if this widget needs redrawing."""
        if self.changed:
            self.on_draw()
            self.changed = False
        return
        

