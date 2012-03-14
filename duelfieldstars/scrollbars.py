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
                
        self.add_mouse_handler(self.jump, pygame.MOUSEBUTTONDOWN, 1)
        
    def jump(self):
        """Called when the scrollbar is clicked on, changes the value of the scrollbar."""
        
        (x,_) = pygame.mouse.get_pos()
        x = x * self.max / self.width - self.blockWidth
        (_,y) = self.viewport.position
        
        self.viewport.position = (x,y)

    def on_tick(self, deltaTime):
        self.set_max(self.viewport.galaxy.width * self.viewport.scale)
        self.blockWidth = self.width**2/self.max
        (x,_) = self.viewport.position
        self.set_value(x)

    def on_draw(self):
        bgColor = (64,64,64)
        fgColor = (0,0,255)
        
        self.surface.fill(bgColor)
        
        x = self.value * self.width / self.max
        
        blockWidth = self.blockWidth
        blockHeight = self.height
        
        self.surface.fill(fgColor, pygame.Rect(x, 0, blockWidth, blockHeight)) 
        
class VerticalScrollBar(Bar):
    """A widget for a scrollbar to go along the bottom of the viewport."""
    def __init__(self,rect,viewport):
        """
        rect is the bounding box for this widget on the window.
        viewport is a viewport widget to control.
        """
        super(VerticalScrollBar,self).__init__(rect)
        
        self.viewport = viewport
                
        self.add_mouse_handler(self.jump, pygame.MOUSEBUTTONDOWN, 1)
        
    def jump(self):
        """Called when the scrollbar is clicked on, changes the value of the scrollbar."""
        
        (_,y) = pygame.mouse.get_pos()
        y = y * self.max / self.height - self.blockHeight
        (x,_) = self.viewport.position
        
        self.viewport.position = (x,y)

    def on_tick(self, deltaTime):
        self.set_max(self.viewport.galaxy.height * self.viewport.scale)
        self.blockHeight = self.height**2/self.max
        (_,y) = self.viewport.position
        self.set_value(y)

    def on_draw(self):
        bgColor = (64,64,64)
        fgColor = (0,0,255)
        
        self.surface.fill(bgColor)
        
        y = self.value * self.height / self.max
        
        blockHeight = self.blockHeight
        blockWidth = self.width
        
        self.surface.fill(fgColor, pygame.Rect(0, y, blockWidth, blockHeight)) 