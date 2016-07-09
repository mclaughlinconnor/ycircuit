from PyQt4 import QtCore, QtGui
import numpy


class Grid(QtGui.QGraphicsItem):
    """temp docstring for the Gridclass"""
    def __init__(self, parent=None, view=None, spacing=10):
        super(Grid, self).__init__()
        self.parent = parent
        self.view = view
        self.spacing = spacing
        self.displaySpacing = spacing
        self.xLength = 10000
        self.yLength = 10000
        self.xPoints = numpy.arange(-self.xLength, self.xLength, self.spacing)
        self.yPoints = numpy.arange(-self.yLength, self.yLength, self.spacing)

    def boundingRect(self):
        return self.scene().sceneRect()

    def paint(self, painter, *args):
        pen = QtGui.QPen()
        pen.setWidth(0.75*self.displaySpacing/self.spacing)
        painter.setPen(pen)
        for i in self.xDisplayPoints:
            for j in self.yDisplayPoints:
                self.point = QtCore.QPoint(i, j)
                painter.drawPoint(self.point)
        pen.setWidth(1.25*self.displaySpacing/self.spacing)
        painter.setPen(pen)
        for i in self.xDisplayPoints[self.xDisplayPoints % 100 == 0]:
            for j in self.yDisplayPoints[self.yDisplayPoints % 100 == 0]:
                self.point = QtCore.QPoint(i, j)
                painter.drawPoint(self.point)

    def createGrid(self, **kwargs):
        if 'spacing' in kwargs:
            self.spacing = kwargs['spacing']
        topLeft = self.view.mapToScene(self.view.rect().topLeft())
        bottomRight = self.view.mapToScene(self.view.rect().bottomRight())
        xL = int(topLeft.x()/self.displaySpacing)*self.displaySpacing
        xL = numpy.minimum(xL, 0)
        xH = int(bottomRight.x()/self.displaySpacing)*self.displaySpacing
        xH = numpy.maximum(xH, int(self.scene().sceneRect().width()))
        yL = int(topLeft.y()/self.displaySpacing)*self.displaySpacing
        yL = numpy.minimum(yL, 0)
        yH = int(bottomRight.y()/self.displaySpacing)*self.displaySpacing
        yH = numpy.maximum(yH, int(self.scene().sceneRect().height()))
        self.displaySpacing = self.spacing*(xH - xL)/1000
        if self.displaySpacing < self.spacing:
            self.displaySpacing = self.spacing
        self.xDisplayPoints = numpy.arange(xL, xH, self.displaySpacing)
        self.yDisplayPoints = numpy.arange(yL, yH, self.displaySpacing)

    def snapTo(self, point):
        newX = numpy.round(point.x()/self.spacing)*self.spacing
        newY = numpy.round(point.y()/self.spacing)*self.spacing
        return QtCore.QPointF(newX, newY)
