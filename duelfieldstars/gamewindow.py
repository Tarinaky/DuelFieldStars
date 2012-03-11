"""
Contains a class describing how to load GameWindow.ui
"""

from PySide import QtGui, QtUiTools, QtCore

from model.galaxy import Galaxy
from model.planet import Planet

class GameViewport(QtGui.QWidget):
    def __init__(self):
        super(GameViewport,self).__init__()
        
        self.galaxy = Galaxy()
        self.galaxy.planets[(1,1)] = Planet(1,1)
    def paintEvent(self,event):
        print "draw"
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.black)
        
        for y in range (50):
            for x in range(50):
                if (x,y) in self.galaxy.planets:
                    planet = self.galaxy.planets[(x,y)]
                    rectangle = QtCore.QRectF(x*33,y*33,15,15)
                    painter.fillRect(rectangle, QtCore.Qt.red)
        
        return

class GameWindow(QtGui.QWidget):
    def __init__(self):
        super(GameWindow, self).__init__()
        
        # Load ui file.
        loader = QtUiTools.QUiLoader()
        file_ = QtCore.QFile("forms/GameWindow.ui")
        file_.open(QtCore.QFile.ReadOnly)
        self = loader.load(file_,self)
    
        # Add viewport.
        self.gridLayout.addWidget(GameViewport(), 0, 0)
        
                    
        # Show and perform initial draw.    
        self.show()
        