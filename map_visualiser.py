from PySide import QtCore, QtGui, QtUiTools
from PySide.QtOpenGL import QGLWidget

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import csv

from loadform import load_form

class ViewWidget(QGLWidget):
    def __init__(self):
        super(ViewWidget, self).__init__()
        self.field = {}

    def loadHabHYG(self):
        with open("./data/HabHYG.csv", "rb") as csvfile:
            reader = csv.reader(csvfile)
            for row in reader:
                try:
                    x = float(row[13])
                    y = float(row[14])
                    z = float(row[15])
                    name = row[3]
                    self.field[(x,y,z)] = name
                except:
                    pass


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glColor(1,1,1)
        glPointSize(16)
        glBegin(GL_POINTS)
        for (x,y,z) in self.field:
            glVertex(x,y,z)
        glEnd()



class MapVisualiser(object):
    def __init__(self):
        self.ui = ViewWidget()
        self.ui.loadHabHYG()

    def publish(self):
        self.ui.show()
        return self

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    a = MapVisualiser().publish()
    sys.exit(app.exec_() )


