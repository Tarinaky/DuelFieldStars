from PySide import QtCore, QtGui, QtUiTools

def load_form(path):
    loader = QtUiTools.QUiLoader()
    uifile = QtCore.QFile(path)
    uifile.open(QtCore.QFile.ReadOnly)
    ui = loader.load(uifile)
    uifile.close()

    return ui


