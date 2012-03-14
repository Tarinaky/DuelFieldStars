import pygame

from ui_abstract.widget import Widget

class ViewportWidget(Widget):
    def __init__(self,rect,galaxy):
        super(ViewportWidget,self).__init__(rect)
        self.galaxy = galaxy
        
        self.position = (0,0)
        self.scale = 128 # Px width of 1 pc
        
        return
    def on_draw(self):
        (x0,y0) = self.position
        width = self.width/self.scale
        height = self.height/self.scale
        for y in range (y0,height):
            for x in range (x0,width):
                planet = self.galaxy.at(x,y)
                if planet is not None:
                    (drawX, drawY) = (x - x0 - 0.5, y - y0 - 0.5)
                    (drawX, drawY) = (drawX*self.scale/2, drawY*self.scale/2)
                    rect = pygame.Rect(drawX, drawY, self.scale/2, self.scale/2)
                    self.surface.fill((255,255,255),rect)
            
        
        return