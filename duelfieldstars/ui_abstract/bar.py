from widget import Widget

class Bar(Widget):
    """
    A simple abstract scrollbar.
    """
    def __init__(self, rect):
        super(Bar,self).__init__(rect)
        
        self.value = 0
        self.min = 0
        self.max = 100
        
    def set_max(self, max_):
        self.max = max_
        self.update()
    def set_min(self, min_):
        self.min = min_
        self.update()
    def set_value(self, value):
        self.value = value
        self.update()
    def get_value(self, value):
        return value