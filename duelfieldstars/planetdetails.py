"""
Loader for the planet details inset.
"""

from PySide import QtGui, QtUiTools, QtCore

from model.galaxy import Galaxy
from model.planet import Planet

class PlanetDetails(QtGui.QWidget):
    def __init__(self,parent,planet):
        super(PlanetDetails,self).__init__()
        
        self.parent = parent
        self.planet = planet
        
        # Load the ui file.
        loader = QtUiTools.QUiLoader()
        file_ = QtCore.QFile("forms/PlanetDetails.ui")
        file_.open(QtCore.QFile.ReadOnly)
        self = loader.load(file_,self)
        
        # Set labels and values
        self.setTitle("Planet at "+str(planet.position) )
        self.type.setText(planet.type) # Colony Type
        