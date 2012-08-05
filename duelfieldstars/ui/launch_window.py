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
from save_game import save
import save_game
import os

def run_hotseat():
                runControl = True
                while runControl:
                    # Autosave
                    save("autosave.json")
                    # Play turn.
                    window = GameWindow()
                    runControl = window.run()
                    # Check end of game
                    if len(game.factions) < 2:
                        break
                    # Cycle to next player
                    previous_player = game.factions[0]
                    game.factions.remove(previous_player)
                    game.factions.append(previous_player)


def new_hotseat():
            # Ask for game parameters
            window = ParametersSetWindow()
            if window.run():
                game.init() # Initialise galaxy.
                game.game_mode = "hotseat"
                run_hotseat()    


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
        
                    
        self.add_option(widget, new_hotseat)
        dy += widget.height
        
        # Load existing game.
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "    Load Game    ")
        def load_game():
            # Ask the user for the save file.
            event = pygame.event.Event(pygame.USEREVENT, 
                                       action="open folder", 
                                       file="")
            pygame.event.post(event)
            pass
        self.add_option(widget, load_game)
        dy += widget.height

class LoadMenu(DefaultMenu):
    """Menu for selecting the path of a savegame file."""
    def __init__(self,rect,path):
        super(LoadMenu,self).__init__(rect)
        
        self.path = path
        
        dy = dx = 0
        
        font = pygame.font.Font(pygame.font.get_default_font(),16)
        
        # Up to parent.
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["white"],
                          "    Back    ")
        if self.path == "":
            def back():
                event = pygame.event.Event(pygame.USEREVENT, action="back")
                pygame.event.post(event)
        else:
            def back():
                event = pygame.event.Event(pygame.USEREVENT, action="open folder", file="")
                pygame.event.post(event)
        self.add_option(widget, back)
        dy += widget.height    
        
        # List contents
        contents = save_game.list(self.path)
        for file in contents:
            widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                          "    "+file+"    ")
            if os.path.isdir(os.path.expanduser(save_game.save_path+self.path+file)):
                def open_folder(file):
                    event = pygame.event.Event(pygame.USEREVENT, action="open folder", file=self.path+file+"/")
                    pygame.event.post(event)
                self.add_option(widget, open_folder, file)
            else:
                def open_file(file):
                    event = pygame.event.Event(pygame.USEREVENT, action="load", file=self.path+file)
                    pygame.event.post(event)
                self.add_option(widget, open_file, file)
            dy += widget.height
            
        
        

class LaunchWindow(Window):
    """The actual launcher itself."""
    def __init__(self):
        super(LaunchWindow,self).__init__()
        self.nice = True # Block when event queue empty
        
        self.menu = LaunchMenu(pygame.Rect(self.width/3,self.height/3,0,0))
        
        self.add_widget(self.menu)
        
    def on_event(self,event):
        
        # Open folder
        if event.type == pygame.USEREVENT and event.action == "open folder":
            self.remove_widget(self.menu)
            self.menu = LoadMenu(self.menu.rect, event.file)
            self.add_widget(self.menu, True)
        
        # Return to launch menu
        if event.type == pygame.USEREVENT and event.action == "back":
            self.remove_widget(self.menu)
            self.menu = LaunchMenu(self.menu.rect)
            self.add_widget(self.menu, True)
            
        # Load a save file
        if event.type == pygame.USEREVENT and event.action == "load":
            file = event.file
            save_game.load(file)
            self.remove_widget(self.menu) # Replace menu
            self.menu = LaunchMenu(self.menu.rect)
            self.add_widget(self.menu,True)
            # Run the game.
            run_hotseat()
        