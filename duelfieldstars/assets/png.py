"""
Code for loading bitmap textures into the asset cache.
"""
from assets import Type
import assets
import pygame

import logging
import os
log = logging.getLogger(__name__)

class PNG(Type):
    def load(self,filename=None):
        if filename == None:
            log.debug("Loading all PNG textures.")
            return self.load_all()
        path = assets.asset_path+"/png/"+filename+".png"
        log.debug("loading "+path)
        surface = pygame.image.load(path)
        assets._cache[(PNG,filename)] = surface
        
    def load_all(self):
        for file in os.listdir(assets.asset_path+"/png/"):
            filename = file.split('.')[0]
            self.load(filename)
            
assets._types.append(PNG)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    os.chdir("..")
    PNG().load()
    print assets._cache