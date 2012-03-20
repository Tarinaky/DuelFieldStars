import pygame

from widget import Widget

class Menu (Widget):
    """
    Class defining a text menu of options that a user may select and execute.
    NOTE: This interface contains no information how to display the menu options.
    
    See also: ListMenu, IconMenu
    """
    def __init__(self,rect):
        super(Menu,self).__init__(rect)
        
        self.options = [] # A list of (widget,method,*arg) tuples.
        
    def add_option(self, widget, method, *arguments):
        self.options.append((widget,method,arguments))
        
    def click(self,button):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        (mouseX, mouseY) = (mouseX - self.x0, mouseY - self.y0)
        for (widget, method, args) in self.options:
            if widget.rect.collidepoint(mouseX, mouseY):
                method(*args)
                
