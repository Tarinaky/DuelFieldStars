import pygame
import logging
import sys

from ui.ui_abstract.window import Window

from ui.viewportwidget import ViewportWidget
from ui.scrollbars import HorizontalScrollBar, VerticalScrollBar
from ui.planetdetails import PlanetDetails
from ui.ticker import Ticker
from ui.action_menu import ActionMenu
from ui.ui_abstract.button import Button

from model import game
from ui import texture_cache
from color import COLORS
from ui.build_menu import BuildMenu

log = logging.getLogger(__name__)

class GameWindow(Window):
    def __init__(self):
        super(GameWindow,self).__init__()
        self.nice = True
        
        game.init()
        self.player = game.factions[0]
        
        (width,height) = pygame.display.get_surface().get_size()
        self.viewport = ViewportWidget(pygame.Rect(0,14,width-174,height), game.galaxy)
        self.add_widget(self.viewport)
        
        self.hzScrollbar = HorizontalScrollBar(pygame.Rect(0,self.height-8,width-174,8), self.viewport)
        self.add_widget(self.hzScrollbar, False)
        
        self.vrScrollbar = VerticalScrollBar(pygame.Rect(width-8-174,14,8,height-14), self.viewport)
        self.add_widget(self.vrScrollbar, False)
        
        self.detailsPanel = None
        self.menu = None

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
        
        
        return
    
    def on_event(self, event):
        """if event.type == pygame.USEREVENT and event.action == "Open planet":
            if self.detailsPanel is not None:
                self.remove_widget(self.detailsPanel)
            self.detailsPanel = PlanetDetails(pygame.Rect(self.width-174, 0, 174, self.height), event.planet )
            self.add_widget(self.detailsPanel, False)
            return True"""
        if self.menu != None:
            if event.type == pygame.KEYDOWN:
                return self.menu._keyboard(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.menu.rect.collidepoint(event.pos):
                    return self.menu._mouse(event)
                else:
                    self.remove_widget(self.menu)
                    self.menu = None
                    self.focusedWidget = self.viewport
            
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
            else:
                self.detailsPanel = PlanetDetails(pygame.Rect(self.width-174, 0, 174, self.height-32), planet )
                self.add_widget(self.detailsPanel, False)
            return True
                
        
        if event.type == pygame.USEREVENT and event.action == "open menu":
            if self.menu is not None:
                self.remove_widget(self.menu)
            (mouseX, mouseY) = pygame.mouse.get_pos()
            self.menu = ActionMenu(pygame.Rect(mouseX-1,mouseY-1,20,20),self.viewport.selected, event.selection)
            self.add_widget(self.menu, True)
            return True
            
        if event.type == pygame.USEREVENT and event.action == "open build menu":
            self.remove_widget(self.menu)
            self.menu = BuildMenu(self.menu.rect,event.destination)
            self.add_widget(self.menu, True)
            return True
            
        if event.type == pygame.USEREVENT and event.action == "End of Turn":
            for widget in self.widgets:
                widget.update()
                
            log.debug("Updated all widgets.")
            return True        
        
    def end_turn(self):
            """
            Called to signify the end of a player's turn. Any processing is performed.
            """
            game.end_of_turn(self.player)
            return
  
        
