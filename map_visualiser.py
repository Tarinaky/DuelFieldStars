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
        self.setMouseTracking(True)

        self.field = {}

        self.rotation = (0,0)
        self.relative_motion = None

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.relative_motion = (event.x(), event.y() )

    def mouseMoveEvent(self, event):
        if self.relative_motion != None:
            (x,y) = (event.x(), event.y() )
            (x0,y0) = self.relative_motion
            (dx,dy) = (x - x0, y - y0)

            (azimuth, elevation) = self.rotation
            self.rotation = (azimuth + dx, elevation + dy)

            self.relative_motion = (x,y)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.relative_motion = None



    def resizeGL(self, w,h):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, w, h)
        gluPerspective(90, float(w)/h, 0.1, 100)

    def loadHabHYG(self):
        with open("./data/HabHYG.csv", "rb") as csvfile:
            reader = csv.reader(csvfile)
            cap = 5000
            for row in reader:
                try:
                    x = float(row[13])
                    y = float(row[14])
                    z = float(row[15])
                    name = row[3]
                    self.field[(x,y,z)] = name
                    cap -= 1
                    if cap < 0:
                        break
                except:
                    print "Not a valid row: "+str(row)
            print str(len(self.field))+" star positions read in."


    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        #Zoom out
        glTranslate(0,0,-self.zoom.value()-1)
        #Rotate
        (azimuth, elevation) = self.rotation
        glRotate(-azimuth, 0, float(1), 0)
        glRotate(-elevation, float(1), 0, 0)


        glColor(1,1,1)
        glPointSize(1)
        glBegin(GL_POINTS)
        for (x,y,z) in self.field:
            glVertex(x,y,z)
        glEnd()

        self.zoom.repaint()



class MapVisualiser(object):
    def __init__(self):
        self.ui = ViewWidget()
        self.ui.resize(QtCore.QSize(640, 480) )
        self.ui.loadHabHYG()

        self.ui.zoom = QtGui.QSlider(QtCore.Qt.Orientation.Vertical, parent=self.ui)
        self.ui.zoom.valueChanged.connect(self.ui.update)

    def publish(self):
        self.ui.show()
        return self

if __name__ == '__main__':
    import sys
    app = QtGui.QApplication(sys.argv)
    a = MapVisualiser().publish()
    sys.exit(app.exec_() )


