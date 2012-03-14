import pygame
import logging

from ui_abstract.widget import Widget

log = logging.getLogger(__name__)

class ViewportWidget(Widget):
    def __init__(self,rect,galaxy):
        super(ViewportWidget,self).__init__(rect)
        self.galaxy = galaxy
        
        self.position = (0,0) # position in px
        self.velocity = (0,0) # position in px/ms
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
        # Mouse button handlers
        self.add_mouse_handler(self.zoom, pygame.MOUSEBUTTONDOWN, 4, "in") # Zoom in
        self.add_mouse_handler(self.zoom, pygame.MOUSEBUTTONDOWN, 5, "out") # Zoom out
        return
    
    def on_draw(self):
        (x,y) = self.position
        # Snap to edge if outside bottom right boundary
        if (x + self.width) > self.galaxy.width*self.scale:
            x = self.galaxy.width*self.scale - self.width
        if (y + self.height) > self.galaxy.height*self.scale:
            y = self.galaxy.height*self.scale - self.height
 
        # Snap to edge if outside topleft boundary
        
        if x < 0:
            x = 0
        if y < 0:
            y = 0
        
        self.position = (x,y)
        
        self.surface.fill((0,0,0))
        
        (x0,y0) = self.position
        (x0,y0) = (int(x0//self.scale), int(y0//self.scale) )
        
        width = self.width/self.scale
        height = self.height/self.scale
        for y in range (y0,height+y0):
            for x in range (x0,width+x0):
                planet = self.galaxy.at(x,y)
                if planet is not None:
                    (drawX, drawY) = (x - x0 - 0.25, y - y0 - 0.25)
                    (drawX, drawY) = (drawX*self.scale, drawY*self.scale)
                    rect = pygame.Rect(drawX, drawY, self.scale/2, self.scale/2)
                    self.surface.fill((255,255,255),rect)
            
        
        return
    
    def on_tick(self, deltaTime):
        (x,y) = self.position
        (dx,dy) = self.velocity
        (x,y) = (x + dx * deltaTime, y + dy * deltaTime)
        self.position = (x,y)
        self.update()
            
            
    def change_scroll_speed(self, d2X, d2Y):
        (dx,dy) = self.velocity
        (dx,dy) = (dx+d2X, dy+d2Y)
            
        self.velocity = (dx,dy)
         
    def zoom(self, string):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        (x,y) = self.position
        (mouseX, mouseY) = (mouseX + x, mouseY + y)
        (mouseX, mouseY) = (mouseX/self.scale, mouseY/self.scale)
        
        if string == "in":
            self.scale = self.scale * 2
            if self.scale > 64:
                self.scale = 64
                
        if string == "out":
            self.scale = self.scale /2
            if self.scale < 8:
                self.scale = 8
                
        (mouseX, mouseY) = (mouseX * self.scale, mouseY * self.scale)
        self.position = (mouseX - self.width/2, mouseY - self.height/2)
        
        self.update()     
                
            
        