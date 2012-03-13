import pygame

from ui_abstract.window import Window
from ui_abstract.widget import Widget

from model.galaxy import Galaxy

screenResolution = (640,480)

class GalaxyViewerWindow(Window):
    def __init__(self):
        super(GalaxyViewerWindow,self).__init__()
        
        self.galaxy = Galaxy()
        
        self.viewport = ViewportWidget(pygame.Rect(0,0,*screenResolution) )
        self.widgets.append(self.viewport)
        
        return

        
class ViewportWidget(Widget):
    def __init__(self,rect):
        super(ViewportWidget,self).__init__(rect)
        return
    def on_draw(self):
        return
    
if __name__ == '__main__':
    pygame.init()
    pygame.display.set_mode(screenResolution)
    window = GalaxyViewerWindow()
    window.run()
    
        
        
        