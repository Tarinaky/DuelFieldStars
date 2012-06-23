import pygame

from color import COLORS

from ui_abstract.text import Text

from model import game, faction
from ui.default_menu import DefaultMenu

class ActionMenu (DefaultMenu):
    
    def __init__(self,rect, source, destination,ship_list=None):
        super(ActionMenu,self).__init__(rect)
        
        self.ship_list = ship_list
        
        self.showMoveMenu = False
        
        self.showCancel = False
        if source == destination and ship_list != None:
            if ship_list.selected != []:
                self.showCancel = True
        
        self.show_colonisation = False
        if ship_list is not None and game.galaxy.at(*destination) != None:
            for ship in ship_list.selected:
                if ship.colony and game.galaxy.at(*destination).owner == None:
                    if game.galaxy.at(*destination).type_ in ship.faction.colony_types:
                        self.show_colonisation = True
                        break
            
        self.source = source
        if source != None:
            if ship_list is not None:
                if ship_list.selected != []:
                    self.showMoveMenu = True
        
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
            self.add_keyboard_handler(open_build_menu, pygame.KEYDOWN, pygame.K_b, None, destination)
            dy += 14
        
        # Cancel orders and Scrap Ship
        if self.showCancel:
            widget = Text(pygame.Rect(dx,dy,0,0), font,
                          COLORS["light blue"], "        (X)Cancel orders    ")
            def cancel_orders(selected):
                for ship in selected:
                    ship.orders = []
                    event = pygame.event.Event(pygame.USEREVENT,action="close menu")
                    pygame.event.post(event)
                    event = pygame.event.Event(pygame.USEREVENT+2)
                    pygame.event.post(event)
            
            self.add_option(widget, cancel_orders, self.ship_list.selected)
            self.add_keyboard_handler(cancel_orders, pygame.KEYDOWN, pygame.K_x, None, self.ship_list.selected)
            dy += widget.height
            
            widget = Text(pygame.Rect(dx,dy,0,0), font,
                          COLORS["light blue"], "        Scrap ships    ")
            def scrap_ships(selected):
                for ship in selected:
                    ship.orders = [("scrap")]
                    event = pygame.event.Event(pygame.USEREVENT,action="close menu")
                    pygame.event.post(event)
                    event = pygame.event.Event(pygame.USEREVENT+2)
                    pygame.event.post(event)
            self.add_option(widget, scrap_ships, self.ship_list.selected)
            dy += widget.height
                
        # Move here
        if self.showMoveMenu:
            widget = Text(pygame.Rect(dx,dy,0,0), font,
                          COLORS["light blue"], "        (M)ove here    ")
            
            def move_ships(source,destination):
                for ship in self.ship_list.selected:
                    modifiers = pygame.key.get_mods()
                    order = ("move to", destination)
                    if modifiers & pygame.KMOD_LSHIFT or modifiers & pygame.KMOD_RSHIFT:
                        ship.orders.append(order)
                    else:
                        ship.orders = [order]
                event = pygame.event.Event(pygame.USEREVENT+2) # Call for a redraw
                pygame.event.post(event)
                event = pygame.event.Event(pygame.USEREVENT,action="close menu")
                pygame.event.post(event)
                    
            self.add_option(widget,move_ships,source,destination)
            self.add_keyboard_handler(move_ships, pygame.KEYDOWN, pygame.K_m, None, source, destination)
        dy += 14    
        # Colonise this
        if self.show_colonisation:
            widget = Text(pygame.Rect(dx,dy,0,0), font,
                          COLORS["light blue"], "        (C)olonise this    ")
            
            def colony_here(source,destination):
                for ship in self.ship_list.selected:
                    move = ("move to", destination)
                    colonise = ("colony here", destination)
                    if not ship.colony:
                        order = [move]
                    else:
                        order = [move, colonise]
                    modifiers = pygame.key.get_mods()
                    if modifiers & pygame.KMOD_LSHIFT or modifiers & pygame.KMOD_RSHIFT:
                        ship.orders.extend(order)
                    else:
                        ship.orders = order
                event = pygame.event.Event(pygame.USEREVENT+2) # Call for a redraw
                pygame.event.post(event)
                event = pygame.event.Event(pygame.USEREVENT,action="close menu")
                pygame.event.post(event)
            self.add_option(widget, colony_here, source, destination)
            self.add_keyboard_handler(colony_here, pygame.KEYDOWN, pygame.K_c, None,
                                      source, destination)  
        dy += 14
