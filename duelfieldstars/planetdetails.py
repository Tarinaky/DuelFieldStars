import pygame

from ui_abstract.widget import Widget

class PlanetDetails(Widget):
    """
    Simple panel containing details about a selected planet.
    """
    def __init__(self,rect,planet):
        super(PlanetDetails,self).__init__(rect)
        
        self.planet = planet
        
    def on_draw(self):
        self.surface.fill((205,205,193))
        
        accumulator = 0
        font = pygame.font.Font(pygame.font.get_default_font(),12)
        text = font.render("Planet at "+str(self.planet.position), True, (0,0,0) )
        
        self.surface.blit(text,(0,accumulator) )
        accumulator += font.get_height()
        
        