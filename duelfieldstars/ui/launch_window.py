"""
Specialisation of Window for launching new games,
loading existing games, etc...
"""
from ui.ui_abstract.window import Window
from ui.default_menu import DefaultMenu
from ui.game_window import GameWindow
from color import COLORS
import pygame
from ui.ui_abstract.text import Text
from model import game
from ui.ParametersSetWindow import ParametersSetWindow

class LaunchMenu(DefaultMenu):
    """Menu of options to be displayed in the launcher."""
    def __init__(self,rect):
        super(LaunchMenu,self).__init__(rect)
        
        # Add options to the menu.
        font = pygame.font.Font(pygame.font.get_default_font(), 18)
        dx = dy = 0
        
        # Open new Sandbox game.
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "    Single Player Sandbox    ")
        def new_sandbox():
            game.init() # Reset game
            window = GameWindow()
            while window.run():
                pass
        self.add_option(widget, new_sandbox)
        dy += widget.height
        
        # Start new Hotseat game.
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "    Hotseat Multiplayer    ")
        def new_hotseat():
            # Ask for game parameters
            window = ParametersSetWindow()
            if window.run():
                game.init() # Initialise galaxy.
                window = GameWindow()
                window.run() # Open viewport.
        self.add_option(widget, new_hotseat)
        dy += widget.height
        
        

class LaunchWindow(Window):
    """The actual launcher itself."""
    def __init__(self):
        super(LaunchWindow,self).__init__()
        self.nice = True # Block when event queue empty
        
        self.add_widget(LaunchMenu(pygame.Rect(self.width/3,self.height/3,0,0)), True)
        
        