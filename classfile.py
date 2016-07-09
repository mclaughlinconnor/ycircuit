from PyQt4 import QtCore, QtGui


class DrawingArea2(QtGui.QGraphicsView):
    """temp docstring"""
    def __init__(self, parent=None):
        super(myView, self).__init__(parent)
        self.setScene(QtGui.QGraphicsScene(self))
        self.setSceneRect(QtCore.QRectF(self.viewport().rect()))
        # self.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)
        self._pressed = False
        self.controlPressed = False

    def keyPressEvent(self, event):
        keyPressed = event.key()
        if (keyPressed == QtCore.Qt.Key_Control):
            self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
            self.controlPressed = True

    def keyReleaseEvent(self, event):
        keyPressed = event.key()
        if (keyPressed == QtCore.Qt.Key_Control):
            self.setDragMode(QtGui.QGraphicsView.NoDrag)
            self.controlPressed = False

    def mousePressEvent(self, event):
        self.currentPos = event.pos()
        self.currentX = event.x()
        self.currentY = event.y()
        self._pressed = True

    def mouseReleaseEvent(self, event):
        self._pressed = False
        self.oldPos = self.currentPos
        self.currentPos = event.pos()
        self.drawLine()

    def drawLine(self):
        start = QtCore.QPointF(self.mapToScene(self.oldPos))
        end = QtCore.QPointF(self.mapToScene(self.currentPos))
        self.scene().\
            addItem(QtGui.QGraphicsLineItem(QtCore.QLineF(start, end)))
        # for point in (start, end):
        #     text = self.scene()\
        #         .addSimpleText('(%d, %d)' % (point.x(), point.y()))
        #     text.setBrush(QtCore.Qt.red)
        #     text.setPos(point)

    def mouseMoveEvent(self, event):
        if (self._pressed is True):
            self.oldPos = self.currentPos
            self.currentPos = event.pos()
            self.oldX = self.currentX
            self.oldY = self.currentY
            self.currentX = event.x()
            self.currentY = event.y()
            if (self.controlPressed is False):
                self.drawLine()
            else:
                print self.currentX - self.oldX, self.currentY - self.oldY
                self.translate(self.currentX - self.oldX,
                               self.currentY - self.oldY)
                # self.translate(self.currentX, self.currentY)

    def wheelEvent(self, event):
        scaleFactor = -event.delta()/240.
        if scaleFactor < 0:
            scaleFactor = -1/scaleFactor
        self.scale(scaleFactor, scaleFactor)
