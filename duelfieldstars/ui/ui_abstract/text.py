
from widget import Widget

def write(surface, x, y , font,color,string):
    """Utility function that draws multiple lines of text."""
    accumulator = y
    
    while len(string):
        (line,_,string) = string.partition('\n')
        text = font.render(line, True, color)
        accumulator += font.get_height()
        surface.blit(text, (x,accumulator) )
    
class Text(Widget):
    """
    A simple text widget.
    """
    def __init__(self, rect, font, color, string):
        super(Text, self).__init__(rect)
        
        self.string = string
        self.font = font
        self.color = color
        
        self.on_draw()
        
    def on_draw(self):
        self.surface = self.font.render(self.string, True, self.color)
    
    @property
    def width(self):
        return self.surface.get_width()
    @property
    def height(self):
        return self.surface.get_height()
