import pygame
import logging

from ui.ui_abstract.window import Window

from ui.viewportwidget import ViewportWidget
from ui.scrollbars import HorizontalScrollBar, VerticalScrollBar
from ui.planetdetails import PlanetDetails

from model.galaxy import Galaxy

screenResolution = (640,480)

class GalaxyViewerWindow(Window):
    def __init__(self):
        super(GalaxyViewerWindow,self).__init__()
        
        self.galaxy = Galaxy()
        
        (width,height) = screenResolution
        self.viewport = ViewportWidget(pygame.Rect(0,0,width-174,height), self.galaxy)
        self.add_widget(self.viewport)
        
        self.hzScrollbar = HorizontalScrollBar(pygame.Rect(0,self.height-8,width-174,8), self.viewport)
        self.add_widget(self.hzScrollbar, False)
        
        self.vrScrollbar = VerticalScrollBar(pygame.Rect(width-8-174,0,8,height), self.viewport)
        self.add_widget(self.vrScrollbar, False)
        
        self.detailsPanel = None
        
        return
    
    def on_event(self, event):
        if event.type == pygame.USEREVENT and event.action == "Open planet":
            if self.detailsPanel is not None:
                self.remove_widget(self.detailsPanel)
            self.detailsPanel = PlanetDetails(pygame.Rect(self.width-174, 0, 174, self.height), event.planet )
            self.add_widget(self.detailsPanel, False)
            return True
        
  
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    pygame.init()
    pygame.display.set_mode(screenResolution)
    window = GalaxyViewerWindow()
    window.run()
    
        
        
        