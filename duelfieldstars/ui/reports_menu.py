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
        
        