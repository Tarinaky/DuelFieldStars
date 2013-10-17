from PySide import QtCore, QtGui, QtUiTools
from PySide.QtOpenGL import QGLWidget

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

import csv
import math

from loadform import load_form

class ViewWidget(QGLWidget):
    def __init__(self):
        super(ViewWidget, self).__init__()
        self.setMouseTracking(True)

        self.field = {}

        self.rotation = (0,0)
        self.relative_motion = None

    def leftClick(self, mouseX, mouseY):
        #Get Matrices
        viewport = glGetIntegerv(GL_VIEWPORT)
        modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
        projection = glGetDoublev(GL_PROJECTION_MATRIX)

        closest_match = None

        mouseY = self.height - mouseY
        for (x,y,z) in self.field: 
            (screenX,screenY, screenZ) = gluProject(x,y,z,
                    modelview, projection, viewport)
            #print str((screenX,screenY,screenZ))+str((x,y,z))
            (dx,dy) = (screenX - mouseX, screenY - mouseY)
            if dx > -4 and dx < 4 and dy > -4 and dy < 4:
                if closest_match == None:
                    closest_match = (x,y,z)
                else:
                    (_,_,z0) = closest_match
                    if screenZ < z0:
                        closest_match = (x,y,z)
        print str(closest_match)+str((mouseX,mouseY))

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.LeftButton:
            self.leftClick(event.x(), event.y() )
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.relative_motion = (event.x(), event.y() )

    def mouseMoveEvent(self, event):
        if self.relative_motion != None:
            (x,y) = (event.x(), event.y() )
            (x0,y0) = self.relative_motion
            (dx,dy) = (x - x0, y - y0)

            (azimuth, elevation) = self.rotation
            self.rotation = (azimuth + dx, min(90,max(-90,elevation + dy)))

            self.relative_motion = (x,y)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.relative_motion = None



    def resizeGL(self, w,h):
        self.width = w
        self.height = h
        self.nearZ = 1
        self.farZ = 1000
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        glViewport(0, 0, w, h)
        gluPerspective(90, float(w)/h, self.nearZ, self.farZ)

        print "OpenGL Version: "+str(glGetString(GL_VERSION) )

    def loadHabHYG(self):
        with open("./data/HabHYG.csv", "rb") as csvfile:
            reader = csv.reader(csvfile)
            cap = 500
            for row in reader:
                try:
                    x = float(row[13])
                    y = float(row[14])
                    z = float(row[15])
                    name = row[3]
                    self.field[(x,y,z)] = name
                    if len(self.field) >= cap:
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
        glRotate(-elevation, float(1), 0, 0)
        glRotate(-azimuth, 0, float(1), 0)


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


