from PyQt4 import QtCore, QtGui
import numpy


class drawingElement(object):
    """Docstring for drawingElement"""
    def __init__(self, parent=None):
        super(drawingElement, self).__init__()

    def __getstate__(self):
        localDict = self.__dict__
        localDict.pop('localPen', None)
        localDict.pop('localBrush', None)
        return localDict

    def __setstate__(self, state):
        state['localPen'] = QtGui.QPen()
        state['localBrush'] = QtGui.QBrush()
        self.__dict__ = state

    def defaultLocalPenBrushOptions(self):
        self.localPen = QtGui.QPen()
        self.localBrush = QtGui.QBrush()
        self.localPenWidth = 2
        self.localPen.setWidth(self.localPenWidth)
        self.localPenColour = 'black'
        self.localPen.setColor(QtGui.QColor(self.localPenColour))
        self.localPenStyle = 1
        self.localPen.setStyle(self.localPenStyle)
        self.localBrushColour = 'black'
        self.localBrush.setColor(QtGui.QColor(self.localBrushColour))
        self.localBrushStyle = 0
        self.localBrush.setStyle(self.localBrushStyle)
        if hasattr(self, 'setPen'):
            self.setPen(self.localPen)
        if hasattr(self, 'setBrush'):
            self.setBrush(self.localBrush)

    def setLocalPenOptions(self, **kwargs):
        # Necessary for objects with modified bounding rects
        self.prepareGeometryChange()
        if 'pen' in kwargs:
            self.localPen = kwargs['pen']
            self.localPenWidth = self.localPen.width()
            self.localPenColour = self.localPen.color()
            self.localPenStyle = self.localPen.style()
        if 'width' in kwargs:
            self.localPenWidth = kwargs['width']
        if 'penColour' in kwargs:
            self.localPenColour = kwargs['penColour']
        if 'penStyle' in kwargs:
            self.localPenStyle = kwargs['penStyle']
        self.localPen.setWidth(self.localPenWidth)
        self.localPen.setColor(QtGui.QColor(self.localPenColour))
        # self.localPen.setStyle(QtCore.Qt.PenStyle(self.localPenStyle))
        self.localPen.setStyle(self.localPenStyle)
        if hasattr(self, 'setPen'):
            self.setPen(self.localPen)

    def setLocalBrushOptions(self, **kwargs):
        # Necessary for objects with modified bounding rects
        self.prepareGeometryChange()
        if 'brush' in kwargs:
            self.localBrush = kwargs['brush']
            self.localBrushColour = self.localBrush.color()
            self.localBrushStyle = self.localBrush.style()
        if 'brushColour' in kwargs:
            self.localBrushColour = kwargs['brushColour']
        if 'brushStyle' in kwargs:
            self.localBrushStyle = kwargs['brushStyle']
        self.localBrush.setColor(QtGui.QColor(self.localBrushColour))
        self.localBrush.setStyle(self.localBrushStyle)
        if hasattr(self, 'setBrush'):
            self.setBrush(self.localBrush)

    def moveTo(self, xOffset, yOffset, status):
        if status == 'start':
            self.oldOriginX = self.x()
            self.oldOriginY = self.y()
            self.originX = self.x()
            self.originY = self.y()
        elif status == 'move':
            self.newOriginX = self.originX + xOffset
            self.newOriginY = self.originY + yOffset
            self.setX(self.newOriginX)
            self.setY(self.newOriginY)
        elif status == 'cancel':
            self.setX(self.oldOriginX)
            self.setY(self.oldOriginY)
        elif status == 'done':
            self.setX(self.newOriginX)
            self.setY(self.newOriginY)
            self.originX = self.newOriginX
            self.originY = self.newOriginY
            self.setSelected(False)
            return
        self.setSelected(True)

    def modifyMoveOrigin(self, startPos, mode='r', moving=False):
        if moving is True:
            if mode == 'R':
                self.originX = 2*startPos.x() - self.originX
            elif mode == 'r':
                self.originX, self.originY = startPos.x() - self.originY +\
                                             startPos.y(),\
                                             startPos.y() + self.originX -\
                                             startPos.x()
            self.moveTo(0, 0, 'move')

    def createCopy(self):
        if self.isSelected() is True:
            self.setSelected(False)
        _start = self.pos()
        newItem = self.__class__(None, _start, pen=self.localPen, brush=self.localBrush)
        newItem.setTransform(self.transform())
        self.scene().addItem(newItem)
        newItem.setSelected(True)
        newItem.moveTo(0, 0, 'start')
        return newItem


class myGraphicsItemGroup(QtGui.QGraphicsItem, drawingElement):
    """Subclassed from QGraphicsItem. Provides additional methods so that
    the parent item remembers all the items that are its children."""
    def __init__(self, parent=None, scene=None, start=None, listOfItems=None):
        super(myGraphicsItemGroup, self).__init__(parent, scene)
        self.listOfItems = listOfItems
        self.setFlag(self.ItemIsSelectable, True)
        self.setFlag(self.ItemIsFocusable, True)
        if start is not None:
            self.setPos(start)
        # The pen and brush options are just place holders
        self.localPenWidth = 2
        self.localPenColour = 'black'
        self.localPenStyle = 1
        self.localBrushColour = 'black'
        self.localBrushStyle = 0

    def paint(self, painter, *args):
        if not isinstance(self.parentItem(), myGraphicsItemGroup):
            if self.isSelected() is True:
                pen = QtGui.QPen()
                pen.setStyle(2)
                painter.setPen(pen)
                painter.drawRect(self.boundingRect())

    def boundingRect(self):
        rect = self.listOfItems[0].sceneBoundingRect()
        for item in self.listOfItems:
            rect = rect.united(item.sceneBoundingRect())
        return self.mapRectFromScene(rect)

    def createCopy(self):
        if self.isSelected() is True:
            self.setSelected(False)
        _start = self.pos()
        newItem = self.__class__(None, self.scene(), _start)
        newItem.listOfItems = []
        for item in self.listOfItems:
            itemCopy = item.createCopy()
            newItem.listOfItems.append(itemCopy)
        newItem.setItems(newItem.listOfItems)
        newItem.setTransform(self.transform())
        # self.scene().addItem(newItem)
        newItem.setSelected(True)
        newItem.moveTo(0, 0, 'start')
        return newItem

    def setItems(self, listOfItems):
        for item in listOfItems:
            item.setParentItem(self)
            if hasattr(item, 'origin'):
                item.setPos(item.origin)
            if hasattr(item, 'transformData'):
                item.setTransform(item.transformData)
            item.setFlag(item.ItemIsSelectable, False)
        self.listOfItems = self.childItems()

    def reparentItems(self, newParent=None):
        for item in self.listOfItems:
            # Remove item and add it again to avoid item being randomly removed
            # self.scene().removeItem(item)
            # self.scene().addItem(item)
            item.setParentItem(newParent)
            item.setFlag(item.ItemIsSelectable, True)
            if hasattr(item, 'origin'):
                item.setPos(self.pos() + item.origin)
                item.origin = item.pos()

    def __setstate__(self, state):
        self.__dict__ = state

    def setLocalPenOptions(self, **kwargs):
        for item in self.listOfItems:
            item.setLocalPenOptions(**kwargs)

    def setLocalBrushOptions(self, **kwargs):
        for item in self.listOfItems:
            item.setLocalBrushOptions(**kwargs)

    def loadItems(self, mode='symbol'):
        for item in self.listOfItems:
            if not isinstance(item, myGraphicsItemGroup):
                item.__init__(self, item.origin, penColour=item.localPenColour, width=item.localPenWidth, penStyle=item.localPenStyle, brushColour=item.localBrushColour, brushStyle=item.localBrushStyle)
            else:
                # item.__init__(self, self.scene(), QtCore.QPointF(0, 0), item.listOfItems)
                item.__init__(self, self.scene(), item.origin, item.listOfItems)
                # item.loadItems(mode)
                # item.setPos(item.origin)
                item.loadItems(mode)
                # item.setPos(item.origin)
            # self.addToGroup(item)
            # item.setParentItem(self)
        self.setItems(self.listOfItems)


class Wire(QtGui.QGraphicsPathItem, drawingElement):
    """Subclassed from the PyQt implementation of standard lines. Provides some
    added convenience functions and enables object-like interaction"""
    def __init__(self, parent=None, start=None, **kwargs):
        point = QtCore.QPointF(0, 0)
        if not hasattr(self, 'oldPath'):
            super(Wire, self).__init__(QtGui.QPainterPath(point), parent)
        else:
            super(Wire, self).__init__(self.oldPath, parent)
        self.oldPath = self.path()
        self.parent = parent
        self.start = start
        # self.defaultLocalPenBrushOptions()
        self.localPen = QtGui.QPen()
        self.localBrush = QtGui.QBrush()
        self.setLocalPenOptions(**kwargs)
        self.setLocalBrushOptions(**kwargs)
        self.setFlag(self.ItemIsSelectable, True)
        self.setFlag(self.ItemIsFocusable, True)
        if self.start is not None:
            self.setPos(self.start)

    # def boundingRect(self):
    #     rect = super(Wire, self).boundingRect()
    #     if self.line().p1().x() == self.line().p2().x():
    #         rect.setWidth(10 + rect.width())
    #         rect.translate(-5, 0)
    #     elif self.line().p1().y() == self.line().p2().y():
    #         rect.setHeight(10 + rect.height())
    #         rect.translate(0, -5)
    #     return rect

    def updateWire(self, newEnd):
        newEnd = self.mapFromScene(newEnd)
        self.setPath(self.oldPath)
        path = self.path()
        path.lineTo(newEnd)
        self.setPath(path)

    def createSegment(self, newEnd):
        newEnd = self.mapFromScene(newEnd)
        self.oldPath.lineTo(newEnd)
        self.setPath(self.oldPath)

    def cancelSegment(self):
        self.setPath(self.oldPath)

    # def contextMenuEvent(self, event):
    #     menu = QtGui.QMenu()
    #     actionDelete = menu.addAction('&Delete')
    #     actionDelete.triggered.connect(lambda: self.scene().removeItem(self))
    #     menu.exec_(event.screenPos())

    def createCopy(self):
        newWire = super(Wire, self).createCopy()
        newWire.setPath(self.path())
        newWire.oldPath = newWire.path()
        if hasattr(self, 'origin'):
            newWire.origin = self.origin
        return newWire

    def __getstate__(self):
        localDict = super(Wire, self).__getstate__()
        polyPathList = self.oldPath.toSubpathPolygons()
        polyPathPointList = []
        for poly in polyPathList:
            polyPathPointList.append([poly.at(i) for i in range(poly.count())])
        localDict['polyPathPointList'] = polyPathPointList
        return localDict

    def __setstate__(self, state):
        state['localPen'] = QtGui.QPen()
        state['localBrush'] = QtGui.QBrush()
        self.__dict__ = state
        a = QtGui.QPolygonF(state['polyPathPointList'][0])
        self.oldPath2 = QtGui.QPainterPath()
        for item in state['polyPathPointList']:
            poly = QtGui.QPolygonF(item)
            self.oldPath2.addPolygon(poly)
        self.oldPath = self.__dict__.pop('oldPath2', None)

    # def keyReleaseEvent(self, event):
    #     super(Wire, self).keyReleaseEvent(event)
    #     keyPressed = event.key()


class Rectangle(QtGui.QGraphicsRectItem, drawingElement):
    """docstring for Rectangle"""
    def __init__(self, parent=None, start=None, **kwargs):
        point = QtCore.QPointF(0, 0)
        rect = QtCore.QRectF(point, point)
        if not hasattr(self, 'oldRect'):
            super(Rectangle, self).__init__(rect, parent)
            self.setPos(start)
        else:
            super(Rectangle, self).__init__(self.oldRect, parent)
            self.setPos(self.origin)
        self.oldRect = self.rect()
        self.parent = parent
        # Set the fixed vertex to (0, 0) in local coordinates
        self.start = point
        self.localPen = QtGui.QPen()
        self.localBrush = QtGui.QBrush()
        self.setLocalPenOptions(**kwargs)
        self.setLocalBrushOptions(**kwargs)
        self.setFlag(self.ItemIsSelectable, True)
        self.setFlag(self.ItemIsFocusable, True)

    def boundingRect(self):
        pad = 10
        bottomLeft = self.rect().bottomLeft() + QtCore.QPointF(-pad, pad)
        topRight = self.rect().topRight() + QtCore.QPointF(pad, -pad)
        rect = QtCore.QRectF(bottomLeft, topRight)
        return rect

    def paint(self, painter, *args):
        # super(Rectangle, self).paint(painter, *args)
        if self.isSelected() is False:
            super(Rectangle, self).paint(painter, *args)
        else:
            pen = QtGui.QPen()
            pen.setStyle(2)
            painter.setPen(pen)
            painter.drawRect(self.boundingRect())
            painter.setPen(self.localPen)
            painter.setBrush(self.localBrush)
            painter.drawRect(self.rect())

    def updateRectangle(self, end):
        end = self.mapFromScene(end)
        rect = QtCore.QRectF(self.start, end)
        self.setRect(rect)
        self.oldRect = rect

    def mouseReleaseEvent(self, event):
        # Necessary so that bounding rect is drawn correctly
        self.prepareGeometryChange()
        super(Rectangle, self).mouseReleaseEvent(event)


class Ellipse(QtGui.QGraphicsEllipseItem, drawingElement):
    """docstring for Ellipse"""
    def __init__(self, parent=None, start=None, **kwargs):
        point = QtCore.QPointF(0, 0)
        rect = QtCore.QRectF(point, point)
        if not hasattr(self, 'oldRect'):
            super(Ellipse, self).__init__(rect, parent)
            self.setPos(start)
        else:
            super(Ellipse, self).__init__(self.oldRect, parent)
            self.setPos(self.origin)
        self.oldRect = self.rect()
        self.parent = parent
        # Set the fixed vertex to (0, 0) in local coordinates
        self.start = point
        self.localPen = QtGui.QPen()
        self.localBrush = QtGui.QBrush()
        self.setLocalPenOptions(**kwargs)
        self.setLocalBrushOptions(**kwargs)
        self.setFlag(self.ItemIsSelectable, True)
        self.setFlag(self.ItemIsFocusable, True)

    def boundingRect(self):
        pad = 10
        # Not sure why this is different from the Rectangle boundingRect
        bottomLeft = self.rect().bottomLeft() + QtCore.QPointF(-pad, -pad)
        topRight = self.rect().topRight() + QtCore.QPointF(pad, pad)
        rect = QtCore.QRectF(bottomLeft, topRight)
        return rect

    def paint(self, painter, *args):
        # super(Rectangle, self).paint(painter, *args)
        if self.isSelected() is False:
            super(Ellipse, self).paint(painter, *args)
        else:
            pen = QtGui.QPen()
            pen.setStyle(2)
            painter.setPen(pen)
            painter.drawRect(self.boundingRect())
            painter.setPen(self.localPen)
            painter.setBrush(self.localBrush)
            painter.drawEllipse(self.rect())

    def updateEllipse(self, end):
        end = self.mapFromScene(end)
        rect = QtCore.QRectF(self.start, end)
        self.setRect(rect)
        self.oldRect = rect

    def mouseReleaseEvent(self, event):
        # Necessary so that bounding rect is drawn correctly
        self.prepareGeometryChange()
        super(Ellipse, self).mouseReleaseEvent(event)


class Circle(Ellipse):
    """docstring for Circle"""
    def __init__(self, parent=None, start=None, **kwargs):
        super(Circle, self).__init__(parent, start, **kwargs)

    def boundingRect(self):
        pad = 10
        # This is the same as that for rectangle
        bottomLeft = self.rect().bottomLeft() + QtCore.QPointF(-pad, pad)
        topRight = self.rect().topRight() + QtCore.QPointF(pad, -pad)
        rect = QtCore.QRectF(bottomLeft, topRight)
        return rect

    def updateCircle(self, end):
        distanceLine = end - self.mapToScene(self.start)
        if distanceLine.x() == 0:
            if distanceLine.y() < 0:
                theta = 270
            elif distanceLine.y() > 0:
                theta = 90
            else:
                theta = 0
        elif distanceLine.y() == 0:
            if distanceLine.x() < 0:
                theta = 180
            elif distanceLine.x() > 0:
                theta = 0
            else:
                theta = 0
        else:
            theta = 180/numpy.pi*numpy.arctan2(distanceLine.y(), distanceLine.x())
        sideLength = numpy.sqrt(distanceLine.x()**2 + distanceLine.y()**2)
        square = QtCore.QRectF(self.start + QtCore.QPointF(0, -sideLength/2), QtCore.QSizeF(sideLength, sideLength))
        self.setRect(square)
        self.setTransformOriginPoint(self.start)
        self.setRotation(theta)
        self.oldRect = self.rect()


class Dot(QtGui.QGraphicsEllipseItem, drawingElement):
    """docstring for Dot"""
    def __init__(self, parent=None, start=0, **kwargs):
        if 'width' not in kwargs:
            diameter = 10
        else:
            diameter = 5*kwargs['width']
        if hasattr(self, 'diameter'):
            diameter = self.diameter
        rect = QtCore.QRectF(-diameter/2., -diameter/2., diameter, diameter)
        super(Dot, self).__init__(rect)
        self.setRect(rect)
        self.parent = parent
        self.start = start
        self.diameter = diameter
        # self.defaultLocalPenBrushOptions()
        # kwargs['brushStyle'] = 1
        self.localPen = QtGui.QPen()
        self.localBrush = QtGui.QBrush()
        self.setLocalPenOptions(**kwargs)
        self.setLocalBrushOptions(**kwargs)
        self.setFlag(self.ItemIsSelectable, True)
        self.setFlag(self.ItemIsFocusable, True)
        self.setZValue(1000)  # Always click on dot first
        self.setPos(self.start)

    def boundingRect(self):
        rect = super(Dot, self).boundingRect()
        rect.setWidth(rect.width() + 2)
        rect.setHeight(rect.height() + 2)
        rect.translate(-1, -1)
        return rect

    def mouseReleaseEvent(self, event):
        super(Dot, self).mouseReleaseEvent(event)
        self.setFocus(QtCore.Qt.MouseFocusReason)


class Transistor(QtGui.QGraphicsPathItem, drawingElement):
    """Docstring for Transistor"""
    def __init__(self, parent=None, start=None, kind='MOS', polarity='N', arrow=False, **kwargs):
        super(Transistor, self).__init__(QtGui.QPainterPath())
        self.parent = parent
        self.start = start
        path = self.path()

        if kind == 'MOS':
            if polarity == 'N':
                self.vertices = [[[0, 0], [40,0], [40, -50], [40, 50]],
                                 [[120, -110], [120, -50], [60, -50], [60, 50],
                                  [120, 50], [120, 110]]]
                if arrow is True:
                    self.arrowVertices = [[100, 40], [120, 50], [100, 60]]
            elif polarity == 'P':
                self.vertices = [[[0, 0], [20,0]],
                                 [[40, 0], [40, -50], [40, 50]],
                                 [[120, -110], [120, -50], [60, -50], [60, 50],
                                  [120, 50], [120, 110]]]
                if arrow is True:
                    self.vertices[0][1][0] = 40
                    self.arrowVertices = [[80, -40], [60, -50], [80, -60]]
                else:
                    path.addEllipse(QtCore.QRectF(20, -10, 20, 20))

        if arrow is True:
            self.arrowVertices = QtGui.QPolygonF([QtCore.QPointF(self.arrowVertices[i][0], self.arrowVertices[i][1]) for i in range(len(self.arrowVertices))])

        for i in range(len(self.vertices)):
            for j in range(len(self.vertices[i])):
                self.vertices[i][j] = QtCore.QPointF(self.vertices[i][j][0], self.vertices[i][j][1])

        for i in range(len(self.vertices)):
            path.moveTo(self.vertices[i][0])
            for j in range(len(self.vertices[i])):
                path.lineTo(self.vertices[i][j])
        self.setPath(path)
        self.defaultLocalPenBrushOptions()
        self.setLocalPenOptions(**kwargs)
        self.setLocalBrushOptions(**kwargs)
        self.setFlag(self.ItemIsSelectable, True)
        self.setFlag(self.ItemIsFocusable, True)
        self.setPos(self.start)

    def paint(self, painter, *args):
        super(Transistor, self).paint(painter, *args)
        if hasattr(self, 'arrowVertices'):
            painter.setPen(self.localPen)
            brush = QtGui.QBrush()
            brush.setColor(QtGui.QColor(self.localPenColour))
            brush.setStyle(1)
            painter.setBrush(brush)
            painter.drawPolygon(self.arrowVertices)

    def setLocalBrushOptions(self, **kwargs):
        # Override brush options for MOSFET
        pass
