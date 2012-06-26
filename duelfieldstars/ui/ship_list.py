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
        
        self.scroll_down_rect = None
        self.scroll_up_rect = None
    
    def on_mouse(self,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            
            # Scroll down button
            try:
                (x,y) = event.pos
                (x,y) = (x-self.x0, y-self.y0)
                if self.scroll_down_rect.collidepoint(x,y): # Scroll down
                    self.scroll += 1
                    self.update()
                    return True
            except AttributeError:
                pass
            
            # Scroll up button
            try:
                (x,y) = event.pos
                (x,y) = (x-self.x0, y-self.y0)
                if self.scroll_up_rect.collidepoint(x,y): # Scroll up
                    self.scroll -= 1
                    self.update()
                    return True
            except AttributeError:
                pass
            
            # Select/Deselect ships. Do this last.
            (x,y) = event.pos
            (x,y) = (x-self.x0, y-self.y0)
            (x,y) = (x, y/self.tile_height)
            log.debug("Trying to get ship "+str(y))
            ship_list = game.ships[self.position]
            if  y >= len(ship_list):
                return False # If the list isn't that long then return to the dispatcher.
            try:
                ship = ship_list[y+self.scroll]
            except IndexError:
                return False
            if ship in self.selected:
                self.selected.remove(ship)
            elif ship.faction == game.factions[0]:
                self.selected.append(ship)
            self.update()
            return True
        else:
            return False
        
    def on_draw(self):
        self.surface.fill(COLORS["black"])
        self.scroll_down_rect = None
        
        # If there is a scroll offset, show a button for going back.
        if self.scroll > 0:
            texture = assets.get(PNG,"up_16")
            self.surface.blit(texture,(self.width-texture.get_width(),
                                       0))
            self.scroll_up_rect = pygame.Rect(self.width - texture.get_width(),
                                              0,
                                              texture.get_width(),
                                              texture.get_height())
        else:
            self.scroll_up_rect = None
        
        dy = y = 0
        
        try:
            ship_list = game.ships[self.position]
        except KeyError:
            ship_list = []
        scroll = self.scroll
        for ship in ship_list:
            if scroll > 0:
                scroll -= 1
                continue # Skip down the list if there's an offset.
            
            if y >= self.height - dy:
                texture = assets.get(PNG,"down_16")
                self.surface.blit(texture,(self.width - texture.get_width(), self.height - texture.get_height()))
                self.scroll_down_rect = pygame.Rect(self.width - texture.get_width(),
                                                    self.height - texture.get_height(),
                                                    texture.get_width(),
                                                    texture.get_height())
                break
            dy = 2
            dx = 16
            # Token
            texture = texture_cache.ship_token(16, ship.faction.flag, True)
            self.surface.blit(texture,(0,dy+y))
            # Selected?
            if ship.faction == game.factions[0]: # Skip if not yours.
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
            if ship.faction == game.factions[0]:
                string = "    "+str(len(ship.orders))+" orders"
                color = COLORS["green"]
            else:
                string = "    "+ship.faction.name
                color = COLORS["red"]
            texture = texture_cache.text(None,12, color,
                                         string)
            self.surface.blit(texture,(dx,dy+y))
            if ship.orders != [] and ship.faction == game.factions[0]:
                try:
                    (order,coordinate) = ship.orders[0]
                except ValueError:
                    (order) = ship.orders[0]
                    coordinate = ""
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
