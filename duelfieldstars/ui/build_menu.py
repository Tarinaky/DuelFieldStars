"""List of items that can be built at a world."""
import pygame
from ui.ui_abstract.text import Text
from color import COLORS
from model import game, ship
from ui.default_menu import DefaultMenu

class BuildMenu(DefaultMenu):
    
    def __init__(self,rect,destination):
        """Destination is an (x,y) tuple addressing the
        world the item will be built at."""
        super(BuildMenu,self).__init__(rect)
        
        self.destination = destination
        
        font = pygame.font.Font(pygame.font.get_default_font(), 12)
        dy = 0
        dx = 0
        
        "Label"
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["white"],
                      "    Build at "+game.galaxy.planets[destination].name+"    ")
        self.add_option(widget,None)
        dy += widget.height
        

        "Cruiser"
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "        Crui(s)er    ")
        def build_cruiser(destination):
            # Check enough cash available.
            if game.galaxy.planets[destination].owner.rez <2:
                event = pygame.event.Event(pygame.USEREVENT, action="insufficient rez")
                pygame.event.post(event)
                return
            # Set construction.
            game.galaxy.planets[destination].owner.rez -= 2
            game.galaxy.planets[destination].construction = ship.Cruiser
            event = pygame.event.Event(pygame.USEREVENT, action="close menu")
            pygame.event.post(event)
            event = pygame.event.Event(pygame.USEREVENT+2)
            pygame.event.post(event)
            
        self.add_option(widget, build_cruiser, destination)
        dy += widget.height
        
        "Marine Transport"
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "        (M)arine Transport    ")
        self.add_option(widget, None)
        dy += widget.height
        
        "Colony Transport"
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "        (C)olony Transport    ")
        self.add_option(widget, None)
        dy += widget.height
        
        
    