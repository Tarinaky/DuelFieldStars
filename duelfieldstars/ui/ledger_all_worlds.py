"""
A panel widget showing all worlds in the game.
May be filtered as All, Friend or Foe.
"""
from ui.ui_abstract.widget import Widget
from ui.ui_abstract.text import Text
import pygame
from color import COLORS
from model import game
from ui import texture_cache
from assets.png import PNG
import assets
from ui.ui_abstract.image import Image

class LedgerAllWorlds(Widget):
    ALL = object()
    FRIEND = object()
    FOE = object()
    
    def __init__(self,rect):
        super(LedgerAllWorlds,self).__init__(rect)
        
        self.tile_height = 1
        self.list_start = 0
        self.scroll = 0
        
        self.all_worlds_button = None
        self.friend_worlds_button = None
        self.foe_worlds_button = None
        self.scroll_up_button = None
        self.scroll_down_button = None
        
        self.show = self.ALL
    
        self.elements = [] # List of (Widget, Method, [args]) 3-tuples.
        
        x = y = 0
        font = pygame.font.Font(pygame.font.get_default_font(), 14)
        # Title
        def show_title(x,y):
            if self.show == self.ALL:
                string = "All worlds"
            elif self.show == self.FRIEND:
                string = "Your worlds"
            else:
                string = "Your rivals' worlds"
            widget = Text(pygame.Rect(x,y,0,0), font, COLORS["white"],
                          string)
            def nop():
                pass
            self.elements.append((widget,nop,[]))
            return (widget.width, widget.height)
        (dx,dy) = show_title(x,y)
        y += dy *1.5
        
        # Show all worlds
        def all_worlds_button(x,y):
            widget = Text(pygame.Rect(x,y,0,0), font, COLORS["white"],
                          "ALL")
            def clicked():
                self.show = self.ALL
                self.scroll = 0
                self.update()
            widget.rect.w = widget.surface.get_width()
            widget.rect.h = widget.surface.get_height()
            self.elements.append((widget,clicked,[]))
            return (widget.width, widget.height)
        (dx,dy) = all_worlds_button(x,y)
        x += dx *1.5
        
        # Filter friendly worlds
        def friend_worlds_button(x,y):
            widget = Text(pygame.Rect(x,y,0,0), font, COLORS["green"],
                          "FRIEND")
            def clicked():
                self.show = self.FRIEND
                self.scroll = 0
                self.update()
            widget.rect.w = widget.surface.get_width()
            widget.rect.h = widget.surface.get_height()
            self.elements.append((widget,clicked,[]))
            return (widget.width, widget.height)
        (dx,dy) = friend_worlds_button(x,y)
        x += dx *1.5
        
        # Filter enemy worlds
        def foe_worlds_button(x,y):
            widget = Text(pygame.Rect(x,y,0,0), font, COLORS["red"],
                          "FOE")
            def clicked():
                self.show = self.FOE
                self.update()
            widget.rect.w = widget.surface.get_width()
            widget.rect.h = widget.surface.get_height()
            self.elements.append((widget, clicked, []))
            return (widget.width, widget.height)
        (dx,dy) = foe_worlds_button(x, y)
        x = 0
        dy += dy *1.5
        
        self.list_start = dy # Start list from here.
        
    def on_mouse(self,event):
        if event.type != pygame.MOUSEBUTTONDOWN:
            return False
        ((mouse_x, mouse_y), button) = (event.pos, event.button)
        (x,y) = (mouse_x - self.x0, mouse_y - self.y0)
        for (widget, method, args) in self.elements:
            if widget.rect.collidepoint(x, y) and button == 1:
                method(*args)
                return True
        try:
            if self.scroll_up_button.rect.collidepoint(x, y) and button == 1:
                if self.scroll > 0:
                    self.scroll -= 1
                    self.update()
                    return True
        except:
            pass
        try:
            if self.scroll_down_button.rect.collidepoint(x,y) and button ==1:
                self.scroll += 1
                self.update()
                return True
        except:
            pass    
    
        
    def on_draw(self):
        self.surface.fill((0x0,0x0,0x0))
        
        self.scroll_up_button = None
        self.scroll_down_button = None
        
        for (widget,_,_) in self.elements:
            self.surface.blit(widget.surface, widget.rect)
        
        # Draw list.
        y = self.list_start
        if self.scroll > 0: # Scroll up button?
            asset = assets.get(PNG,"up_16")
            widget = Image(pygame.Rect(self.width-16,y,0,0),asset)
            self.scroll_up_button = widget
            self.surface.blit(widget.surface,widget.rect)
        
        i = self.scroll
        for world in game.galaxy.planets.values():
            if y +self.tile_height > self.height:
                # Draw button to scroll list down.
                asset = assets.get(PNG,"down_16")
                widget = Image(pygame.Rect(self.width-16,self.height-16,0,0), asset)
                self.scroll_down_button = widget
                self.surface.blit(widget.surface,widget.rect)
                break
                
            
            if self.show == self.FOE and world.owner == game.factions[0]:
                # Hide friends when filtering for foes.
                continue
            if self.show == self.FRIEND and world.owner != game.factions[0]:
                # Hide foes when filtering for friends.
                continue
            if self.show != self.ALL and world.owner == None:
                continue
            
            if i > 0:
                i -= 1
                continue # Skip the first few elements if there's a scroll.
            
            dy = 0
            # Planet name
            if world.owner == None:
                color = COLORS["white"]
            elif world.owner == game.factions[0]:
                color = COLORS["green"]
            else:
                color = COLORS["red"]
            string = world.name+" "+str(world.position)
            texture = texture_cache.text(None, 12, color, string)
            self.surface.blit(texture,(0,y+dy))
            dy += texture.get_height()
            
            # Income
            try:
                string = "    Income: "+str(world.income)+" rez/turn"
            except:
                string = "    No owner"
            texture = texture_cache.text(None,12,COLORS["white"],string)
            self.surface.blit(texture,(0,y+dy))
            dy += texture.get_height()
            
            # Construction
            if world.owner == game.factions[0]:
                string = "    Building: "+str(world.construction)
            else:
                string = "    Base Value "+str(world.baseValue)
            texture = texture_cache.text(None,12,COLORS["white"],string)
            self.surface.blit(texture,(0,y+dy))
            dy += texture.get_height()
            
            # Next entry
            y += dy
            self.tile_height = dy
            
            