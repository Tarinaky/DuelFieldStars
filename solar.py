from PySide import QtCore, QtGui, QtUiTools
from PySide.QtOpenGL import QGLWidget

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from math import *

class OrbitalPath(object):
    def __init__(self, gravitational_parameter, semimajor_axis, eccentricity,
            inclination, longtitude_of_ascending_node,
            argument_of_periapsis):
        self.gravitational_parameter = float(gravitational_parameter) # In m^3/s^2
        self.semimajor_axis = float(semimajor_axis) # In Au, or 150e9m
        self.eccentricity = float(eccentricity) # Less than 1.
        self.inclination = float(inclination) # Not implemented. Degrees from sun's equator
        self.longtitude_of_ascending_node = float(longtitude_of_ascending_node) # Not implemented. Degrees
        self.argument_of_periapsis = float(argument_of_periapsis) # Not implemented. Degrees

        self.sample_orbit()

    def sample_orbit(self):
        self.period = 2.0*pi*sqrt((150e9 * self.semimajor_axis)**3 / self.gravitational_parameter)
        print self.period
        weeks = max(1,int(floor(self.period /(3600*168))) )
        print weeks
        week_length = self.period/weeks
        samples = []
        
        n = 1.0/self.period
        #print (n,self.period,week_length,weeks,week_length*weeks)
        for i in range (weeks):
            mean_anomaly = float(2*pi*i * week_length * n)
            eccentric_anomaly = mean_anomaly
            for _ in range (4):
                eccentric_anomaly = eccentric_anomaly - (mean_anomaly - eccentric_anomaly + self.eccentricity*sin(eccentric_anomaly) ) / (-1 + self.eccentricity * cos(eccentric_anomaly) )
            
            #print (eccentric_anomaly, self.eccentricity)
            #true_anomaly = 2.0*atan(sqrt((1+self.eccentricity)/(1-self.eccentricity))*tan(eccentric_anomaly/2))
            e = self.eccentricity
            E = eccentric_anomaly
            true_anomaly = 2*atan2(sqrt(1-e)*cos(E/2), sqrt(1+e)*sin(E/2) )
            heliocentric_distance = self.semimajor_axis * (1 - e**2) / (1 + e*cos(true_anomaly) )
            samples.append((true_anomaly, heliocentric_distance))
        self.orbital_samples = samples

earth = OrbitalPath(1.33e20, 1, 1.67e-2, 7.16, 349, 114)

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

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()

        glTranslate(0,0,-2)

        glColor(1,1,1)
        glBegin(GL_LINE_LOOP)
        for (anomaly, r) in earth.orbital_samples:
            x = r * sin (anomaly)
            y = r * cos (anomaly)
            glVertex(x,y,0)
        glEnd()
            



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
    print earth.orbital_samples
    sys.exit(app.exec_() )

