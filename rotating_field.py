from PySide import QtCore, QtGui, QtUiTools
from PySide.QtOpenGL import QGLWidget

class RotationData(object):
    def __init__(self):
        self.rotation = (0,0)
        self.relative_motion = None

class RotatingField(QGLWidget):
    def __init__(self):
        super(RotatingField, self).__init__()
        self.setMouseTracking(True)
        self.field_rotation = RotationData()

    def mousePressEvent(self, event):
        super(RotatingField, self)
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.field_rotation.relative_motion = (event.x(), event.y() )

    def mouseMoveEvent(self, event):
        super(RotatingField, self)
        if self.field_rotation.relative_motion != None:
            (x,y) = (event.x(), event.y() )
            (x0, y0) = self.field_rotation.relative_motion
            (dx, dy) = (x - x0, y - y0)

            (azimuth, elevation) = self.field_rotation.rotation
            self.field_rotation.rotation = (azimuth + dx, min(90, max(-90, elevation + dy) ) )

            self.field_rotation.relative_motion = (x,y)
            self.update()

    def mouseReleaseEvent(self, event):
        super(RotatingField, self)
        if event.button() == QtCore.Qt.MouseButton.RightButton:
            self.field_rotation.relative_motion = None





