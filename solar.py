from PySide import QtCore, QtGui, QtUiTools
from PySide.QtOpenGL import QGLWidget

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

class SolarWidget(QGLWidget):
    def __init__(self):
        super(SolarWidget, self).__init__()
        
        self.field = []

        self.rotation = (0,0)
        self.displacement = (0,0)
        self.mousePosition = None

    def publish(self):
        self.show()
        return self

    def resizeGL(self, w, h):
        self.width = w
        self.height = h
        self.nearZ = 1
        self.farZ = 1000
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, w, h)
        gluPerspective(90, float(w)/h, self.nearZ, self.farZ)
        print "Window resized. Context Version: "+str(glGetString(GL_VERSION) )

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    a = SolarWidget().publish()
    sys.exit(app.exec_() )

