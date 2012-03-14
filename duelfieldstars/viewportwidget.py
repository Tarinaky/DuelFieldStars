import pygame
import logging

from ui_abstract.widget import Widget

log = logging.getLogger(__name__)

class ViewportWidget(Widget):
    def __init__(self,rect,galaxy):
        super(ViewportWidget,self).__init__(rect)
        self.galaxy = galaxy
        
        self.position = (0,0)
        self.velocity = (0,0)
        self.scale = 32 # Px width of 1 pc
        
        # Register key handlers.
        self.add_keyboard_handler(self.change_scroll_speed, pygame.KEYDOWN, pygame.K_w, 0, 0, -1) # Up.
        self.add_keyboard_handler(self.change_scroll_speed, pygame.KEYUP, pygame.K_w, 0, 0, 1) # Release.
        self.add_keyboard_handler(self.change_scroll_speed, pygame.KEYDOWN, pygame.K_s, 0, 0, 1) # Down.
        self.add_keyboard_handler(self.change_scroll_speed, pygame.KEYUP, pygame.K_s, 0, 0, -1) # Release.
        self.add_keyboard_handler(self.change_scroll_speed, pygame.KEYDOWN, pygame.K_a, 0, -1, 0) # Left.
        self.add_keyboard_handler(self.change_scroll_speed, pygame.KEYUP, pygame.K_a, 0, 1, 0) # Release.
        self.add_keyboard_handler(self.change_scroll_speed, pygame.KEYDOWN, pygame.K_d, 0, 1, 0) # Right.
        self.add_keyboard_handler(self.change_scroll_speed, pygame.KEYUP, pygame.K_d, 0, -1, 0) # Release.
        
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
    
            
            
    def change_scroll_speed(self, d2X, d2Y):
        (dx,dy) = self.velocity
        (dx,dy) = (dx+d2X, dy+d2Y)
            
        self.velocity = (dx,dy)
         
         
                
            
        