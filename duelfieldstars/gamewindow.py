"""
Contains a class describing how to load GameWindow.ui
"""

from PySide import QtGui, QtUiTools, QtCore

from model.galaxy import Galaxy
from model.planet import Planet

class GameViewport(QtGui.QWidget):
    def __init__(self,parent):
        super(GameViewport,self).__init__()
        
        self.parent = parent
        
        self.galaxy = Galaxy()
        
        self.scale = 180 # How many px represent 1 pc.
        
        
    def paintEvent(self,event):    
        # Update coordinates for the viewport.
        self.x = self.parent.horizontalScrollBar.value()
        self.y = self.parent.verticalScrollBar.value()
        
        # Colour the background black.    
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.black)
        
        # Draw grid
        painter.setPen(QtCore.Qt.white)
        for y in range (0, self.height(),self.scale ):
            painter.drawLine(0, y, self.width(), y)
        for x in range (0, self.width(), self.scale ):
            painter.drawLine(x, 0, x, self.height() )
        
        # Draw planets
        for y in range (self.y,self.y+self.height() ):
            for x in range(self.x,self.x+self.width() ):
                if (x,y) in self.galaxy.planets:
                    planet = self.galaxy.planets[(x,y)]
                    
                    # Vary world colour according to value.
                    color = QtCore.Qt.yellow
                    if planet.baseValue < 75:
                        color = QtCore.Qt.red
                    if planet.baseValue > 125:
                        color = QtCore.Qt.blue                    
                        
                    rectangle = QtCore.QRectF( (x-self.x)*self.scale-30,(y-self.y)*self.scale-30,60,60)
                    painter.fillRect(rectangle, color)
        
        
        # Set the correct scale for the scrollbars.
        self.parent.horizontalScrollBar.setMaximum(self.galaxy.width)
        self.parent.verticalScrollBar.setMaximum(self.galaxy.height)
        
        
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
        self.viewport = GameViewport(self)
        self.gridLayout.addWidget(self.viewport, 0, 0)
        self.horizontalScrollBar.valueChanged.connect(self.viewport.update)
        self.verticalScrollBar.valueChanged.connect(self.viewport.update)
        
                    
        # Show and perform initial draw.    
        self.show()
        