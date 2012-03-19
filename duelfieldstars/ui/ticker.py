import pygame
import logging

from ui_abstract.widget import Widget
from ui_abstract.text import Text

from ui import texture_cache

from model.faction import Faction, NOFACTION


log = logging.getLogger(__name__)

class Ticker(Widget):
    """
    Ticker bar to appear across the top. Contains information on rez, income and maybe some buttons.
    """

    def __init__(self,rect,faction=NOFACTION):
        super(Ticker,self).__init__(rect)

        self.faction = faction
        
        font = pygame.font.Font(pygame.font.get_default_font(),12 )
        self.subwidgets = []

        "Flag"
        self.flag = texture_cache.flag((self.height,self.height), *self.faction.flag)
        
        "Name"
        self.name = Text(pygame.Rect(20,0,0,0), font, (0,0,0),
                         self.faction.name)
        self.subwidgets.append(self.name)

    def on_draw(self):
        self.surface.fill((205,205,193))
        
        self.surface.blit(self.flag, (0,0) )

        for widget in self.subwidgets:
            widget._draw()
            self.surface.blit(widget.surface, (widget.x0, widget.y0) )



