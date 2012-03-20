"""
Pygame is optimised to perform blits, not draws.
This module stores a dictionary to which commonly used textures may be 'cached' and reused.
"""

import pygame

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
        fgRect = pygame.Rect(0,height/4, width, height/2+1)
        
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
        