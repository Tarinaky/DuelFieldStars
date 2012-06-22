import pygame
import logging

from color import COLORS

from ui_abstract.widget import Widget
from ui_abstract.text import Text

from ui import texture_cache
import assets
from assets.png import PNG
from ui.ui_abstract.image import Image

log = logging.getLogger(__name__)

class Ticker(Widget):
    """
    Ticker bar to appear across the top. Contains information on rez, income and maybe some buttons.
    """

    def __init__(self,rect,faction=None):
        super(Ticker,self).__init__(rect)

        self.faction = faction
        self.flagbox = pygame.Rect((0,0,0,0))
        self.researchbox = pygame.Rect((0,0,0,0))

    def generate_surface(self):        
        font = pygame.font.Font(pygame.font.get_default_font(),12 )
        self.subwidgets = []

        dx = 0
        "Flag"
        self.flag = texture_cache.flag((self.height,self.height), *self.faction.flag)
        self.flagbox = pygame.Rect((dx,0,self.height,self.height))
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
        
        # Start at the reverse end of the bar.
        dx = self.width
        
        "Research button"
        texture = assets.get(PNG, "research_16")
        texture.set_colorkey((0x0,0x0,0x0))
        dx -= texture.get_width()
        self.researchbox = pygame.Rect(dx,0,texture.get_width(), texture.get_height())
        self.subwidgets.append(Image(self.researchbox,texture))

    def on_mouse(self,event):
        # Check flag box.
        def check_flag_box(a):
            if a.type == pygame.MOUSEBUTTONDOWN:
                ((mouse_x, mouse_y),button) = (a.pos, a.button)
                if self.flagbox.colliderect(pygame.Rect((mouse_x,mouse_y,0,0))):
                    if button == 1:
                        event = pygame.event.Event(pygame.USEREVENT, action="go to homeworld")
                        pygame.event.post(event)
                        return True
            return False
        
        if check_flag_box(event):
            return True
        
        # Check research box.
        def check_research_box(a):
            if a.type == pygame.MOUSEBUTTONDOWN:
                ((mouse_x, mouse_y), button) = (a.pos, a.button)
                if self.researchbox.colliderect(pygame.Rect((mouse_x,mouse_y,0,0))):
                    if button == 1:
                        event = pygame.event.Event(pygame.USEREVENT, action="open research")
                        pygame.event.post(event)
                        return True
            return False
        if check_research_box(event):
            return True
                

    def on_draw(self):
        self.generate_surface()
        self.surface.fill((205,205,193))

        self.surface.blit(self.flag, (0,0) )

        for widget in self.subwidgets:
            widget._draw()
            self.surface.blit(widget.surface, (widget.x0, widget.y0) )



