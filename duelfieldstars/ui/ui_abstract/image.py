"""
A very simple widget that simply holds a pygame surface.
"""
from ui.ui_abstract.widget import Widget

class Image(Widget):
    def __init__(self,rect,surface):
        rect.w = surface.get_width()
        rect.h = surface.get_height()
        super(Image,self).__init__(rect)
        self.surface = surface
    def on_draw(self):
        pass # do nothing.