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
from model import game

from ui.game_window import GameWindow

log = logging.getLogger(__name__)

screenResolution = (640,480)
  
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    pygame.init()
    pygame.display.set_mode(screenResolution)
    window = GameWindow()
    window.run()
    
    log.debug("Quitting...")
    
        
        
        
