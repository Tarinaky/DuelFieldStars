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
        self.surface.fill((255,255,255))