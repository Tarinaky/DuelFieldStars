from PySide import QtGui, QtUiTools, QtCore

from model.galaxy import Galaxy
from model.planet import Planet

class PlanetDetails(QtGui.QWidget):
    def __init__(self,parent):
        super(PlanetDetails, self).__init__()
        
        self.parent = parent
        
        self.planet = None
        
        # Load ui file.
        loader = QtUiTools.QUiLoader()
        file_ = QtCore.QFile("forms/PlanetDetails.ui")
        file_.open(QtCore.QFile.ReadOnly)
        self = loader.load(file_,self)
        
        self.pushButton.clicked.connect(self.hide)
        
    
    def set_planet(self, planet):
        self.planet = planet
        self.show()
        
        