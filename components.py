from PyQt4 import QtCore, QtGui
import numpy


class drawingElement(object):
    """Docstring for drawingElement"""
    def __init__(self, parent=None, start=None, **kwargs):
        super(drawingElement, self).__init__()
        self.parent = parent
        self.start = start
        self.localPen = QtGui.QPen()
        self.localBrush = QtGui.QBrush()
        self.setLocalPenOptions(**kwargs)
        self.setLocalBrushOptions(**kwargs)
        self.setFlag(self.ItemIsSelectable, True)
        self.setFlag(self.ItemIsFocusable, True)
        self.setAcceptHoverEvents(True)

    def __getstate__(self):
        localDict = self.__dict__
        localDict.pop('localPen', None)
        localDict.pop('localBrush', None)
        return localDict

    def __setstate__(self, state):
        state['localPen'] = QtGui.QPen()
        state['localBrush'] = QtGui.QBrush()
        self.__dict__ = state

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

    def opaqueArea(self):
        p = QtGui.QPainterPath()
        p.addRect(self.boundingRect())
        return p

    def hoverEnterEvent(self, event):
        self.localPen.setColor(QtGui.QColor('gray'))
        self.setPen(self.localPen)
        self.localBrush.setColor(QtGui.QColor('gray'))
        self.setBrush(self.localBrush)
        self.update()

    def hoverLeaveEvent(self, event):
        self.localPen.setColor(QtGui.QColor(self.localPenColour))
        self.setPen(self.localPen)
        self.localBrush.setColor(QtGui.QColor(self.localBrushColour))
        self.setBrush(self.localBrush)
        self.update()


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
        self.setAcceptHoverEvents(True)

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

    def __setstate__(self, state):
        self.__dict__ = state

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
            item.setAcceptHoverEvents(False)
        self.listOfItems = self.childItems()

    def reparentItems(self, newParent=None):
        for item in self.listOfItems:
            item.setParentItem(newParent)
            item.setFlag(item.ItemIsSelectable, True)
            item.setAcceptHoverEvents(True)
            if hasattr(item, 'origin'):
                item.setPos(self.pos() + item.origin)
                item.origin = item.pos()
            if not hasattr(item, 'localPen'):
                item.localPen = QtGui.QPen()
                item.setLocalPenOptions()
            if not hasattr(item, 'localBrush'):
                item.localBrush = QtGui.QBrush()
                item.setLocalBrushOptions()

    def setLocalPenOptions(self, **kwargs):
        for item in self.listOfItems:
            item.setLocalPenOptions(**kwargs)

    def setLocalBrushOptions(self, **kwargs):
        for item in self.listOfItems:
            item.setLocalBrushOptions(**kwargs)

    def hoverEnterEvent(self, event):
        # For some reason calling the children's hoverEnterEvent did not work
        for item in self.listOfItems:
            item.localPen.setColor(QtGui.QColor('gray'))
            item.setPen(item.localPen)
            item.localBrush.setColor(QtGui.QColor('gray'))
            item.setBrush(item.localBrush)
        self.update()

    def hoverLeaveEvent(self, event):
        # For some reason calling the children's hoverLeaveEvent did not work
        for item in self.listOfItems:
            item.localPen.setColor(QtGui.QColor(item.localPenColour))
            item.setPen(item.localPen)
            item.localBrush.setColor(QtGui.QColor(item.localBrushColour))
            item.setBrush(item.localBrush)
        self.update()

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
        drawingElement.__init__(self, parent, start, **kwargs)
        self.oldPath = self.path()
        if self.start is not None:
            self.setPos(self.start)

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

    def createCopy(self):
        newWire = super(Wire, self).createCopy()
        newWire.setPath(self.path())
        newWire.oldPath = newWire.path()
        if hasattr(self, 'origin'):
            newWire.origin = self.origin
        return newWire


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
        # Set the fixed vertex to (0, 0) in local coordinates
        drawingElement.__init__(self, parent, start=point, **kwargs)

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
        collidingItems = self.collidingItems()
        for item in collidingItems:
            if item.isObscuredBy(self):
                item.setZValue(item.zValue() + 1)

    def createCopy(self):
        newRectangle = super(Rectangle, self).createCopy()
        newRectangle.setRect(self.rect())
        newRectangle.oldRect = newRectangle.rect()
        if hasattr(self, 'origin'):
            newRectangle.origin = self.origin
        return newRectangle

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
        # Set the fixed vertex to (0, 0) in local coordinates
        drawingElement.__init__(self, parent, start=point, **kwargs)
        self.oldRect = self.rect()

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
        collidingItems = self.collidingItems()
        for item in collidingItems:
            if item.isObscuredBy(self):
                item.setZValue(item.zValue() + 1)

    def createCopy(self):
        newEllipse = super(Ellipse, self).createCopy()
        newEllipse.setRect(self.rect())
        newEllipse.oldRect = newEllipse.rect()
        if hasattr(self, 'origin'):
            newEllipse.origin = self.origin
        return newEllipse

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
        collidingItems = self.collidingItems()
        for item in collidingItems:
            if item.isObscuredBy(self):
                item.setZValue(item.zValue() + 1)

