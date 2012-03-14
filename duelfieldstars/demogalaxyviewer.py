import pygame
import logging

from ui_abstract.window import Window
from ui_abstract.widget import Widget

from viewportwidget import ViewportWidget
from scrollbars import HorizontalScrollBar

from model.galaxy import Galaxy

screenResolution = (640,480)

class GalaxyViewerWindow(Window):
    def __init__(self):
        super(GalaxyViewerWindow,self).__init__()
        
        self.galaxy = Galaxy()
        
        self.viewport = ViewportWidget(pygame.Rect(0,0,*screenResolution), self.galaxy)
        self.add_widget(self.viewport)
        self.hzScrollbar = HorizontalScrollBar(pygame.Rect(0,self.height-8,self.width,self.height), self.viewport)
        self.add_widget(self.hzScrollbar, False)
        
        return
  
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    pygame.init()
    pygame.display.set_mode(screenResolution)
    window = GalaxyViewerWindow()
    window.run()
    
        
        
        