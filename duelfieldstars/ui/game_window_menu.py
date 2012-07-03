"""
A simple window to be summoned to confirm
whether the player wishes to exit, save state to disk...
etc...
"""
from ui.ui_abstract.window import Window
from ui.ui_abstract.text import Text
import pygame
from color import COLORS
from ui.default_menu import DefaultMenu
from model import game
from save import save

class GameWindowMenu(DefaultMenu):
    def __init__(self,rect):
        super(GameWindowMenu,self).__init__(rect)
        self.close = False # Set true to close this.
        
        font = pygame.font.Font(pygame.font.get_default_font(),32)
        
        
        widget = Text(pygame.Rect(0,0,0,0),font,COLORS["white"],
                      "    Options    ")
        self.add_option(widget, None)
        
        dy = widget.height
        
        widget = Text(pygame.Rect(0,dy,0,0), font, COLORS["light blue"],
                      "        Resume    ")
        def resume():
            self.close = True
        self.add_option(widget, resume)
        dy += widget.height
        
        widget = Text(pygame.Rect(0,dy,0,0), font,COLORS["light blue"],
                      "        Save    ")
        def save_method():
            filename = game.factions[0].name + "_Turn" + str(game.turn_count) + ".json"
            save(filename)
            self.close = True
            event = pygame.event.Event(pygame.USEREVENT+2) # Redraw
            pygame.event.post(event)
        self.add_option(widget, save_method)
        dy += widget.height
        
        widget = Text(pygame.Rect(0,dy,0,0), font, COLORS["light blue"],
                      "        Quit    ")
        def quit_method():
            event = pygame.event.Event(pygame.QUIT)
            pygame.event.post(event)
        self.add_option(widget, quit_method)
        dy += widget.height
        
        