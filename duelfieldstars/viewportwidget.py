import pygame
import logging

from ui_abstract.widget import Widget

log = logging.getLogger(__name__)

class ViewportWidget(Widget):
    def __init__(self,rect,galaxy):
        super(ViewportWidget,self).__init__(rect)
        self.galaxy = galaxy
        
        self.position = (0,0)
        self.scale = 32 # Px width of 1 pc
        
        return
    
    def on_draw(self):
        self.surface.fill((0,0,0))
        
        (x0,y0) = self.position
        width = self.width/self.scale
        height = self.height/self.scale
        for y in range (y0,height+y0):
            for x in range (x0,width+x0):
                planet = self.galaxy.at(x,y)
                if planet is not None:
                    (drawX, drawY) = (x - x0 - 0.5, y - y0 - 0.5)
                    (drawX, drawY) = (drawX*self.scale, drawY*self.scale)
                    rect = pygame.Rect(drawX, drawY, self.scale, self.scale)
                    self.surface.fill((255,255,255),rect)
            
        
        return
    
    def on_keyboard(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                self.move(0, -1)
                return True
            if event.key == pygame.K_s:
                self.move(0, 1)
                return True
            if event.key == pygame.K_a:
                self.move(-1, 0)
                return True
            if event.key == pygame.K_d:
                self.move(1, 0)
                return True
        return False
            
            
    def move(self, deltaX, deltaY):
        (x,y) = self.position
        (x,y) = (x+deltaX, y+deltaY)
        
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        
        self.position = (x,y)
        self.update()
         
         
                
            
        