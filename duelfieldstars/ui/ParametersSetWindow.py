"""
Window for setting/changing the parameters with which
to generate a new game galaxy.
"""
from ui.ui_abstract.window import Window
from model import game
from ui.ui_abstract.text import Text
import pygame
from color import COLORS
from assets.png import PNG
import assets
from ui.ui_abstract.image import Image

class ParametersSetWindow(Window):
    
    def __init__(self):
        super(ParametersSetWindow,self).__init__()
        self.nice = True # Block when event queue empty
        
        # Load current parameters.
        self.galaxy_size = game.galaxy_size
        self.world_density = game.world_density
        self.faction_num = game.number_of_initial_factions
        self.seed = game.generation_seed
        
        self.rects = []
    
    def on_mouse(self,event):
        (x,y) = event.pos
        if event.type != pygame.MOUSEBUTTONDOWN:
            return False
        for (rect,method) in self.rects:
            if rect.collidepoint(x,y):
                return method()
        
    def on_draw(self):
        # Display all the parameters
        dx = dy = 20
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        
        # Blank window
        self.widgets = []
        self.rects = []
        self.surface.fill((0x0,0x0,0x0))
        
        # Window title
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["white"],
                      "Parameters for new game")
        self.add_widget(widget, False)
        dy += widget.height *1.5
        
        # Galaxy size
        (w,h) = self.galaxy_size
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "Galaxy size: "+str(w)+"x"+str(h)+" parsecs")
        self.add_widget(widget, False)
        dx += widget.width+8
        
        def decrease_galaxy_size():
            (w,h) = self.galaxy_size
            (w,h) = (w-25,h-25) # Decrease by 25 square pc
            if w < 25 or h < 25:
                (w,h) = (25,25)
            self.galaxy_size = (w,h)
            #self.update()
            d = self.world_density
            if self.faction_num > int(w*h*d):
                self.faction_num = int(w*h*d)
        asset = assets.get(PNG,"left_16")
        widget = Image(pygame.Rect(dx,dy,0,0),asset)
        self.add_widget(widget, False)
        self.rects.append((widget.rect,decrease_galaxy_size))
        dx += widget.width + 8
        
        def increase_galaxy_size():
            (w,h) = self.galaxy_size
            (w,h) = (w+25,h+25) # Increase by 25 square parsecs
            self.galaxy_size = (w,h)
            #self.update()
        asset = assets.get(PNG,"right_16")
        widget = Image(pygame.Rect(dx,dy,0,0),asset)
        self.add_widget(widget, False)
        self.rects.append((widget.rect,increase_galaxy_size))
        dy += widget.height *1.2
        
        
        # World density
        dx = 20
        d = self.world_density
        num_worlds = int(w * h * d)
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "World density: 1/"+str(int(d**(-1)))+" ("+str(num_worlds)+" worlds)")
        self.add_widget(widget, False)
        dx += widget.width + 8
        
        def decrease_density():
            choice = [float(1)/100, float(1)/50, float(1)/25, float(1)/12, float(1)/9]
            d = self.world_density
            for i in range(len(choice)):
                if d == choice[i]:
                    if i > 0:
                        self.world_density = choice[i-1]
                        (w,h) = self.galaxy_size
                        d = self.world_density
                        if self.faction_num > int(w*h*d):
                            self.faction_num = int(w*h*d)
                    return
                else:
                    i += 1
            
        asset = assets.get(PNG,"left_16")
        widget = Image(pygame.Rect(dx,dy,0,0),asset)
        self.add_widget(widget, False)
        self.rects.append((widget.rect,decrease_density))
        dx += widget.width + 8
        
        def increase_density():
            choice = [float(1)/100, float(1)/50, float(1)/25, float(1)/12, float(1)/9]
            d = self.world_density
            for i in range(len(choice)):
                if d == choice[i]:
                    if i < len(choice)-1:
                        self.world_density = choice[i+1]
                    return
                else:
                    i += 1
        asset = assets.get(PNG,"right_16")
        widget = Image(pygame.Rect(dx,dy,0,0),asset)
        self.add_widget(widget, False)
        self.rects.append((widget.rect,increase_density))
        
        dy += widget.height * 1.2
        
        # Seed?
        dx = 20
        seed = self.seed
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "Galaxy seed: "+str(seed))
        self.add_widget(widget, False)
        dy += widget.height *1.2
        
        # Number of factions?
        dx = 20
        num = self.faction_num
        widget = Text(pygame.Rect(dx,dy,0,0), font, COLORS["light blue"],
                      "Number of factions: "+str(num))
        self.add_widget(widget, False)
        dx += widget.width +8
        
        def decrease_faction_num():
            if self.faction_num > 2:
                self.faction_num -= 1
        asset = assets.get(PNG,"left_16")
        widget = Image(pygame.Rect(dx,dy,0,0), asset)
        self.add_widget(widget, False)
        self.rects.append((widget.rect,decrease_faction_num))
        dx += widget.width +8
        
        def increase_faction_num():
            (w,h) = self.galaxy_size
            if self.faction_num < int(w*h*self.world_density):
                self.faction_num += 1
        asset = assets.get(PNG,"right_16")
        widget = Image(pygame.Rect(dx,dy,0,0), asset)
        self.add_widget(widget, False)
        self.rects.append((widget.rect,increase_faction_num))
        
        dy += widget.height *1.2
        
        
        # Start the game!
        dx = 20
        font = pygame.font.Font(pygame.font.get_default_font(),32)
        def start_game():
            game.galaxy_size = self.galaxy_size
            game.world_density = self.world_density
            game.generation_seed = self.seed
            game.number_of_initial_factions = self.faction_num
            
            self.return_value = 1
            self.runControl = False
        
        widget = Text(pygame.Rect(dx,dy,0,0),font, COLORS["green"],
                      "Start the Game!")
        widget.on_draw()
        widget.rect.w = widget.width
        widget.rect.h = widget.height
        self.add_widget(widget, False)
        self.rects.append((widget.rect, start_game))
        
        dy += widget.height *1.2