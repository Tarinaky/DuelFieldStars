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
        self.surface.fill(0x0,0x0,0x0)
        
        y = 0
        
        ship_list = game.ships[self.position]
        for ship in ship_list:
            if y >= self.height-16:
                # TODO: print 'scroll down' button then break.
                break
            # Ship name
            dy = 0
            texture = texture_cache.text(None, 8, COLORS["white"],
                                         ship.name+" ("+ship.type_+")")
            self.surface.blit(texture,(0,dy+y))
            dy += texture.get_height()
            # Show offence and defence
            texture = texture_cache.text(None,8, COLORS["white"],
                                         "    Offence: "+str(ship.attack)+" Defence: "+str(ship.defence))
            self.surface.blit(texture,(0,dy+y))
            # Increase y
            y += 16
