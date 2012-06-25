import pygame
import logging
import sys

from ui.game_window import GameWindow
from ui.launch_window import LaunchWindow

log = logging.getLogger(__name__)

screenResolution = (640,480)
  
if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    pygame.init()
    pygame.display.set_mode(screenResolution)
    window = LaunchWindow()
    window.run()
    
    log.debug("Quitting...")
    
        
        
        
