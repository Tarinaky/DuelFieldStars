import sys

from PySide import QtUiTools, QtCore, QtGui

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
        
    loader = QtUiTools.QUiLoader()
    file_ = QtCore.QFile("forms/GameWindow.ui")
    file_.open(QtCore.QFile.ReadOnly)
    myWidget = loader.load(file_)
    
    myWidget.show()
    
    app.exec_()