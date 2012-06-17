"""
Code for loading bitmap textures into the asset cache.
"""
from assets import Type
import assets
import pygame

import logging
import os
log = logging.getLogger(__name__)

alpha = False # If False then per-pixel alpha will be discarded on load. Set to True to preserve.

class PNG(Type):
    def load(self,filename=None):
        if filename == None:
            log.debug("Loading all PNG textures.")
            return self.load_all()
        path = assets.asset_path+"/png/"+filename+".png"
        log.debug("loading "+path)
        surface = pygame.image.load(path)
        if alpha:
            surface = surface.convert_alpha()
        else:
            surface = surface.convert()
        assets._cache[(PNG,filename)] = surface
        return True
        
    def load_all(self):
        for file in os.listdir(assets.asset_path+"/png/"):
            filename = file.split('.')[0]
            self.load(filename)
        return True
            
assets._types.append(PNG)

if __name__ == '__main__': # Import all PNGs as a test.
    logging.basicConfig(level=logging.DEBUG)
    pygame.init()
    pygame.display.set_mode((640,480))
    os.chdir("..")
    #PNG().load()
    assets.preload()
    print assets._cache