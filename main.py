import sys

from PySide import QtUiTools, QtCore, QtGui

from duelfieldstars import gamewindow

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    myWindow = gamewindow.GameWindow()
    print myWindow
    app.exec_()