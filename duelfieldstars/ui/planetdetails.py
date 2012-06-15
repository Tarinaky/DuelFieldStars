import pygame

from ui_abstract.widget import Widget

import texture_cache
from color import COLORS

fontSize = 16

class PlanetDetails(Widget):
    """
    Simple panel containing details about a selected planet.
    """
    def __init__(self,rect,planet):
        super(PlanetDetails,self).__init__(rect)
        
        self.planet = planet
        
        
        
        
    def on_draw(self):
        self.surface.fill((205,205,193))
        
        y = 0
        
        # Header
        texture = texture_cache.text(None, fontSize, COLORS["black"], 
                                     "Planet at "+str(self.planet.position)+":")
        self.surface.blit(texture,(0,y))
        y += 14
        
        texture = texture_cache.text(None, fontSize, COLORS["blue"], 
                                     self.planet.name)
        self.surface.blit(texture, (0,y))
        y += 14

        # Owner
        if self.planet.owner != None:
            texture = texture_cache.text(None, fontSize, COLORS["black"],
                                         "Faction: ")
            self.surface.blit(texture, (0,y))
            
            texture = texture_cache.text(None, fontSize, COLORS["blue"],
                                         self.planet.owner.name)
            self.surface.blit(texture, (50,y))
        y += 14
        
        # Type
        texture = texture_cache.text(None, fontSize, COLORS["black"],
                                     "Type, ")
        self.surface.blit(texture, (20,y))
        
        texture = texture_cache.text(None, fontSize, COLORS["black"],
                                     self.planet.type_)
        self.surface.blit(texture, (self.width-100,y))
        y += 14
        
        # Value
        texture = texture_cache.text(None, fontSize, COLORS["black"],
                                     "Value, ")
        self.surface.blit(texture, (20,y))
        
        color = COLORS["black"]
        if self.planet.currentValue < 75:
            color = COLORS["red"]
        if self.planet.currentValue > 125:
            color = COLORS["blue"]
        
        texture = texture_cache.text(None, fontSize, color,
                                     str(self.planet.currentValue)+"%")
        self.surface.blit(texture, (self.width-100,y,0,0))
        
        color = COLORS["black"]
        if self.planet.baseValue < 75:
            color = COLORS["red"]
        if self.planet.baseValue > 125:
            color = COLORS["blue"]
            
        texture = texture_cache.text(None, fontSize, color,
                                     "("+str(self.planet.baseValue)+"%)")
        self.surface.blit(texture, (self.width-50,y))
        y += 14
        
        # Realisation
        if self.planet.owner != None:
            
            texture = texture_cache.text(None, fontSize, COLORS["black"],
                                         "Realisation, ")
            self.surface.blit(texture, (20,y))
            color = COLORS["black"]
            if self.planet.realisedValue < 75:
                color = COLORS["red"]
            if self.planet.realisedValue > 125:
                color = COLORS["blue"]
                
            texture = texture_cache.text(None, fontSize, color,
                                         str(self.planet.realisedValue)+"%")
            self.surface.blit(texture, (self.width-75,y))
        y += 14
        
        # Growth
        
        
        
        if self.planet.owner != None:
            
            texture = texture_cache.text(None, fontSize, COLORS["black"],
                                     "Growth, ")
            self.surface.blit(texture, (20,y))
            
            texture = texture_cache.text(None, fontSize, COLORS["black"],
                                         "+"+str(self.planet.growth)+"%")
            self.surface.blit(texture, (self.width-100,y))
                
        y += 14
        
        # Income
        if self.planet.owner != None:
            
            texture = texture_cache.text(None, fontSize, COLORS["black"],
                                         "Income, ")
            self.surface.blit(texture, (20,y))
            
            texture = texture_cache.text(None, fontSize, COLORS["black"],
                                         str(self.planet.income)+" rez/turn")
            self.surface.blit(texture, (self.width-75,y))
        y += 14
        
        # Construction?
        texture = texture_cache.text(None, fontSize, COLORS["black"],
                                       "Building... ")
        self.surface.blit(texture, (20,y))
        
        if self.planet.construction == None:
            texture = texture_cache.text(None,fontSize,COLORS["black"],
                                         "Nothing")
        else:
            texture = texture_cache.text(None,fontSize,COLORS["blue"],
                                         self.planet.construction.type_)
        self.surface.blit(texture, (self.width-75,y))
        y += 14
        
        # Space
        y += 14
                
        # Improvement Levels
        texture = texture_cache.text(None, fontSize, COLORS["black"],
                                     "Mining Improvement Levels")
        self.surface.blit(texture, (0,y))
        y += 14
        x = 14
        for level in self.planet.improvementLevels:
            if level <= self.planet.realisedImprovement:
                color = COLORS["blue"]
            else:
                color = COLORS["red"]
                
            texture = texture_cache.text(None, fontSize, color,
                                         str(level) )
            self.surface.blit(texture, (x,y))
            x += 28