"""
Control research for your faction.
"""
from ui.ui_abstract.window import Window
import logging

log = logging.getLogger(__name__)

class ResearchWindow(Window):
    faction = None
    
    def __init__(self, faction):
        super(ResearchWindow, self).__init__()
        
        log.debug("Openning research window for "+faction.name)
        
        self.faction = faction
        
    
    