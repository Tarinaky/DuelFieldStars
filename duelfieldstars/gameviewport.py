from PySide import QtGui, QtUiTools, QtCore

from model.galaxy import Galaxy
from model.planet import Planet

class GameViewport(QtGui.QWidget):
    def __init__(self,parent):
        super(GameViewport,self).__init__()
        
        self.parent = parent
        
        self.galaxy = Galaxy()
        
        self.scale = 60 # How many px represent 1 pc.
        
        
    
    def mousePressEvent(self,event):
        x = event.pos().x()/self.scale+self.x
        y = event.pos().y()/self.scale+self.y
        
        
        planet = None
        for scanY in [y-1,y+1,y]:
            for scanX in [x-1,x+1,x]:
                if (scanX,scanY) in self.galaxy.planets:
                    planet = self.galaxy.planets[(scanX,scanY)]
        
        print "Got planet at..."+str(planet.position)
        self.parent.planetDetails.set_planet(planet)
        
    
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
            painter.drawText(0, (y-self.y)*self.scale, "("+str(y)+")")
        for x in range (0, self.galaxy.width,3 ):
            painter.drawLine((x-self.x)*self.scale, 15, (x-self.x)*self.scale, self.height() )
            painter.drawText((x-self.x)*self.scale, 15, "("+str(x)+")")
        
        # Draw planets
        for y in range (self.y,self.y+self.height() ):
            for x in range(self.x,self.x+self.width() ):
                if (x,y) in self.galaxy.planets:
                    planet = self.galaxy.planets[(x,y)]
                    
                    # Vary world colour according to value.
                    color = QtCore.Qt.yellow
                    painter.setPen(QtCore.Qt.black)
                    if planet.baseValue < 75:
                        color = QtCore.Qt.red
                        painter.setPen(QtCore.Qt.white)
                    if planet.baseValue > 125:
                        color = QtCore.Qt.blue
                        painter.setPen(QtCore.Qt.white)                    
                        
                    rectangle = QtCore.QRectF(
                                              (x-self.x)*self.scale - self.scale/6,
                                              (y-self.y)*self.scale - self.scale/6,
                                              self.scale/3,self.scale/3)
                    painter.fillRect(rectangle, color)
                    
                    #Print planet class.
                    painter.drawText(rectangle, QtCore.Qt.AlignCenter, planet.type)
        
        
        # Set the correct scale for the scrollbars.
        self.parent.horizontalScrollBar.setMaximum(self.galaxy.width - self.width() / self.scale)
        self.parent.verticalScrollBar.setMaximum(self.galaxy.height - self.height() / self.scale)
        
        
        return