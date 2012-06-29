"""
A menu of different reports and lists to open in the rhs
panel.
"""
from ui.default_menu import DefaultMenu
from ui.ui_abstract.text import Text
import pygame
from color import COLORS

class ReportsMenu(DefaultMenu):
    
    def __init__(self,rect):
        super(ReportsMenu,self).__init__(rect)
        
        font = pygame.font.Font(pygame.font.get_default_font(), 12)
        dy = 0
        dx = 0
                
        # Label
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["white"],
                      "    Reports    ")
        self.add_option(widget, None)
        dy += widget.height
        
        # Event List
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "        Event Log    ")
        def open_event_list():
            event = pygame.event.Event(pygame.USEREVENT, action="open event list")
            pygame.event.post(event)
            event = pygame.event.Event(pygame.USEREVENT, action="close menu")
            pygame.event.post(event)
            
        self.add_option(widget, open_event_list)
        dy += widget.height
        
        # World List
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "        World List    ")
        def open_world_list():
            event = pygame.event.Event(pygame.USEREVENT, action="open world list")
            pygame.event.post(event)
            event = pygame.event.Event(pygame.USEREVENT, action="close menu")
            pygame.event.post(event)
        self.add_option(widget, open_world_list)
        dy += widget.height
        
        # Ship List
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "        Ship List    ")
        def open_ship_list():
            event = pygame.event.Event(pygame.USEREVENT, action="open ship list")
            pygame.event.post(event)
            event = pygame.event.Event(pygame.USEREVENT, action="close menu")
            pygame.event.post(event)
        self.add_option(widget, open_ship_list)
        dy += widget.height