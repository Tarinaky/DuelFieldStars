"""
A panel widget showing all worlds in the game.
May be filtered as All, Friend or Foe.
"""
from ui.ui_abstract.widget import Widget
from ui.ui_abstract.text import Text
import pygame
from color import COLORS

class LedgerAllWorlds(Widget):
    ALL = object()
    FRIEND = object()
    FOE = object()
    
    def __init__(self,rect):
        super(LedgerAllWorlds,self).__init__(rect)
        
        self.tile_height = 1
        self.list_start = 0
        
        self.all_worlds_button = None
        self.friend_worlds_button = None
        self.foe_worlds_button = None
        self.scroll_up_button = None
        self.scroll_down_button = None
        
        self.show = self.ALL
    
        self.elements = [] # List of (Widget, Method, [args]) 3-tuples.
        
        x = y = 0
        font = pygame.font.Font(pygame.font.get_default_font(), 14)
        # Title
        def show_title(x,y):
            if self.show == self.ALL:
                string = "All worlds"
            elif self.show == self.FRIEND:
                string = "Your worlds"
            else:
                string = "Your rivals' worlds"
            widget = Text(pygame.Rect(x,y,0,0), font, COLORS["white"],
                          string)
            def nop():
                pass
            self.elements.append((widget,nop,[]))
            return (widget.width, widget.height)
        (dx,dy) = show_title(x,y)
        y += dy *1.5
        
        # Show all worlds
        def all_worlds_button(x,y):
            widget = Text(pygame.Rect(x,y,0,0), font, COLORS["white"],
                          "ALL")
            def clicked():
                self.show = self.ALL
                self.update()
            self.elements.append((widget,all_worlds_button,[]))
            x += widget.width+10
            return (widget.width, widget.height)
        (dx,dy) = all_worlds_button(x,y)
        x += dx *1.5
        
        
    def on_draw(self):
        for (widget,_,_) in self.elements:
            self.surface.blit(widget.surface, widget.rect)
            
        