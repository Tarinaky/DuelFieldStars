"""Use this file as a script to launch the game."""

import sys

import pygame

from duelfieldstars.window import Window

if __name__ == '__main__':
    resolution = (640,480)
    
    pygame.init()
    screen = pygame.display.set_mode(resolution)
    pygame.display.set_caption("Duelfield Stars")
    
    myWindow = Window(resolution)
    myWindow.run()