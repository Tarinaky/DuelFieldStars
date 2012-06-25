"""
Window for setting/changing the parameters with which
to generate a new game galaxy.
"""
from ui.ui_abstract.window import Window
from model import game
from ui.ui_abstract.text import Text
import pygame
from color import COLORS

class ParametersSetWindow(Window):
    
    def __init__(self):
        super(ParametersSetWindow,self).__init__()
        self.nice = True # Block when event queue empty
        
        # Load current parameters.
        self.galaxy_size = game.galaxy_size
        self.world_density = game.world_density
        self.faction_num = game.number_of_initial_factions
        self.seed = game.generation_seed
        
    def on_draw(self):
        # Display all the parameters
        dx = dy = 20
        font = pygame.font.Font(pygame.font.get_default_font(), 12)
        
        # Blank window
        self.widgets = []
        self.surface.fill((0x0,0x0,0x0))
        
        # Window title
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["white"],
                      "Parameters for new game")
        self.add_widget(widget, False)
        dy += widget.height *1.5
        
        # Galaxy size
        (w,h) = self.galaxy_size
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "Galaxy size: "+str(w)+"x"+str(h)+" parsecs")
        self.add_widget(widget, False)
        dy += widget.height *1.2
        
        
        