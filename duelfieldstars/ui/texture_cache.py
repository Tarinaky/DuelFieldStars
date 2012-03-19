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
        pygame.draw.circle(surface, color, (radius,radius), radius)
        cache[key] = surface
        return surface