"""
A list of all ships in a given tile. Can be used either as a stand-alone details Widget or 'embedded' by
specifying different sizes.
"""
from ui.ui_abstract.widget import Widget
from model import game
from ui import texture_cache
from color import COLORS

class ShipList(Widget):
    """
    A list of all ships in the selected tile.
    """
    def __init__(self,rect,position):
        super(ShipList,self).__init__(rect)
        
        self.scroll = 0
        self.position = position
        
    def on_draw(self):
        self.surface.fill(COLORS["black"])
        
        dy = y = 0
        
        ship_list = game.ships[self.position]
        for ship in ship_list:
            if y >= self.height-dy:
                # TODO: print 'scroll down' button then break.
                break
            dy = 2
            dx = 16
            # Token
            texture = texture_cache.ship_token(16, ship.faction.flag, True)
            self.surface.blit(texture,(0,dy+y))
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
            dy += texture.get_height()
            # Increase y
            y += dy + 2
