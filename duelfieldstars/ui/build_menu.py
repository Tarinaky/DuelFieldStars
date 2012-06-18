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
        
        def build(destination, ship_type_):
            world = game.galaxy.planets[destination]
            # Cancel existing production
            if world.construction != None:
                world.construction = None
                world.owner.rez += 2
            # Check enough cash available.
            if world.owner.rez <2:
                event = pygame.event.Event(pygame.USEREVENT, action="insufficient rez")
                pygame.event.post(event)
                return
            # Check upkeep/income balance.
            if world.owner.income < world.owner.upkeep + 1:
                event = pygame.event.Event(pygame.USEREVENT, action="too much upkeep")
                pygame.event.post(event)
                return
            # Set construction.
            world.owner.rez -= 2
            world.construction = ship_type_
            event = pygame.event.Event(pygame.USEREVENT, action="close menu")
            pygame.event.post(event)
            event = pygame.event.Event(pygame.USEREVENT+2)
            pygame.event.post(event)
        
                
        "Cruiser"
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "        Crui(s)er    ")
        self.add_option(widget, build, destination, ship.Cruiser)
        self.add_keyboard_handler(build, pygame.KEYDOWN, pygame.K_s, 0,
                                  destination, ship.Cruiser)
        dy += widget.height
        
        "Marine Transport"
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "        (M)arine Transport    ")
        self.add_option(widget, build, destination, ship.MarineTransport)
        self.add_keyboard_handler(build, pygame.KEYDOWN, pygame.K_m, 0,
                                  destination, ship.MarineTransport)
        dy += widget.height
        
        "Colony Transport"
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "        (C)olony Transport    ")
        self.add_option(widget, build, destination, ship.ColonyTransport)
        self.add_keyboard_handler(build, pygame.KEYDOWN, pygame.K_c, 0,
                                  destination, ship.ColonyTransport)
        dy += widget.height
        
        
    