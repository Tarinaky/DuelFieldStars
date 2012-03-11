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
        
        self.scale = 60 # How many px represent 1 pc.
    
    def wheelEvent(self,event):
        (x,y) = (event.pos().x()/self.scale+self.x,event.pos().y()/self.scale+self.y)
        if event.delta() > 0 and self.scale < 300:
            self.scale = self.scale *2
        if event.delta() < 0 and self.scale > 15:
            self.scale = self.scale /2
        
        newX = x - self.width()/2 /self.scale
        newY = y - self.height()/2 /self.scale
        
        self.parent.horizontalScrollBar.setValue(newX)
        self.parent.verticalScrollBar.setValue(newY)
        
        self.update()
        
    def paintEvent(self,event):    
        # Update coordinates for the viewport.
        self.x = self.parent.horizontalScrollBar.value()
        self.y = self.parent.verticalScrollBar.value()
        
        # Colour the background black.    
        painter = QtGui.QPainter(self)
        painter.fillRect(self.rect(), QtCore.Qt.black)
        
        # Draw grid
        painter.setPen(QtCore.Qt.white)
        for y in range (0, self.galaxy.height,3 ):
            painter.drawLine(0, (y-self.y)*self.scale, self.width(), (y-self.y)*self.scale)
        for x in range (0, self.galaxy.width,3 ):
            painter.drawLine((x-self.x)*self.scale, 0, (x-self.x)*self.scale, self.height() )
        
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
                        
                    rectangle = QtCore.QRectF(
                                              (x-self.x)*self.scale - self.scale/6,
                                              (y-self.y)*self.scale - self.scale/6,
                                              self.scale/3,self.scale/3)
                    painter.fillRect(rectangle, color)
        
        
        # Set the correct scale for the scrollbars.
        self.parent.horizontalScrollBar.setMaximum(self.galaxy.width - self.width() / self.scale)
        self.parent.verticalScrollBar.setMaximum(self.galaxy.height - self.height() / self.scale)
        
        
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
        