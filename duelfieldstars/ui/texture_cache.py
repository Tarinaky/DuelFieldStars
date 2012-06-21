"""
Pygame is optimised to perform blits, not draws.
This module stores a dictionary to which commonly used textures may be 'cached' and reused.
"""

import pygame
from assets.png import PNG
import assets

cache = {}

def circle(radius,color):
    key = ("circle", radius, color)
    if key in cache:
        return cache[key]
    else:
        surface = pygame.Surface((radius*2,radius*2))
        surface.set_colorkey((0,0,0))
        pygame.draw.circle(surface, color, (radius,radius), radius)
        cache[key] = surface
        return surface
    
def flag(size, forgroundColor, backgroundColor):
    key = ("flag", size, forgroundColor, backgroundColor)
    if key in cache:
        return cache[key]
    else:
        surface = pygame.Surface(size)
        # surface.set_colorkey((0,0,0))
        (width,height) = size
        bgRect = pygame.Rect(0,0, width,height)
        fgRect = pygame.Rect(0,height/3, width, height/3)
        
        surface.fill(backgroundColor, bgRect)
        surface.fill(forgroundColor, fgRect)
        
        cache[key] = surface
        return surface
    
def rect(size, color, thickness):
    key = ("rect", size, color, thickness)
    if key in cache:
        return cache[key]
    else:
        surface = pygame.Surface(size)
        surface.set_colorkey((0,0,0))
        (width,height) = size
        rect = (pygame.Rect(0,0, width, height))
        pygame.draw.rect(surface, color, rect, thickness)
        
        cache[key] = surface
        return surface
    
def text(fontname, size, color, string):
    key = ("text", fontname, size, color, string)
    if key in cache:
        return cache[key]
    else:
        font = pygame.font.Font(fontname, size)
        surface = font.render(string, True, color)
        cache[key] = surface
        return surface
    
def button(fontname, fontSize, boxSize, colorFG, colorBG, string):
    key = ("button", fontname, fontSize, boxSize, colorFG, colorBG, string)
    if key in cache:
        return cache[key]
    else:
        
        textSur = text(fontname, fontSize, colorFG, string)
        surface = pygame.Surface(boxSize)
        surface.fill(colorBG)
        surface.blit(textSur,(0,0))
        
        cache[key] = surface
        return surface
        
def ship_token(size, colors, friend, colony=False, marine=False, missile=False, service=False):
    (foreground_color, background_color) = colors
    key = ("ship_token", size, foreground_color, background_color, friend, colony, marine, missile, service)
    if key in cache:
        return cache[key]
    else:
        # Start with faction flag
        texture = flag((size,size), foreground_color, background_color).copy()
        # Mask off edge
        alphamask = None
        if friend:
            alphamask = assets.get(PNG,"friend_alphamask_"+str(size))
        else:
            alphamask = assets.get(PNG,"foe_alphamask_"+str(size))
        alphamask.set_colorkey((0xff,0xff,0xff))
        texture.blit(alphamask,(0,0))
        #texture.set_colorkey((0x0,0x0,0x0))
        cache[key] = texture
        return texture
        
    
        