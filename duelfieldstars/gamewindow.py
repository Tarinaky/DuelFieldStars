"""
Contains a class describing how to load GameWindow.ui
"""

from PySide import QtGui, QtUiTools, QtCore

class GameWindow(QtGui.QWidget):
    def __init__(self):
        super(GameWindow, self).__init__()
        
        # Load ui file.
        loader = QtUiTools.QUiLoader()
        file_ = QtCore.QFile("forms/GameWindow.ui")
        file_.open(QtCore.QFile.ReadOnly)
        self.widget = loader.load(file_,self)
    
        # Overload repaint for viewport.
        def paintEvent(self,event):
            painter = QtGui.QPainter(self)
            painter.fillRect(self.rect(), QtGui.QBrush(QtCore.Qt.red, QtCore.Qt.Dense2Pattern) )
            return
        self.widget.gameViewport.paintEvent = paintEvent
    
        # Show and perform initial draw.    
        self.widget.show()
        