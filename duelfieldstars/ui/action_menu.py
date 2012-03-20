from ui_abstract.menu import Menu

class ActionMenu (Menu):
    
    def __init__(self,rect):
        super(ActionMenu,self).__init__(rect)
        
    def on_draw(self):
        self.surface.fill((0xff,0xff,0xff))