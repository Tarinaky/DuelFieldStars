"""
Control research for your faction.
"""
from ui.ui_abstract.window import Window
import logging
import pygame
from ui.ui_abstract.widget import Widget

log = logging.getLogger(__name__)

class ResearchWindow(Window):
    def __init__(self, faction):
        super(ResearchWindow, self).__init__()
        
        log.debug("Openning research window for "+faction.name)
        
        self.faction = faction
        self.research_list = Widget(pygame.Rect(0,0,self.width*2/3,self.height/2))
        self.current_research = Widget(pygame.Rect(0,self.height/2,self.width*2/3,self.height/2))
        self.research_choices = Widget(pygame.Rect(self.width*2/3,0,self.width/3,self.height))
        
        #self.add_widget(self.research_list, True)
        #self.add_widget(self.current_research, False)
        #self.add_widget(self.research_choices, False)
        
         
        
        
    
    