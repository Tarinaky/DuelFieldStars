"""
Contains a class describing how to load GameWindow.ui
"""

from PySide import QtGui, QtUiTools, QtCore

class GameWindow(QtGui.QWidget):
    def __init__(self):
        super(GameWindow, self).__init__()
        loader = QtUiTools.QUiLoader()
        file_ = QtCore.QFile("forms/GameWindow.ui")
        file_.open(QtCore.QFile.ReadOnly)
        myWidget = loader.load(file_,self)
    
        myWidget.show()