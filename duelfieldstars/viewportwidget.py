import pygame
import logging

from ui_abstract.widget import Widget

log = logging.getLogger(__name__)

class ViewportWidget(Widget):
    def __init__(self,rect,galaxy):
        super(ViewportWidget,self).__init__(rect)
        self.galaxy = galaxy
        
        self.font = pygame.font.Font(pygame.font.get_default_font(),10)
        
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
        self.add_mouse_handler(self.click_left_mouse_button, pygame.MOUSEBUTTONDOWN, 1)
        self.add_mouse_handler(self.zoom, pygame.MOUSEBUTTONDOWN, 4, "in") # Zoom in
        self.add_mouse_handler(self.zoom, pygame.MOUSEBUTTONDOWN, 5, "out") # Zoom out
        return
            
    def on_draw(self):
        self.surface.fill((0,0,0))
        
        (x0,y0) = self.position
        (x0,y0) = (int(x0//self.scale), int(y0//self.scale) )
        
        width = self.width/self.scale
        height = self.height/self.scale
        
        # Draw coordinate grid
        for y in range (1, self.galaxy.height, 3):
            pygame.draw.line(self.surface, (255,255,255), (0, (y-y0)*self.scale), (self.galaxy.width*self.scale, (y-y0)*self.scale) )
            label = self.font.render("("+str(y)+")", True, (255,255,255) )
            self.surface.blit(label, (0,(y-y0)*self.scale+2) )
        for x in range (1, self.galaxy.width, 3):
            pygame.draw.line(self.surface, (255,255,255), ((x-x0)*self.scale, 0), ((x-x0)*self.scale, self.galaxy.height*self.scale) )
            label = self.font.render("("+str(x)+")", True, (255,255,255) )
            self.surface.blit(label, ((x-x0)*self.scale,0) )
        
        # Draw planets
        for y in range (y0,height+y0):
            for x in range (x0,width+x0):
                planet = self.galaxy.at(x,y)
                if planet is not None:
                    (drawX, drawY) = (x - x0 - 0.25, y - y0 - 0.25)
                    (drawX, drawY) = (drawX*self.scale, drawY*self.scale)
                    rect = pygame.Rect(drawX, drawY, self.scale/2, self.scale/2)
                    
                    #Choose colour based on value
                    color = (255,255,0)
                    textColor = (0,0,0)
                    if planet.baseValue < 75:
                        color = (255,69,0)
                    if planet.baseValue > 125:
                        color = (64,64,255)
                        
                    self.surface.fill(color,rect)
                    font = pygame.font.Font(pygame.font.get_default_font(), self.scale/2)
                    label = font.render(planet.type, True, textColor)
                    self.surface.blit(label, (drawX, drawY))
            
        
        return
    
    def on_tick(self, deltaTime):
        (x,y) = self.position
        (dx,dy) = self.velocity
        (x,y) = (x + dx * deltaTime, y + dy * deltaTime)
                
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
        self.update()
            
    def click_left_mouse_button(self):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        (viewX, viewY) = self.position
        (mouseX, mouseY) = (mouseX - self.x0 + viewX, mouseY - self.y0 + viewY)
        def rounddiv(a,b):
            return a // b + (1 if a%b >= b // 2 else 0)
        (x, y) = (rounddiv(mouseX,self.scale), rounddiv(mouseY,self.scale) ) # Where in the map the click occured.
        
        
        planet = None
        if (x,y) in self.galaxy.planets:
            planet = self.galaxy.planets[(x,y)]
        if planet is not None:
            event = pygame.event.Event(pygame.USEREVENT, action="Open planet", planet=planet)
            pygame.event.post(event)
        else:
            log.debug("No planet to open at "+str((mouseX,mouseY) ) )
            
    def change_scroll_speed(self, d2X, d2Y):
        (dx,dy) = self.velocity
        (dx,dy) = (dx+d2X, dy+d2Y)
            
        self.velocity = (dx,dy)
         
    def zoom(self, string):
        (mouseX, mouseY) = pygame.mouse.get_pos()
        (x,y) = self.position
        (mouseX, mouseY) = (mouseX + x - self.x0, mouseY + y - self.y0)
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
                
            
        