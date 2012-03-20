import pygame
import logging
import sys

from ui.ui_abstract.window import Window

from ui.viewportwidget import ViewportWidget
from ui.scrollbars import HorizontalScrollBar, VerticalScrollBar
from ui.planetdetails import PlanetDetails
from ui.ticker import Ticker
from ui.action_menu import ActionMenu

from model.galaxy import Galaxy

log = logging.getLogger(__name__)

screenResolution = (640,480)

class GalaxyViewerWindow(Window):
    def __init__(self):
        super(GalaxyViewerWindow,self).__init__()
        self.nice = True
        
        self.galaxy = Galaxy()
        
        (width,height) = screenResolution
        self.viewport = ViewportWidget(pygame.Rect(0,14,width-174,height), self.galaxy)
        self.add_widget(self.viewport)
        
        self.hzScrollbar = HorizontalScrollBar(pygame.Rect(0,self.height-8,width-174,8), self.viewport)
        self.add_widget(self.hzScrollbar, False)
        
        self.vrScrollbar = VerticalScrollBar(pygame.Rect(width-8-174,14,8,height-14), self.viewport)
        self.add_widget(self.vrScrollbar, False)
        
        self.detailsPanel = None
        self.menu = None

        self.ticker = Ticker(pygame.Rect(0,0,self.width-174,14), self.galaxy.factions[0] )
        self.add_widget(self.ticker,False)
        
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
            if (x,y) in self.galaxy.planets:
                planet = self.galaxy.planets[(x,y)]
            if planet is None:  
                log.debug("No planet at "+str((x,y)))
            else:
                self.detailsPanel = PlanetDetails(pygame.Rect(self.width-174, 0, 174, self.height), planet )
                self.add_widget(self.detailsPanel, False)
        
        if event.type == pygame.USEREVENT and event.action == "open menu":
            if self.menu is not None:
                self.remove_widget(self.menu)
            (mouseX, mouseY) = pygame.mouse.get_pos()
            self.menu = ActionMenu(pygame.Rect(mouseX-1,mouseY-1,20,20))
            self.add_widget(self.menu, True)        
        
        
  
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    pygame.init()
    pygame.display.set_mode(screenResolution)
    window = GalaxyViewerWindow()
    window.run()
    
    log.debug("Quitting...")
    
        
        
        
