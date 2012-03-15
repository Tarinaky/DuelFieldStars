import pygame

from ui_abstract.widget import Widget
from ui_abstract.text import write

class PlanetDetails(Widget):
    """
    Simple panel containing details about a selected planet.
    """
    def __init__(self,rect,planet):
        super(PlanetDetails,self).__init__(rect)
        
        self.planet = planet
        
    def on_draw(self):
        self.surface.fill((205,205,193))
        
        text = "Planet at "+str(self.planet.position)+":\n"
        text += self.planet.name+"\n"        
        text += "    Type, "+str(self.planet.type)+"\n"
        text += "    Value, "+str(self.planet.baseValue)+"%\n"
        text += "    Realisation, "+str(self.planet.realisedValue)+"%\n"
        text += "\n"
        text += "Mining Improvement Levels\n"
        for level in self.planet.improvementLevels:
            text += "    "+str(level)+"\n"
        
        
        font = pygame.font.Font(pygame.font.get_default_font(),12)
        write(self.surface, 0,0, font, (0,0,0), text)