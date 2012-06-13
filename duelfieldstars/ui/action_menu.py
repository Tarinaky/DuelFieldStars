import pygame

from color import COLORS

from ui_abstract.menu import Menu
from ui_abstract.text import Text

from model import game, faction

class ActionMenu (Menu):
    
    def __init__(self,rect, source, destination):
        super(ActionMenu,self).__init__(rect)
        
        self.source = source
        self.destination = destination
        self.showBuildMenu = False
        
        font = pygame.font.Font(pygame.font.get_default_font(), 12)
        dy = 0
        dx = 14
        "Name"
        name = str("Deep space at "+str(destination) )
        if destination in game.galaxy.planets: #@UndefinedVariable
            name = game.galaxy.planets[destination].name
            if game.galaxy.planets[destination].owner == faction.PLAYERFACTION:
                self.showBuildMenu = True

        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["white"], name)
        self.add_option(widget,None,None)
        dy += widget.height
        
        
        "Build here"
        if self.showBuildMenu:
            dx = 28
            widget = Text(pygame.Rect(dx,dy,0,0), font, 
                          COLORS["light blue"], "Build >")
            def open_build_menu(destination):
                event = pygame.event.Event(
                                           pygame.USEREVENT,
                                           action = "open build menu",
                                           destination = destination
                                           )
                pygame.event.post(event)
            self.add_option(widget,open_build_menu,destination)
            dy += 14
        
        
        
    def on_draw(self):
        "Calculate the size of the surface needed."
        width = 0
        height = 0
        for (widget,_,_) in self.options:
            if (widget.width+42) > width:
                width = widget.width + 28
            height += widget.height
            
        self.surface = pygame.Surface((width,height))
        self.rect.width = self.surface.get_width()
        self.rect.height = self.surface.get_height() 
        self.surface.fill(COLORS["darkGray"])
        
        