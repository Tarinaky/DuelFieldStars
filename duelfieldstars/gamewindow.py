"""
Contains a class describing how to load GameWindow.ui
"""

from PySide import QtGui, QtUiTools, QtCore

from model.galaxy import Galaxy
from model.planet import Planet

from gameviewport import GameViewport
from planetdetails import PlanetDetails

class GameWindow(QtGui.QWidget):
    def __init__(self):
        super(GameWindow, self).__init__()
        
        # Load ui file.
        loader = QtUiTools.QUiLoader()
        file_ = QtCore.QFile("forms/GameWindow.ui")
        file_.open(QtCore.QFile.ReadOnly)
        self = loader.load(file_,self)
    
        # Add viewport.
        self.viewport = GameViewport(self)
        self.gridLayout.addWidget(self.viewport, 0, 0)
        self.horizontalScrollBar.valueChanged.connect(self.viewport.update)
        self.verticalScrollBar.valueChanged.connect(self.viewport.update)
        
        # Add planetDetails
                    
        # Show and perform initial draw.    
        self.show()
        