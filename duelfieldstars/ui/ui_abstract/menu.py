import pygame

from widget import Widget

class Menu (Widget):
    """
    Class defining a text menu of options that a user may select and execute.
    """
    def __init__(self,rect):
        super(Menu,self).__init__(rect)
        
        self.options = [] # A list of (widget,method,*arg) tuples.
        
        self.add_mouse_handler(self.click, pygame.MOUSEBUTTONDOWN, 1, 1)
        self.add_mouse_handler(self.click, pygame.MOUSEBUTTONDOWN, 3, 3)
        
    def do_nothing(self):
        pass
        
    def add_option(self, widget, method=None,*arguments):
        if method == None:
            method = self.do_nothing
        widget.rect = (widget.x0,widget.y0,widget.width,widget.height)
        self.options.append((widget,method,arguments))
        
    def _tick(self,deltaTime):
        super(Menu,self)._tick(deltaTime)
        for (widget,_,_) in self.options:
            widget._tick(deltaTime)
        self.update()
        
    def click(self,button):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        (mouseX, mouseY) = (mouseX - self.x0, mouseY - self.y0)
        for (widget, method, args) in self.options:
            if pygame.Rect(widget.rect).collidepoint(mouseX, mouseY):
                method(*args)
                return True
                
    def _draw(self):
        super(Menu,self)._draw()
        
        for (widget, _, _) in self.options:
            widget._draw()
            self.surface.blit(widget.surface, (widget.x0, widget.y0) )


    