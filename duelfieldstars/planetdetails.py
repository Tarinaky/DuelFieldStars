import pygame

from ui_abstract.widget import Widget
from ui_abstract.writer import write

class PlanetDetails(Widget):
    """
    Simple panel containing details about a selected planet.
    """
    def __init__(self,rect,planet):
        super(PlanetDetails,self).__init__(rect)
        
        self.planet = planet
        
    def on_draw(self):
        self.surface.fill((205,205,193))
        """
        accumulator = 0
        font = pygame.font.Font(pygame.font.get_default_font(),12)
        text = font.render("Planet at "+str(self.planet.position), True, (0,0,0) )
        
        self.surface.blit(text,(0,accumulator) )
        accumulator += font.get_height()
        
        """
        
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
        write(self.surface, font, (0,0,0), text)