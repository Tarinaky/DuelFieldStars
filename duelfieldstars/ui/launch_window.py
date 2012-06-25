"""
Specialisation of Window for launching new games,
loading existing games, etc...
"""
from ui.ui_abstract.window import Window

class LaunchWindow(Window):
    def __init__(self):
        super(LaunchWindow,self).__init__()
        self.nice = True # Block when event queue empty
        
        