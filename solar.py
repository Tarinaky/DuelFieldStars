from PySide import QtCore, QtGui, QtUiTools
from PySide.QtOpenGL import QGLWidget

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *

from math import *

from rotating_field import RotatingField

class OrbitalPath(object):
    def __init__(self, gravitational_parameter, semimajor_axis, eccentricity,
            inclination, longtitude_of_ascending_node,
            argument_of_periapsis):
        self.gravitational_parameter = float(gravitational_parameter) # In m^3/s^2
        self.semimajor_axis = float(semimajor_axis) # In Au, or 150e9m
        self.eccentricity = float(eccentricity) # Less than 1.
        self.inclination = float(inclination) # Degrees from sun's equator
        self.longtitude_of_ascending_node = float(longtitude_of_ascending_node) # Degrees
        self.argument_of_periapsis = float(argument_of_periapsis) # Not implemented. Degrees
        self.period = 2.0*pi*sqrt((150e9 * self.semimajor_axis)**3 / self.gravitational_parameter)

        self.sample_orbit()

    def true_anomaly(self, time):
        n = 1.0/self.period
        mean_anomaly = float(2*pi*time*n)
        eccentric_anomaly = mean_anomaly
        for _ in range(4):
            eccentric_anomaly = eccentric_anomaly - (mean_anomaly - eccentric_anomaly + self.eccentricity*sin(eccentric_anomaly) ) / (-1 + self.eccentricity * cos(eccentric_anomaly) )
            
        e = self.eccentricity
        E = eccentric_anomaly
        return 2*atan2(sqrt(1-e)*cos(E/2), sqrt(1+e)*sin(E/2) )

    def heliocentric_distance(self, true_anomaly):
        e = self.eccentricity
        return self.semimajor_axis * (1 - e**2) / (1 + e*cos(true_anomaly) )

    def cartesian(self, true_anomaly, r):
        x = r * cos(true_anomaly+self.argument_of_periapsis)
        y = r * sin(true_anomaly+self.argument_of_periapsis)
        z = 0
        
        #Inclination / rotation about x-axis
        inclination = self.inclination/180*pi
        (x,y,z) = (x,
                y*cos(inclination) - z*sin(inclination),
                y*sin(inclination) + z*cos(inclination) )
        #longitude of ascending node / rotation about z-axis
        node = self.longtitude_of_ascending_node/180*pi
        (x,y,z) = (x*cos(node) - y*sin(node),
                x*sin(node) + y*cos(node),
                z)

        return (x,y,z)

    def sample_orbit(self):
        weeks = max(1,int(floor(self.period /(3600*168))) )
        week_length = self.period/weeks
        samples = []
        
        n = 1.0/self.period
        for i in range (weeks):
            time = i * week_length
            true_anomaly = self.true_anomaly(time)
            radius = self.heliocentric_distance(true_anomaly)
            samples.append((true_anomaly, radius))
        self.orbital_samples = samples

earth = OrbitalPath(1.33e20, 1, 1.67e-2, 7.16, 349, 114)

class SolarWidget(RotatingField):
    def __init__(self):
        super(SolarWidget, self).__init__()
        self.setMouseTracking(True)
        
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
        #Rotation
        (azimuth, elevation) = self.field_rotation.rotation
        glRotate(-elevation, float(1), 0, 0)
        glRotate(-azimuth, 0, float(1), 0)

        
        glColor(1,1,1)
        glBegin(GL_LINE_LOOP)
        for (anomaly, r) in earth.orbital_samples:
            (x,y,z) = earth.cartesian(anomaly,r)
            glVertex(x,y,z)
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

