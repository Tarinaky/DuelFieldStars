import pygame
import logging
import sys

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
    sys.exit(0)
    
        
        
        
