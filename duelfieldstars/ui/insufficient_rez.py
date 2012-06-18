"""
Message to be displayed as a menu to indicate to the user
that they do not have enough 'Rez' to complete an action.
"""
import pygame
from ui.ui_abstract.text import Text
from color import COLORS
from ui.default_menu import DefaultMenu

class InsufficientRezMenu(DefaultMenu):
    message = "Insufficient Rez"
    def __init__(self, rect):
        super(InsufficientRezMenu,self).__init__(rect)
        
        font = pygame.font.Font(pygame.font.get_default_font(),12)
        widget = Text(pygame.Rect(0,0,0,0), font, COLORS["red"],
                      "    "+self.message+"    "
                      )
        self.add_option(widget, None)
    
class TooMuchUpkeep(InsufficientRezMenu):
    message = "Upkeep would exceed income"
    