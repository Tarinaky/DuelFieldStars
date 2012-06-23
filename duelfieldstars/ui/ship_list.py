"""
A list of all ships in a given tile. Can be used either as a stand-alone details Widget or 'embedded' by
specifying different sizes.
"""
from ui.ui_abstract.widget import Widget
from model import game
from ui import texture_cache
from color import COLORS
from assets.png import PNG
import assets
import pygame
import logging

log = logging.getLogger(__name__)

class ShipList(Widget):
    """
    A list of all ships in the selected tile.
    """
    def __init__(self,rect,position):
        super(ShipList,self).__init__(rect)
        
        self.scroll = 0
        self.position = position
        
        self.selected = []
        self.tile_height = 1
    
    def on_mouse(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # Select/Deselect ships. Do this last.
            (x,y) = event.pos
            (x,y) = (x-self.x0, y-self.y0)
            (x,y) = (x, y/self.tile_height)
            log.debug("Trying to get ship "+str(y))
            ship_list = game.ships[self.position]
            if  y >= len(ship_list):
                return False # If the list isn't that long then return to the dispatcher.
            ship = ship_list[y+self.scroll]
            if ship in self.selected:
                self.selected.remove(ship)
            else:
                self.selected.append(ship)
            self.update()
            return True
        else:
            return False
        
    def on_draw(self):
        self.surface.fill(COLORS["black"])
        
        dy = y = 0
        
        ship_list = game.ships[self.position]
        for ship in ship_list:
            if y >= self.height:
                # TODO: print 'scroll down' button then break.
                texture = assets.get(PNG,"down_16")
                self.surface.blit(texture,(self.width - texture.get_width(), self.height - texture.get_height()))
                break
            dy = 2
            dx = 16
            # Token
            texture = texture_cache.ship_token(16, ship.faction.flag, True)
            self.surface.blit(texture,(0,dy+y))
            # Selected?
            if ship in self.selected:
                texture = assets.get(PNG,"selected_16")
            else:
                texture = assets.get(PNG,"unselected_16")
            self.surface.blit(texture,(0,dy+y+16))
            # Ship name
            texture = texture_cache.text(None, 12, COLORS["white"],
                                         ship.name+" ("+ship.type_+")")
            self.surface.blit(texture,(dx,dy+y))
            dy += texture.get_height()
            # Show offence and defence
            texture = texture_cache.text(None,12, COLORS["white"],
                                         "    Offence: "+str(ship.attack)+" Defence: "+str(ship.defence))
            self.surface.blit(texture,(dx,dy+y))
            dy += texture.get_height()
            # Show orders
            texture = texture_cache.text(None,12, COLORS["white"],
                                         "    "+str(len(ship.orders))+" orders")
            self.surface.blit(texture,(dx,dy+y))
            if ship.orders != []:
                (order,coordinate) = ship.orders[0]
                dx += texture.get_width()
                texture = texture_cache.text(None, 12, COLORS["green"],
                                             "    "+order+" "+str(coordinate))
                self.surface.blit(texture,(dx,dy+y))
                dx = 16
            
            dy += texture.get_height()
            # Save dy
            self.tile_height = dy +2
            # Increase y
            y += dy + 2
