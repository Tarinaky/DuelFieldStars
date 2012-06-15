import pygame

from color import COLORS

from ui_abstract.text import Text

from model import game, faction
from ui.default_menu import DefaultMenu

class ActionMenu (DefaultMenu):
    
    def __init__(self,rect, source, destination):
        super(ActionMenu,self).__init__(rect)
        
        self.source = source
        self.destination = destination
        self.showBuildMenu = False
        
        font = pygame.font.Font(pygame.font.get_default_font(), 12)
        dy = 0
        dx = 0
        "Name"
        name = str("    Deep space at "+str(destination) )
        if destination in game.galaxy.planets: #@UndefinedVariable
            name = "    "+game.galaxy.planets[destination].name+"    "
            if game.galaxy.planets[destination].owner == faction.PLAYERFACTION:
                self.showBuildMenu = True

        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["white"], name + "    ")
        
        self.add_option(widget,None)
        dy += widget.height
        
        
        "Build here"
        if self.showBuildMenu:
            
            widget = Text(pygame.Rect(dx,dy,0,0), font, 
                          COLORS["light blue"], "        (B)uild >    ")
            def open_build_menu(destination):
                event = pygame.event.Event(
                                           pygame.USEREVENT,
                                           action = "open build menu",
                                           destination = destination
                                           )
                pygame.event.post(event)
            self.add_option(widget,open_build_menu,destination)
            self.add_keyboard_handler(open_build_menu, pygame.KEYDOWN, pygame.K_b, 0, destination)
            dy += 14
        
