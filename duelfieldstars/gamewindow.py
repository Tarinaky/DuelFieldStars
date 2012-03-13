"""
Contains a class describing how to load GameWindow.ui
"""

from PySide import QtGui, QtUiTools, QtCore

from model.galaxy import Galaxy
from model.planet import Planet

from gameviewport import GameViewport
from planetdetails import PlanetDetails

class GameWindow(QtGui.QMainWindow):
        
    def __init__(self):
        super(GameWindow, self).__init__()
        
        # Load ui file.
        loader = QtUiTools.QUiLoader()
        file_ = QtCore.QFile("forms/GameWindow.ui")
        file_.open(QtCore.QFile.ReadOnly)
        self = loader.load(file_,self)
    
        # Create galaxy
        self.galaxy = Galaxy()
    
        # Add viewport.
        self.viewport = GameViewport(self)
        self.gridLayout.addWidget(self.viewport, 0, 0)
        self.horizontalScrollBar.valueChanged.connect(self.viewport.update)
        self.verticalScrollBar.valueChanged.connect(self.viewport.update)
        
        
        
        # Add planet details widget
        self.details.fixture = None
        self.open_planet(None)
        print self
        
        # Show and perform initial draw.    
        self.show()
        return
        
    def open_planet(self,planet):
        if self.details.fixture is not None:
            self.details.layout().removeWidget(self.details.fixture)
        self.details.fixture = PlanetDetails(self,planet)
        self.details.addWidget(self.details.fixture)