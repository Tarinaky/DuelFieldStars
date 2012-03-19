import pygame
import logging

from ui_abstract.widget import Widget
from ui_abstract.text import Text

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

        self.text = Text(pygame.Rect(0,0,0,0), font, (0,0,0),
                         self.faction.name)
        self.subwidgets.append(self.text)

    def on_draw(self):
        self.surface.fill((205,205,193))

        for widget in self.subwidgets:
            widget._draw()
            self.surface.blit(widget.surface, (widget.x0, widget.y0) )



