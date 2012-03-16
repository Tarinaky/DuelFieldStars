import pygame

from ui_abstract.widget import Widget
from ui_abstract.text import Text

from model.faction import NOFACTION

class PlanetDetails(Widget):
    """
    Simple panel containing details about a selected planet.
    """
    def __init__(self,rect,planet):
        super(PlanetDetails,self).__init__(rect)
        
        self.planet = planet
        
        black = (0,0,0)
        red = (255,0,0)
        blue = (0,0,255)
        
        font = pygame.font.Font(pygame.font.get_default_font(),12)
        self.text = []
        
        y = 0
        # Header
        self.text.append(Text(pygame.Rect(0,y,0,0), font, black, 
                              "Planet at "+str(self.planet.position)+":"))
        y += 14
        self.text.append(Text(pygame.Rect(0,y,0,0), font, blue,
                              self.planet.name))
        y += 14

        # Owner
        if self.planet.owner != NOFACTION:
            self.text.append(Text(pygame.Rect(0,y,0,0), font, black,
                                  "Faction: "))
            self.text.append(Text(pygame.Rect(50,y,0,0),font,blue,
                                  self.planet.owner.name))
        y += 14
        
        # Type
        self.text.append(Text(pygame.Rect(20,y,0,0), font, black,
                              "Type, "))
        self.text.append(Text(pygame.Rect(self.width-100,y,0,0), font, black,
                              self.planet.type))
        y += 14
        
        # Value
        self.text.append(Text(pygame.Rect(20,y,0,0), font, black,
                              "Value, "))
        color = black
        if self.planet.currentValue < 75:
            color = red
        if self.planet.currentValue > 125:
            color = blue
        self.text.append(Text(pygame.Rect(self.width-100,y,0,0), font, color,
                              str(self.planet.currentValue)+"%"))
        color = black
        if self.planet.baseValue < 75:
            color = red
        if self.planet.baseValue > 125:
            color = blue
        self.text.append(Text(pygame.Rect(self.width-50,y,0,0), font, color,
                              "("+str(self.planet.baseValue)+"%)"))
        y += 14
        # Realisation
        if self.planet.owner != NOFACTION:
            
            self.text.append(Text(pygame.Rect(20,y,0,0), font, black,
                                  "Realisation, "))
            color = black
            if self.planet.realisedValue < 75:
                color = red
            if self.planet.realisedValue > 125:
                color = blue
            self.text.append(Text(pygame.Rect(self.width-75,y,0,0), font, color,
                                  str(self.planet.realisedValue)+"%" ) )
        y += 14
        # Growth
        if self.planet.owner != NOFACTION:
            self.text.append(Text(pygame.Rect(20,y,0,0), font, black,
                                  "Growth, "))
            self.text.append(Text(pygame.Rect(self.width-100,y,0,0), font, black,
                                  "+"+str(self.planet.growth)+"%"))
                
        y += 14
        
        # Income
        if self.planet.owner != NOFACTION:
            self.text.append(Text(pygame.Rect(20,y,0,0), font, black, 
                                  "Income, "))
            self.text.append(Text(pygame.Rect(self.width-75,y,0,0), font, black,
                                  str(self.planet.income)+" rez/turn"))
        y += 14
        
        # Space
        y += 14
        
        # Improvement Levels
        self.text.append(Text(pygame.Rect(0,y,0,0), font, black,
                              "Mining Improvement Levels"))
        y += 14
        x = 14
        for level in self.planet.improvementLevels:
            if level <= self.planet.realisedImprovement:
                color = blue
            else:
                color = red
            self.text.append(Text(pygame.Rect(x,y,0,0), font, color,
                                  str(level)))
            x += 28
        
        
    def on_draw(self):
        self.surface.fill((205,205,193))
        
        for text in self.text:
            text._draw()
            self.surface.blit(text.surface, (text.x0, text.y0) )
        
