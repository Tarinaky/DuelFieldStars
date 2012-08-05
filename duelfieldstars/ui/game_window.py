import pygame
import logging

from ui.ui_abstract.window import Window

from ui.viewportwidget import ViewportWidget
from ui.scrollbars import HorizontalScrollBar, VerticalScrollBar
from ui.planetdetails import PlanetDetails
from ui.ticker import Ticker
from ui.action_menu import ActionMenu
from ui.ui_abstract.button import Button

from model import game
from ui import texture_cache, event_list, ledger_all_worlds, ledger_all_ships,\
    game_window_menu
from color import COLORS
from ui.build_menu import BuildMenu
from ui.insufficient_rez import InsufficientRezMenu, TooMuchUpkeep
from ui.ship_list import ShipList
from ui.research_window import ResearchWindow
from ui.reports_menu import ReportsMenu

log = logging.getLogger(__name__)

class GameWindow(Window):
    SILENT_EVENT = pygame.USEREVENT+1
    REDRAW_EVENT = pygame.USEREVENT+2
    
    def __init__(self):
        super(GameWindow,self).__init__()
        self.nice = True
        
        #game.init()
        self.player = game.factions[0]
        
        self.has_viewed_research = False
        
        self.quit_menu = False
        
        (width,height) = pygame.display.get_surface().get_size()
        self.viewport = ViewportWidget(pygame.Rect(0,14,width-174,height), game.galaxy, self)
        self.add_widget(self.viewport)
        
        self.hzScrollbar = HorizontalScrollBar(pygame.Rect(0,self.height-8,width-174,8), self.viewport)
        self.add_widget(self.hzScrollbar, False)
        
        self.vrScrollbar = VerticalScrollBar(pygame.Rect(width-8-174,14,8,height-14), self.viewport)
        self.add_widget(self.vrScrollbar, False)
        
        self.detailsPanel = None
        self.menu = None
        self.ship_list = None

        self.ticker = Ticker(pygame.Rect(0,0,self.width-174,14), self.player )
        self.add_widget(self.ticker,False)
        
        self.add_widget(Button(pygame.Rect(self.width-174,self.height-32,self.width,self.height),
                               texture_cache.button(None,
                                                     32,
                                                      (174,64), 
                                                    COLORS["black"], COLORS["aqua"], "End Turn"),
                               texture_cache.button(None, 32, (174,64), 
                                                    COLORS["black"], COLORS["blue"], "End Turn"),
                               self.end_turn))
        
        self.focusedWidget = self.viewport
        
        event = pygame.event.Event(pygame.USEREVENT, action="open event list")
        pygame.event.post(event) # Start with event list open.
        
        
        
        return

    def on_tick(self,deltaTime):
        pass
    
    def on_event(self, event):
        if event.type == pygame.USEREVENT and event.action == "End of Game":
            self.runControl = False

        try: # Close quit menu if marked for close.
            if self.menu.close:
                self.remove_widget(self.menu)
                self.menu = None
                self.quit_menu = False
                self.update()
        except:
            pass

        
        # Do not log or handle events of type USEREVENT+1
        if event.type == pygame.USEREVENT+1:
            return True
        
        # Use USEREVENT+2 to force redraws.
        if event.type == pygame.USEREVENT+2:
            for widget in self.widgets:
                widget.update()
            return True
        
        # If the quit menu is open, only the quitmenu can
        # take events.
        if self.quit_menu:
            if event.type == pygame.KEYDOWN:
                # Escape closes the menu.
                if event.key == pygame.K_ESCAPE:
                    self.menu.close = True
                    return True
                # Else pass to the menu.
                return self.menu._keyboard(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                return self.menu._mouse(event)
            return False
        
        # Pressing escape opens the quit menu.
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                event = pygame.event.Event(pygame.QUIT)
                pygame.event.post(event)
                return True
        
        # Action Menus
        if self.menu != None:
            if event.type == pygame.USEREVENT and  event.action == "close menu":
                self.remove_widget(self.menu)
                self.menu = None
                self.focusedWidget = self.viewport
            if event.type == pygame.KEYDOWN:
                return self.menu._keyboard(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu.rect.collidepoint(event.pos):
                    return self.menu._mouse(event)
                else:
                    self.remove_widget(self.menu)
                    self.menu = None
                    self.focusedWidget = self.viewport
        
        # Userevents for openning/closing widgets.    
        if event.type == pygame.USEREVENT and event.action == "selection":
            if self.detailsPanel is not None:
                self.remove_widget(self.detailsPanel)
            "Get planet"
            planet = None
            (x,y) = event.selection
            if (x,y) in game.galaxy.planets: #@UndefinedVariable
                planet = game.galaxy.planets[(x,y)] #@UndefinedVariable
            if planet is None:  
                log.debug("No planet at "+str((x,y)))
                #event = pygame.event.Event(pygame.USEREVENT,action="hide embedded ship list")
                #pygame.event.post(event)
                rect = pygame.Rect(self.width-174, 0, 174, self.height-32)
                event = pygame.event.Event(pygame.USEREVENT, action="show embedded ship list",
                                           rect=rect, position = (x,y))
                pygame.event.post(event)
            else:
                self.detailsPanel = PlanetDetails(pygame.Rect(self.width-174, 0, 174, self.height-32), planet )
                self.add_widget(self.detailsPanel, False)
            return True
                
        
        if event.type == pygame.USEREVENT and event.action == "open menu":
            if self.menu is not None:
                self.remove_widget(self.menu)
            (mouseX, mouseY) = pygame.mouse.get_pos()
            self.menu = ActionMenu(pygame.Rect(mouseX-1,mouseY-1,20,20),
                                   self.viewport.selected, event.selection,
                                   self.ship_list)
            self.add_widget(self.menu, True)
            return True
            
        if event.type == pygame.USEREVENT and event.action == "open build menu":
            self.remove_widget(self.menu)
            try:
                rect = self.menu.rect
            except AttributeError:
                (x,y) = pygame.mouse.get_pos()
                rect = pygame.Rect(x,y,0,0)
            self.menu = BuildMenu(rect,event.destination)    
            self.add_widget(self.menu, True)
            return True
        
        if event.type == pygame.USEREVENT and event.action == "insufficient rez":
            self.remove_widget(self.menu)
            self.menu = InsufficientRezMenu(self.menu.rect)
            self.add_widget(self.menu, True)
            return True
        
        if event.type == pygame.USEREVENT and event.action == "too much upkeep":
            self.remove_widget(self.menu)
            self.menu = TooMuchUpkeep(self.menu.rect)
            self.add_widget(self.menu, True)
            return True
            
        if event.type == pygame.USEREVENT and event.action == "End of Turn":
            for widget in self.widgets:
                widget.update()
            log.debug("Updated all widgets.")
            return True
        
        if event.type == pygame.USEREVENT and event.action == "show embedded ship list":
            rect = event.rect
            position = event.position
            if self.ship_list != None:
                self.remove_widget(self.ship_list)
            self.ship_list = ShipList(rect,position)
            self.add_widget(self.ship_list, False)
        
        if event.type == pygame.USEREVENT and event.action == "hide embedded ship list":        
            if self.ship_list != None:
                self.remove_widget(self.ship_list)
                self.ship_list = None
                
        # Go to a player's homeworld.
        def go_to_homeworld(event):
            if event.type == pygame.USEREVENT and event.action == "go to homeworld":
                
                def find_homeworld():
                    for planet in game.galaxy.planets.values():
                        if planet.is_homeworld == game.factions[0]:
                            return planet
                homeworld = find_homeworld()
                
                (grid_x,grid_y) = homeworld.position
                self.viewport.position = (grid_x * self.viewport.scale - self.viewport.width/2, grid_y * self.viewport.scale - self.viewport.height/2)
                
                return True
        
        if go_to_homeworld(event):
            return True
        
        # Go to location.
        def go_to(event):
            if event.type == pygame.USEREVENT and event.action == "go to":
                (grid_x, grid_y) = event.goto
                self.viewport.position = (grid_x * self.viewport.scale - self.viewport.width/2,
                                          grid_y * self.viewport.scale - self.viewport.height/2)
                return True
        if go_to(event):
            return True
        
        
        # Open research window
        def open_research(event):
            if event.type == pygame.USEREVENT and event.action == "open research":
                window = ResearchWindow(game.factions[0])
                window.run()
                event = pygame.event.Event(pygame.USEREVENT+2)
                pygame.event.post(event) # Redraw.
                return True
        if open_research(event):
            self.has_viewed_research = True
            return True
        
        # Open reports menu
        def open_reports_menu(event):
            if event.type == pygame.USEREVENT and event.action == "reports menu":
                (x,y) = event.position
                rect = pygame.Rect(x,y,0,0)
                if self.menu != None:
                    self.remove_widget(self.menu)
                self.menu = ReportsMenu(rect)
                self.add_widget(self.menu, True)
                return True
        if open_reports_menu(event):
            return True
        
        # Open event list
        def open_event_list(event):
            if event.type == pygame.USEREVENT and event.action == "open event list":
                if self.detailsPanel != None:
                    self.remove_widget(self.detailsPanel)
                self.detailsPanel = event_list.EventList(pygame.Rect(self.width-174, 0, 174, self.height-32))
                self.add_widget(self.detailsPanel, False)
                return True
        if open_event_list(event):
            return True
        
        # Open world list
        def open_world_list(event):
            if event.type == pygame.USEREVENT and event.action == "open world list":
                if self.detailsPanel != None:
                    self.remove_widget(self.detailsPanel)
                self.detailsPanel = ledger_all_worlds.LedgerAllWorlds(pygame.Rect(self.width-174, 0, 174, self.height-32))
                self.add_widget(self.detailsPanel, False)
                return True
        if open_world_list(event):
            return True
            
        # Open ship list
        def open_ship_list(event):
            if event.type == pygame.USEREVENT and event.action == "open ship list":
                if self.detailsPanel != None:
                    self.remove_widget(self.detailsPanel)
                self.detailsPanel = ledger_all_ships.LedgerAllShips(pygame.Rect(self.width-174, 0, 174, self.height-32))
                self.add_widget(self.detailsPanel, False)
                return True
        if open_ship_list(event):
            return True 
        
    def end_turn(self):
            """
            Called to signify the end of a player's turn. Any processing is performed.
            """
            if self.has_viewed_research == False:
                event = pygame.event.Event(pygame.USEREVENT)
                event.action = "open research"
                pygame.event.post(event)
                return
            else:
                game.end_of_turn(self.player)
                self.return_value = 1
                self.runControl = False
                return
  
    def on_quit(self):
        """Call the menu."""
        if self.quit_menu:
            self.runControl = False
        
        if self.menu != None:
            self.remove_widget(self.menu)
        self.menu = game_window_menu.GameWindowMenu(pygame.Rect(self.width/3,self.height/3,0,0))
        self.add_widget(self.menu, True)
        self.quit_menu = True
            
