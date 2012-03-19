import pygame
import logging

from color import COLORS

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

        dx = 0
        "Flag"
        self.flag = texture_cache.flag((self.height,self.height), *self.faction.flag)
        dx += self.flag.get_width() + 5
        
        "Name"
        self.name = Text(pygame.Rect(dx,0,0,0), font, (0,0,0),
                         self.faction.name)
        self.subwidgets.append(self.name)
        dx += self.name.width + 5
        
        "Rez"
        rezLabel = Text(pygame.Rect(dx,0,0,0), font, COLORS["black"], 
                             "- Rez " )
        self.subwidgets.append(rezLabel)
        dx += rezLabel.width + 5
        
        self.rez = Text(pygame.Rect(dx,0,0,0), font, COLORS["blue"],
                                  str(self.faction.rez) )
        self.subwidgets.append(self.rez)
        dx += self.rez.width + 5
        
        incomeLabel = Text(pygame.Rect(dx,0,0,0), font, COLORS["black"],
                           "(Income")
        self.subwidgets.append(incomeLabel)
        dx += incomeLabel.width +5
        
        self.income = Text(pygame.Rect(dx,0,0,0), font, COLORS["blue"],
                           str(self.faction.income) )
        self.subwidgets.append(self.income)
        dx += self.income.width + 5
        
        expenseLabel = Text(pygame.Rect(dx,0,0,0), font, COLORS["black"],
                            "/ Upkeep")
        self.subwidgets.append(expenseLabel)
        dx += expenseLabel.width + 5
        
        self.upkeep = Text(pygame.Rect(dx,0,0,0), font, COLORS["red"],
                           str(self.faction.upkeep) )
        self.subwidgets.append(self.upkeep)
        dx += self.upkeep.width
        
        closingParanLabel = Text(pygame.Rect(dx,0,0,0), font, COLORS["black"],
                                 ")")
        self.subwidgets.append(closingParanLabel)
        dx += closingParanLabel.width + 5

    def on_draw(self):
        self.surface.fill((205,205,193))
        
        self.surface.blit(self.flag, (0,0) )

        for widget in self.subwidgets:
            widget._draw()
            self.surface.blit(widget.surface, (widget.x0, widget.y0) )



