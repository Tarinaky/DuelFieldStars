import pygame

from ui_abstract.bar import Bar

class HorizontalScrollBar(Bar):
    """A widget for a scrollbar to go along the bottom of the viewport."""
    def __init__(self,rect,viewport):
        """
        rect is the bounding box for this widget on the window.
        viewport is a viewport widget to control.
        """
        super(HorizontalScrollBar,self).__init__(rect)
        
        self.viewport = viewport
        self.set_max(self.viewport.galaxy.width*self.viewport.scale)
        
        self.add_mouse_handler(self.jump, pygame.MOUSEBUTTONDOWN, 1)
        
    def jump(self):
        """Called when the scrollbar is clicked on, changes the value of the scrollbar."""
        (x,_) = pygame.mouse.get_pos()
        # Set this x as the middle of the screen.
        y = self.viewport.y0
        self.viewport.position = (x - self.viewport.width, y)

    def on_tick(self, deltaTime):
        (x,_) = self.viewport.position
        
        if x is not self.value:
            self.set_value(x)

    def on_draw(self):
        bgColor = (64,64,64)
        fgColor = (0,0,255)
        self.surface.fill(bgColor)
        
        blockWidth = self.width / self.max
        blockHeight = self.height
        
        self.surface.fill(fgColor, pygame.Rect(self.value, 0, blockWidth, blockHeight) )
        