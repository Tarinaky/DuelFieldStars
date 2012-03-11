import sys

from PySide import QtUiTools, QtCore, QtGui

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
        
    loader = QtUiTools.QUiLoader()
    file = QtCore.QFile("forms/GameWindow.ui")
    file.open(QtCore.QFile.ReadOnly)
    myWidget = loader.load(file)
    
    myWidget.show()
    
    app.exec_()