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
from save import save

class LaunchMenu(DefaultMenu):
    """Menu of options to be displayed in the launcher."""
    def __init__(self,rect):
        super(LaunchMenu,self).__init__(rect)
        
        # Add options to the menu.
        font = pygame.font.Font(pygame.font.get_default_font(), 18)
        dx = dy = 0
        """
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
        """
        # Start new Hotseat game.
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "    Hotseat Multiplayer    ")
        def new_hotseat():
            # Ask for game parameters
            window = ParametersSetWindow()
            if window.run():
                game.init() # Initialise galaxy.
                game.game_mode = "hotseat"
                runControl = True
                while runControl:
                    # Autosave
                    save("autosave.json")
                    # Play turn.
                    window = GameWindow()
                    runControl = window.run()
                    # Cycle to next player
                    previous_player = game.factions[0]
                    game.factions.remove(previous_player)
                    game.factions.append(previous_player)
                    
        self.add_option(widget, new_hotseat)
        dy += widget.height
        
        # Load existing game.
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "    Load Game    ")
        def load_game():
            # Ask the user for the save file.
            pass
        self.add_option(widget, load_game)
        dy += widget.height
        

class LaunchWindow(Window):
    """The actual launcher itself."""
    def __init__(self):
        super(LaunchWindow,self).__init__()
        self.nice = True # Block when event queue empty
        
        self.add_widget(LaunchMenu(pygame.Rect(self.width/3,self.height/3,0,0)), True)
        
        