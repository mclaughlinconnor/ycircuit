from PyQt5 import QtCore, QtGui, QtWidgets
import math
import pickle
from src.drawingitems import TextEditor


class drawingElement(object):
    """The drawingElement forms part of the basis for all drawing classes.
    It contains methods for setting pen and brush options, moving, copying etc.
    """

    def __init__(self, parent=None, start=None):
        super().__init__()
        self.parent = parent
        self.start = start
        self.localPen = QtGui.QPen()
        self.localBrush = QtGui.QBrush()
        self.setFlag(self.ItemIsSelectable, True)
        self.setFlag(self.ItemIsFocusable, True)
        self.setAcceptHoverEvents(True)
        self.setToolTip(str(self))
        if hasattr(self, 'height'):
            self.setZValue(self.height)
        else:
            self.setZValue(0)

    def __getstate__(self):
        """Pen and brush objects are not picklable so remove them"""
        localDict = self.__dict__
        # Create copy of localDict and return that so that autosave does not
        # remove important required properties
        localDictCopy = localDict.copy()
        localDictCopy.pop('localPen', None)
        localDictCopy.pop('localBrush', None)
        localDictCopy['transformData'] = self.transform()
        localDictCopy['height'] = self.zValue()
        return localDictCopy

    def __setstate__(self, state):
        """Since pen and brush objects were removed, we need to add them back"""
        state['localPen'] = QtGui.QPen()
        state['localBrush'] = QtGui.QBrush()
        self.__dict__ = state

    def setLocalPenOptions(self, **kwargs):
        """Sets pen options for the current object.
        The following keyword arguments are accepted:
        pen: QtGui.QPen instance of a pen
        width: int specifying width of the line to be drawn
        penColour: string specifying colour of the line to be drawn
        penStyle: int specifying style of the line to be drawn
        """
        # Necessary for objects with modified bounding rects
        # self.prepareGeometryChange()
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
        self.localPen.setJoinStyle(QtCore.Qt.RoundJoin)
        if hasattr(self, 'setPen'):
            self.setPen(self.localPen)

    def setLocalBrushOptions(self, **kwargs):
        """Sets brush options for the current object.
        The following keyword arguments are accepted:
        brush: QtGui.QBrush instance of a brush
        brushColour: string specifying colour of the fill
        brushStyle: int specifying style of the fill
        """
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

    def moveTo(self, newPoint, status):
        """Move by changing the pos of the item relative to the origin"""
        if status == 'start':
            self.oldPos = self.pos()
            self.origin = newPoint - self.oldPos
        elif status == 'move':
            if self.parentItem() is not None:
                self.setPos(self.mapFromParent(newPoint) - self.origin)
            else:
                self.setPos(newPoint - self.origin)
        elif status == 'done':
            if self.parentItem() is not None:
                self.setPos(self.mapFromParent(newPoint) - self.origin)
            else:
                self.setPos(newPoint - self.origin)
            self.transformData = self.transform()
            self.setSelected(False)
        elif status == 'cancel':
            self.transformData = self.transform()
            self.setPos(self.oldPos)
        self.setSelected(True)

    def rotateBy(self, moving, origin, angle):
        """Rotate using the item's transformation matrix instead of the
        deprecated QGraphicsItem.rotate() function
        """
        transform_ = self.transform()
        if hasattr(self, 'reflections'):
            if self.reflections != 0:
                angle = -angle
        if moving is True:
            # origin = self.mapFromScene(origin)
            origin = origin
        else:
            origin = QtCore.QPointF(0, 0)
        transform_.translate(origin.x(), origin.y())
        transform_.rotate(angle)
        transform_.translate(-origin.x(), -origin.y())
        self.setTransform(transform_)
        self.transformData = self.transform()  # Backwards compatibility

    def reflect(self, moving, origin):
        """Mirror using the item's transformation matrix instead of the
        deprecated QGraphicsItem.scale() function
        """
        if not hasattr(self, 'reflections'):
            # The first time this is called, reflections will be 1
            self.reflections = 1
        else:
            self.reflections += 1
            self.reflections %= 2
        transform_ = self.transform()
        if moving is True:
            # origin = self.mapFromScene(origin)
            origin = origin
        else:
            origin = QtCore.QPointF(0, 0)
        transform_.translate(origin.x(), origin.y())
        rotation_ = 180 / math.pi * math.atan2(-transform_.m21(),
                                                   transform_.m11())
        transform_.rotate(-rotation_)
        transform_.scale(-1, 1)
        transform_.rotate(rotation_)
        transform_.translate(-origin.x(), -origin.y())
        self.setTransform(transform_)
        self.transformData = self.transform()  # Backwards compatibility

    def createCopy(self, parent=None):
        # Deselect item
        if self.isSelected() is True:
            self.setSelected(False)
        _start = self.pos()
        # Create copy with same pen and brush and start location
        # Manually add pen and brush colours because these are stored as strings
        # as opposed to the #RRGGBB format that QColor.color() returns
        newItem = self.__class__(
            parent,
            _start,
            pen=self.localPen,
            brush=self.localBrush,
            penColour=self.localPenColour,
            brushColour=self.localBrushColour)
        # Apply any transforms (rotations, reflections etc.)
        newItem.setTransform(self.transform())
        # Copy reflection info if it exists
        if hasattr(self, 'reflections'):
            newItem.reflections = self.reflections
        if hasattr(self, 'height'):
            newItem.height = self.height
            newItem.setZValue(newItem.height)
        if parent is None:
            # Add new item to scene if no parent exists
            self.scene().addItem(newItem)
        # Select item
        newItem.setSelected(True)
        newItem.moveTo(self.scenePos(), 'start')
        return newItem

    def opaqueArea(self):
        p = QtGui.QPainterPath()
        p.addRect(self.boundingRect())
        return p

    def hoverEnterEvent(self, event):
        """Turns the item gray when mouse enters its bounding rect"""
        self.lightenColour(True)

    def hoverLeaveEvent(self, event):
        """Restores the item's original pen and brush when mouse leaves
        its bounding rect
        """
        self.lightenColour(False)

    def lightenColour(self, lighten=False):
        # For some reason, after creating a symbol, localPen and localBrush get
        # deleted. Check to see if they exist, and create them if they don't
        if not hasattr(self, 'localPen'):
            self.localPen = QtGui.QPen()
            self.setLocalPenOptions()
        if not hasattr(self, 'localBrush'):
            self.localBrush = QtGui.QBrush()
            self.setLocalBrushOptions()
        pen = QtGui.QPen(self.localPen)
        brush = QtGui.QBrush(self.localBrush)
        if lighten == True:
            penColour = self.localPen.color().lighter()
            brushColour = self.localBrush.color().lighter()
            if penColour == QtGui.QColor('black'):
                penColour = QtGui.QColor('grey')
            if brushColour == QtGui.QColor('black'):
                brushColour = QtGui.QColor('grey')
            pen.setColor(penColour)
            brush.setColor(brushColour)
        self.setPen(pen)
        if hasattr(self, 'setBrush'):
            self.setBrush(brush)

    def undoEdit(self):
        """Handled by classes individually"""
        pass

    def redoEdit(self, point=None, **kwargs):
        """Handled by classes individually"""
        pass


class myGraphicsItemGroup(QtWidgets.QGraphicsItem, drawingElement):
    """Subclassed from QGraphicsItem. Provides additional methods so that
    the parent item remembers all the items that are its children.
    """

    def __init__(self, parent=None, start=None, listOfItems=None, **kwargs):
        super().__init__(parent=parent, start=start)
        self.listOfItems = listOfItems
        if 'mode' in kwargs:
            self.loadItems(**kwargs)
        if self.listOfItems != []:
            self.setItems(self.listOfItems)
            self.setLocalPenOptions(**kwargs)
            self.setLocalBrushOptions(**kwargs)
        self.setFlag(self.ItemIsSelectable, True)
        self.setFlag(self.ItemIsFocusable, True)
        if start is not None:
            self.start = start
            self.setPos(start)
        # The pen and brush options are just place holders
        self.localPenWidth = 2
        self.localPenColour = 'black'
        self.localPenStyle = 1
        self.localBrushColour = 'black'
        self.localBrushStyle = 0
        self.setAcceptHoverEvents(True)

    def __setstate__(self, state):
        """Reimplemented from drawingElement because group does not have
        pen and brush of its own.
        """
        self.__dict__ = state

    def paint(self, painter, *args):
        """Call child paint methods individually"""
        if not isinstance(self.parentItem(), myGraphicsItemGroup):
            if self.isSelected() is True:
                pen = QtGui.QPen()
                pen.setStyle(2)
                painter.setPen(pen)
                painter.drawRect(self.boundingRect())

    def boundingRect(self):
        return self.childrenBoundingRect()

    def createCopy(self, parent=None):
        """Call child copy methods individually after creating new parent"""
        self.setSelected(False)
        _start = self.pos()
        newItem = self.__class__(parent, _start, [])
        newItem.origin = self.origin
        newItem.setTransform(self.transform())
        # Copy reflection info if it exists
        if hasattr(self, 'reflections'):
            newItem.reflections = self.reflections
        if hasattr(self, 'height'):
            newItem.height = self.height
            newItem.setZValue(newItem.height)
        if newItem.parentItem() is None:
            self.scene().addItem(newItem)
            newItem.moveTo(self.scenePos(), 'start')
        else:
            newItem.setPos(newItem.origin)
        for item in self.listOfItems:
            itemCopy = item.createCopy(newItem)
            newItem.listOfItems.append(itemCopy)
        newItem.setItems(newItem.listOfItems)
        newItem.setSelected(True)
        return newItem

    def setItems(self, listOfItems):
        """Add all items in listOfItems as children"""
        for item in listOfItems:
            item.setParentItem(self)
            # For when children are being loaded from a file
            if hasattr(item, 'origin'):
                item.setPos(item.origin)
            if hasattr(item, 'transformData'):
                item.setTransform(item.transformData)
            item.setFlag(item.ItemIsSelectable, False)
            item.setAcceptHoverEvents(False)
        self.listOfItems = self.childItems()

    def reparentItems(self, newParent=None):
        """Sets parent of all child items to newParent"""
        # Call prepareGeometryChange because the bounding rect for this
        # item is going to change
        self.prepareGeometryChange()
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

    def getLocalPenParameters(self, parameter='colour'):
        widthList = []
        penColourList = []
        penStyleList = []
        for item in self.listOfItems:
            if item.localPen.width() not in widthList:
                widthList.append(item.localPen.width())
            if item.localPen.color() not in penColourList:
                penColourList.append(item.localPen.color())
            if item.localPen.style() not in penStyleList:
                penStyleList.append(item.localPen.style())
        if parameter == 'width':
            if len(widthList) > 1:
                return None
            else:
                return widthList[0]
        if parameter == 'colour':
            if len(penColourList) > 1:
                return None
            else:
                return penColourList[0]
        if parameter == 'style':
            if len(penStyleList) > 1:
                return None
            else:
                return penStyleList[0]

    def setLocalPenOptions(self, **kwargs):
        """Set pen individually for each child item"""
        self.prepareGeometryChange()
        if hasattr(self, 'listOfItems'):
            for item in self.listOfItems:
                if not hasattr(item, 'localPen'):
                    item.localPen = QtGui.QPen()
                item.setLocalPenOptions(**kwargs)

    def getLocalBrushParameters(self, parameter='colour'):
        brushColourList = []
        brushStyleList = []
        for item in self.listOfItems:
            if item.localBrush.color() not in brushColourList:
                brushColourList.append(item.localBrush.color())
            if item.localBrush.style() not in brushStyleList:
                brushStyleList.append(item.localBrush.style())
        if parameter == 'colour':
            if len(brushColourList) > 1:
                return None
            else:
                return brushColourList[0]
        if parameter == 'style':
            if len(brushStyleList) > 1:
                return None
            else:
                return brushStyleList[0]

    def setLocalBrushOptions(self, **kwargs):
        """Set brush individually for each child item"""
        self.prepareGeometryChange()
        if hasattr(self, 'listOfItems'):
            for item in self.listOfItems:
                if not hasattr(item, 'localBrush'):
                    item.localBrush = QtGui.QBrush()
                item.setLocalBrushOptions(**kwargs)

    def hoverEnterEvent(self, event):
        self.lightenColour(True)

    def hoverLeaveEvent(self, event):
        self.lightenColour(False)

    def lightenColour(self, lighten=False):
        for item in self.listOfItems:
            item.lightenColour(lighten)

    def loadItems(self, mode='symbol'):
        """Initializes items in self.listOfItems."""
        for item in self.listOfItems:
            if not isinstance(item, myGraphicsItemGroup):
                item.__init__(
                    self,
                    item.origin,
                    penColour=item.localPenColour,
                    width=item.localPenWidth,
                    penStyle=item.localPenStyle,
                    brushColour=item.localBrushColour,
                    brushStyle=item.localBrushStyle)
            else:
                item.__init__(
                    self, item.origin, item.listOfItems, mode='symbol')
                # Call loadItems if item is also a myGraphicsItemGroup
                # item.loadItems(mode)
        self.setItems(self.listOfItems)

    def undoEdit(self):
        for item in self.listOfItems:
            item.undoEdit()

    def redoEdit(self, point=None, **kwargs):
        for item in self.listOfItems:
            item.redoEdit(point, **kwargs)


class Wire(QtWidgets.QGraphicsPathItem, drawingElement):
    """Subclassed from the PyQt implementation of standard lines. Provides some
    added convenience functions and enables object-like interaction"""
    def __init__(self, parent=None, start=None, **kwargs):
        point = QtCore.QPointF(0, 0)
        # For when wire is being loaded from a file, polyPathPointList already exists
        if not hasattr(self, 'polyPathPointList'):
            super().__init__(QtGui.QPainterPath(point), parent=parent, start=start)
        else:
            poly = QtGui.QPolygonF(self.polyPathPointList[0])
            path = QtGui.QPainterPath()
            path.addPolygon(poly)
            super().__init__(path, parent=parent, start=start)
        # drawingElement.__init__(self, parent, start, **kwargs)
        self.setLocalPenOptions(**kwargs)
        self.setLocalBrushOptions(**kwargs)
        self.oldPath = self.path()
        if self.start is not None:
            self.setPos(self.start)
        self.editPointNumber = 0
        self.undoPathList = []

    def __getstate__(self):
        localDict = super().__getstate__()
        # Add a list of all points part of the wire
        polyPathList = self.path().toSubpathPolygons(QtGui.QTransform())
        polyPathPointList = []
        for poly in polyPathList:
            polyPathPointList.append([poly.at(i) for i in range(poly.count())])
        localDict['polyPathPointList'] = polyPathPointList
        # Create copy and return that so that autosave does not remove
        # important required properties
        localDictCopy = localDict.copy()
        localDictCopy.pop('oldPath', None)
        localDictCopy['undoPathList'] = []
        return localDictCopy

    def __setstate__(self, state):
        super().__setstate__(state)
        # Add a polygon corresponding to the list of saved points
        a = QtGui.QPolygonF(state['polyPathPointList'][0])
        self.oldPath2 = QtGui.QPainterPath()
        for item in state['polyPathPointList']:
            poly = QtGui.QPolygonF(item)
            self.oldPath2.addPolygon(poly)
        self.oldPath = self.__dict__.pop('oldPath2', None)

    def boundingRect(self):
        rect = super().boundingRect()
        return rect

    def updateWire(self, newEnd, edit=False):
        # Update existing segment to end at newEnd
        newEnd = self.mapFromScene(newEnd)
        if edit is False:
            self.setPath(self.oldPath)
            path = self.path()
            path.lineTo(newEnd)
        else:
            polyPathList = self.oldPath.toSubpathPolygons(QtGui.QTransform())
            polyPathPointList = []
            for poly in polyPathList:
                for i in range(poly.count()):
                    polyPathPointList.append(poly.at(i))
            polyPathPointList[self.editPointNumber] = newEnd
            polyPathList = QtGui.QPolygonF(polyPathPointList)
            path = QtGui.QPainterPath()
            path.addPolygon(polyPathList)
        self.setPath(path)

    def createSegment(self, newEnd):
        # Create a new segment (e.g. when LMB is clicked)
        newEnd = self.mapFromScene(newEnd)
        self.oldPath.lineTo(newEnd)
        self.setPath(self.oldPath)

    def cancelSegment(self):
        # Remove from scene if no segment exists
        if self.oldPath.toSubpathPolygons(self.transform()) == []:
            self.scene().removeItem(self)
        else:
            self.setPath(self.oldPath)

    def createCopy(self, parent=None):
        """Reimplemented from drawingElement. Sets path and origin of the copy
        to that of the original.
        """
        newWire = super().createCopy(parent)
        newWire.setPath(self.path())
        newWire.oldPath = newWire.path()
        if hasattr(self, 'origin'):
            newWire.origin = self.origin
        return newWire

    def undoDraw(self):
        if len(self.oldPath.toSubpathPolygons(self.transform())) == 0:
            return False
        lastPoly = self.oldPath.toSubpathPolygons(self.transform())[-1]
        lastPoly.remove(lastPoly.size() - 1)
        otherPoly = self.oldPath.toSubpathPolygons(self.transform())[:-1]
        path = QtGui.QPainterPath()
        for i in otherPoly:
            path.addPolygon(i)
        path.addPolygon(lastPoly)
        self.oldPath = path
        self.setPath(self.oldPath)

    def redoDraw(self, point=None):
        self.createSegment(point)

    def editPointLocation(self, editPointNumber):
        polyPathList = self.oldPath.toSubpathPolygons(QtGui.QTransform())
        polyPathPointList = []
        for poly in polyPathList:
            for i in range(poly.count()):
                polyPathPointList.append(poly.at(i))
        return polyPathPointList[editPointNumber]

    def undoEdit(self):
        path = self.undoPathList.pop()
        if path is None:
            self.setPath(self.oldPath)
            return
        self.oldPath = path
        self.setPath(path)
        self.editPointNumber -= 1
        poly = path.toSubpathPolygons(QtGui.QTransform())[0]
        self.editPointNumber %= poly.size()

    def redoEdit(self, point=None, clicked=False):
        if self.editPointLocation(self.editPointNumber) == self.mapFromScene(point):
            self.undoPathList.append(None)
            if clicked is True:
                self.editPointNumber += 1
                self.editPointNumber %= self.oldPath.toSubpathPolygons(QtGui.QTransform())[0].size()
            return
        # Create a list of all points part of the wire
        polyPathList = self.oldPath.toSubpathPolygons(QtGui.QTransform())
        polyPathPointList = []
        for poly in polyPathList:
            for i in range(poly.count()):
                polyPathPointList.append(poly.at(i))
        polyPathPointList[self.editPointNumber] = self.mapFromScene(point)
        poly = QtGui.QPolygonF(polyPathPointList)
        path = QtGui.QPainterPath()
        path.addPolygon(poly)
        self.undoPathList.append(self.oldPath)
        self.oldPath = path
        self.setPath(path)
        if clicked is True:
            self.editPointNumber += 1
            self.editPointNumber %= self.oldPath.toSubpathPolygons(QtGui.QTransform())[0].size()


class Net(QtWidgets.QGraphicsLineItem, drawingElement):
    def __init__(self, parent=None, start=None, **kwargs):
        """This class implements nets for connecting elements in a circuit. It
        is different from the Wire class in that it only supports right angle
        connections (automatically draws these as 2 separate Nets)."""
        point = QtCore.QPointF(0, 0)
        # For when the net is being loaded from a file, oldLine already exists
        if not hasattr(self, 'oldLine'):
            super().__init__(QtCore.QLineF(point, point), parent=parent, start=start)
        else:
            super().__init__(self.oldLine, parent=parent, start=start)
        # drawingElement.__init__(self, parent, start, **kwargs)
        self.setLocalPenOptions(**kwargs)
        self.setLocalBrushOptions(**kwargs)
        self.oldLine = self.line()
        self.rightAngleMode = "top"
        self.perpLine = None  #Perpendicular line
        self.setFlag(QtWidgets.QGraphicsItem.ItemSendsScenePositionChanges)
        if self.start is not None:
            self.setPos(self.start)

    def __getstate__(self):
        localDict = super().__getstate__()
        # Add a list of all points part of the wire
        line = self.line()
        localDict['oldLine'] = line
        return localDict

    def __setstate__(self, state):
        super().__setstate__(state)
        self.oldLine = state['oldLine']

    def boundingRect(self):
        rect = super().boundingRect()
        pad = 10
        if rect.width() < pad:
            rect.setWidth(pad)
            rect.moveLeft(-pad / 2)
        elif rect.height() < pad:
            rect.setHeight(pad)
            rect.moveTop(-pad / 2)
        return rect

    def updateNet(self, newEnd):
        newEnd = self.mapFromScene(newEnd)
        if self.perpLine is None:
            if newEnd.x() != 0 and newEnd.y() != 0:
                self.perpLine = self.createCopy()
                self.perpLine.setPos(QtCore.QPointF(self.start.x(), self.start.y() + newEnd.y()))
                self.perpLine.setSelected(False)
        line = self.line()
        if self.rightAngleMode == 'top':
            line.setP2(QtCore.QPointF(0.0, newEnd.y()))
        elif self.rightAngleMode == 'bottom':
            line.setP2(QtCore.QPointF(newEnd.x(), 0.0))
        if newEnd.x() == 0 or newEnd.y() == 0:
            if self.perpLine is not None:
                self.scene().removeItem(self.perpLine)
            self.perpLine = None
            line.setP2(newEnd)
        else:
            perpLine = self.perpLine.line()
            if self.rightAngleMode == 'top':
                self.perpLine.setPos(QtCore.QPointF(self.start.x(), self.start.y() + newEnd.y()))
                perpLine.setP2(QtCore.QPointF(newEnd.x(), 0.0))
            elif self.rightAngleMode == 'bottom':
                self.perpLine.setPos(QtCore.QPointF(self.start.x() + newEnd.x(), self.start.y()))
                perpLine.setP2(QtCore.QPointF(0.0, newEnd.y()))
            self.perpLine.setLine(perpLine)
        self.setLine(line)

    def cancelSegment(self):
        # Remove from scene if no segment exists
        if self.perpLine is not None:
            self.scene().removeItem(self.perpLine)
            self.perpLine = None
        self.scene().removeItem(self)

    def createCopy(self, parent=None):
        """Reimplemented from drawingElement. Sets the line and origin of the
        copy the same as the current line.
        """
        newNet = super().createCopy(parent)
        newNet.setLine(self.line())
        newNet.oldLine = newNet.line()
        if hasattr(self, 'origin'):
            newNet.origin = self.origin
        return newNet

    def changeRightAngleMode(self, newEnd):
        self.prepareGeometryChange()
        if self.rightAngleMode == 'top':
            self.rightAngleMode = 'bottom'
        else:
            self.rightAngleMode = 'top'
        self.updateNet(newEnd)

    def mergeNets(self, netList, undoStack):
        # Had to do the import here to avoid circular imports
        from src.commands import Add, Delete, EditNet
        # If this net has already been processed, its scene will not exist
        if self.scene() is None:
            return None
        if self in netList:
            netList.remove(self)
        mergedNet = None
        line1 = self.line()
        line1 = QtCore.QLineF(self.mapToScene(line1.p1()), self.mapToScene(line1.p2()))
        # Logic to figure out which points are within which other points
        x11, x12 = min(line1.p1().x(), line1.p2().x()), max(line1.p1().x(), line1.p2().x())
        y11, y12 = min(line1.p1().y(), line1.p2().y()), max(line1.p1().y(), line1.p2().y())
        for net in netList:
            line2 = net.line()
            line2 = QtCore.QLineF(net.mapToScene(line2.p1()), net.mapToScene(line2.p2()))
            x21, x22 = min(line2.p1().x(), line2.p2().x()), max(line2.p1().x(), line2.p2().x())
            y21, y22 = min(line2.p1().y(), line2.p2().y()), max(line2.p1().y(), line2.p2().y())
            xList, yList = [x11, x21, x12, x22], [y11, y21, y12, y22]
            if x21 < x11:
                xList = [x21, x11, x22, x12]
            if y21 < y11:
                yList = [y21, y11, y22, y12]
            sortedXList, sortedYList = sorted(xList), sorted(yList)
            if line2.angleTo(line1) in [0, 180]:
                p1 = None
                p2 = None
                if y11 == y21 and y11 == y12 and y11 == y22:
                    if xList == sortedXList:
                        p1 = self.mapFromScene(QtCore.QPointF(sortedXList[0], y11))
                        p2 = self.mapFromScene(QtCore.QPointF(sortedXList[3], y11))
                    elif x21 >= x11 and x22 <= x12:
                        scene = net.scene()
                        del1 = Delete(None, scene, [net])
                        undoStack.push(del1)
                        mergedNet = self
                    elif x21 < x11 and x22 > x12:
                        scene = self.scene()
                        del1 = Delete(None, scene, [self])
                        undoStack.push(del1)
                        mergedNet = net
                elif x11 == x21 and x11 == x12 and x11 == x22:
                    if yList == sortedYList:
                        p1 = self.mapFromScene(QtCore.QPointF(x11, sortedYList[0]))
                        p2 = self.mapFromScene(QtCore.QPointF(x11, sortedYList[3]))
                    elif y21 >= y11 and y22 <= y12:
                        scene = net.scene()
                        del1 = Delete(None, scene, [net])
                        undoStack.push(del1)
                        mergedNet = self
                    elif y21 < y11 and y22 > y12:
                        scene = self.scene()
                        del1 = Delete(None, scene, [self])
                        undoStack.push(del1)
                        mergedNet = net
                if p1 is not None:
                    scene = self.scene()
                    oldLine = self.line()
                    newLine = QtCore.QLineF(p1, p2)
                    editNet = EditNet(None, scene, self, oldLine, newLine)
                    undoStack.push(editNet)
                    # self.setLine(QtCore.QLineF(p1, p2))
                    del1 = Delete(None, scene, [net])
                    undoStack.push(del1)
                    # Update x11, x12, y11 and y12
                    line1 = self.line()
                    line1 = QtCore.QLineF(self.mapToScene(line1.p1()), self.mapToScene(line1.p2()))
                    # Logic to figure out which points are within which other points
                    x11, x12 = min(line1.p1().x(), line1.p2().x()), max(line1.p1().x(), line1.p2().x())
                    y11, y12 = min(line1.p1().y(), line1.p2().y()), max(line1.p1().y(), line1.p2().y())
                    mergedNet = self
        if mergedNet == self:
            scene = mergedNet.scene()
            # Check if the item is a dot
            allDots = [item for item in scene.items() if isinstance(item, Circle) and item.localBrushStyle == 1 and item.oldRect == QtCore.QRectF(0, -5, 10, 10)]
            # Keep only dots that are inside the net (not on endpoints)
            for dot in allDots[:]:
                dotPos = mergedNet.mapFromScene(dot.scenePos())
                # The dot's scenePos is slightly to the left of actual center
                dotPos += QtCore.QPointF(5, 0)
                if dotPos in [mergedNet.line().p1(), mergedNet.line().p2()]:
                    allDots.remove(dot)
                elif not mergedNet.contains(dotPos):
                    allDots.remove(dot)
            if allDots != []:
                # Find parent item of the dot instead of the circle that has been found
                for i in xrange(len(allDots)):
                    while allDots[i].parentItem() is not None:
                        allDots[i] = allDots[i].parentItem()
                # Delete the dots that are on the net
                del1 = Delete(None, scene, allDots)
                undoStack.push(del1)
        return mergedNet

    def splitNets(self, netList, undoStack, mode='add'):
        # Had to do the import here to avoid circular imports
        from src.commands import Add, Delete
        # If this net has already been processed, its scene will not exist
        if self.scene() is None:
            return None
        if self in netList:
            netList.remove(self)
        line1 = self.line()
        line1 = QtCore.QLineF(self.mapToScene(line1.p1()), self.mapToScene(line1.p2()))
        scene = self.scene()
        for net in netList:
            line2 = net.line()
            line2 = QtCore.QLineF(net.mapToScene(line2.p1()), net.mapToScene(line2.p2()))
            if line2.angleTo(line1) == 90 or line2.angleTo(line1) == 270:
                if line2.p1() in [line1.p1(), line1.p2()] or line2.p2() in [line1.p1(), line1.p2()]:
                    pass
                else:
                    newNet1, newNet2 = None, None
                    if net.contains(net.mapFromItem(self, self.line().p1())):
                        newNet1 = net.createCopy()
                        newNet2 = net.createCopy()
                        scene.removeItem(newNet1)
                        scene.removeItem(newNet2)
                        if net.scene() is not None:
                            del1 = Delete(None, scene, [net])
                            undoStack.push(del1)
                        newNet1Line, newNet2Line = newNet1.line(), newNet2.line()
                        newNet1Line.setP1(net.line().p1())
                        newNet1Line.setP2(net.mapFromItem(self, self.line().p1()))
                        newNet2Line.setP2(net.line().p2())
                        newNet2Line.setP1(net.mapFromItem(self, self.line().p1()))
                        newNet1.setLine(newNet1Line)
                        newNet2.setLine(newNet2Line)
                        add = Add(None, scene, newNet1)
                        undoStack.push(add)
                        add = Add(None, scene, newNet2)
                        undoStack.push(add)
                        dotPos = self.mapToScene(self.line().p1())
                    elif net.contains(net.mapFromItem(self, self.line().p2())):
                        newNet1 = net.createCopy()
                        newNet2 = net.createCopy()
                        scene.removeItem(newNet1)
                        scene.removeItem(newNet2)
                        if net.scene() is not None:
                            del1 = Delete(None, scene, [net])
                            undoStack.push(del1)
                        newNet1Line, newNet2Line = newNet1.line(), newNet2.line()
                        newNet1Line.setP1(net.line().p1())
                        newNet1Line.setP2(net.mapFromItem(self, self.line().p2()))
                        newNet2Line.setP2(net.line().p2())
                        newNet2Line.setP1(net.mapFromItem(self, self.line().p2()))
                        newNet1.setLine(newNet1Line)
                        newNet2.setLine(newNet2Line)
                        add = Add(None, scene, newNet1)
                        undoStack.push(add)
                        add = Add(None, scene, newNet2)
                        undoStack.push(add)
                        dotPos = self.mapToScene(self.line().p2())
                    elif self.contains(self.mapFromItem(net, net.line().p1())):
                        newNet1 = self.createCopy()
                        newNet2 = self.createCopy()
                        scene.removeItem(newNet1)
                        scene.removeItem(newNet2)
                        if self.scene() is not None:
                            del1 = Delete(None, scene, [self])
                            undoStack.push(del1)
                        newNet1Line, newNet2Line = newNet1.line(), newNet2.line()
                        newNet1Line.setP1(self.line().p1())
                        newNet1Line.setP2(self.mapFromItem(net, net.line().p1()))
                        newNet2Line.setP2(self.line().p2())
                        newNet2Line.setP1(self.mapFromItem(net, net.line().p1()))
                        newNet1.setLine(newNet1Line)
                        newNet2.setLine(newNet2Line)
                        add = Add(None, scene, newNet1)
                        undoStack.push(add)
                        add = Add(None, scene, newNet2)
                        undoStack.push(add)
                        dotPos = net.mapToScene(net.line().p1())
                    elif self.contains(self.mapFromItem(net, net.line().p2())):
                        newNet1 = self.createCopy()
                        newNet2 = self.createCopy()
                        scene.removeItem(newNet1)
                        scene.removeItem(newNet2)
                        if self.scene() is not None:
                            del1 = Delete(None, scene, [self])
                            undoStack.push(del1)
                        newNet1Line, newNet2Line = newNet1.line(), newNet2.line()
                        newNet1Line.setP1(self.line().p1())
                        newNet1Line.setP2(self.mapFromItem(net, net.line().p2()))
                        newNet2Line.setP2(self.line().p2())
                        newNet2Line.setP1(self.mapFromItem(net, net.line().p2()))
                        newNet1.setLine(newNet1Line)
                        newNet2.setLine(newNet2Line)
                        add = Add(None, scene, newNet1)
                        undoStack.push(add)
                        add = Add(None, scene, newNet2)
                        undoStack.push(add)
                        dotPos = net.mapToScene(net.line().p2())
                    if newNet1 is not None:
                        newNetList1 = [item for item in netList if item.collidesWithItem(newNet1)]
                        newNetList2 = [item for item in netList if item.collidesWithItem(newNet2)]
                        # Add a dot if required
                        allDots = [item for item in scene.items() if isinstance(item, Circle) and item.localBrushStyle == 1 and item.oldRect == QtCore.QRectF(0, -5, 10, 10)]
                        dotExists = False
                        for item in allDots:
                            existingDotPos = item.scenePos()
                            # The dot's scenePos is slightly to the left of actual center
                            existingDotPos += QtCore.QPointF(5, 0)
                            if dotPos == item.scenePos():
                                dotExists = True
                                break
                        if dotExists is False:
                            with open('Resources/Symbols/Standard/Dot.sym', 'rb') as f:
                                dot1 = pickle.load(f)
                                dot1.__init__(None, dotPos, dot1.listOfItems, mode='symbol')
                                scene.addItem(dot1)
                                dot1.moveTo(dotPos, 'start')
                                dot1.moveTo(dotPos, 'done')
                                scene.removeItem(dot1)
                                add1 = Add(None, scene, dot1, symbol=True, origin=dotPos)
                                undoStack.push(add1)
                        newNet1.splitNets(newNetList1, undoStack)
                        newNet2.splitNets(newNetList2, undoStack)
                        # Break if self has been deleted
                        if self.scene() is None:
                            break


class Rectangle(QtWidgets.QGraphicsRectItem, drawingElement):
    """Class responsible for drawing rectangular objects"""

    def __init__(self, parent=None, start=None, **kwargs):
        point = QtCore.QPointF(0, 0)
        rect = QtCore.QRectF(point, point)
        if not hasattr(self, 'oldRect'):
            super().__init__(rect, parent=parent, start=point)
            self.setPos(start)
        else:
            super().__init__(self.oldRect, parent=parent, start=point)
            self.setPos(self.origin)
        self.oldRect = self.rect()
        # Set the fixed vertex to (0, 0) in local coordinates
        # drawingElement.__init__(self, parent, start=point, **kwargs)
        self.setLocalPenOptions(**kwargs)
        self.setLocalBrushOptions(**kwargs)

    def boundingRect(self):
        # Make the bounding rect a little bigger so it is easier to see
        pad = 10
        topLeft = self.rect().normalized().topLeft() + QtCore.QPointF(-pad, -pad)
        bottomRight = self.rect().normalized().bottomRight() + QtCore.QPointF(pad, pad)
        rect = QtCore.QRectF(topLeft, bottomRight)
        return rect

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(self.boundingRect())
        hollowRect = self.boundingRect()
        pad = 10
        hollowRect.setWidth(hollowRect.width() - 4 * pad)
        hollowRect.setHeight(hollowRect.height() - 4 * pad)
        hollowRect.moveLeft(hollowRect.left() + 2 * pad)
        hollowRect.moveTop(hollowRect.top() + 2 * pad)
        hollowPath = QtGui.QPainterPath()
        hollowPath.addRect(hollowRect)
        return path.subtracted(hollowPath)

    def paint(self, painter, *args):
        # We have to manually draw out the bounding rect
        if self.isSelected() is False:
            super().paint(painter, *args)
        else:
            pen = QtGui.QPen()
            pen.setStyle(2)
            painter.setPen(pen)
            painter.drawRect(self.boundingRect())
            painter.setPen(self.localPen)
            painter.setBrush(self.localBrush)
            painter.drawRect(self.rect())

    def updateRectangle(self, end, edit=False):
        # Update the end point of the rectangle to end
        end = self.mapFromScene(end)
        if edit is True:
            start = self.p1
        else:
            start = self.start
        rect = QtCore.QRectF(start, end)
        self.prepareGeometryChange()
        self.setRect(rect)
        self.oldRect = rect

    def createCopy(self, parent=None):
        """Reimplemented from drawingElement. Sets the rect and origin of the
        copy the same as the current rect.
        """
        newRectangle = super().createCopy(parent)
        newRectangle.setRect(self.rect())
        newRectangle.oldRect = newRectangle.rect()
        if hasattr(self, 'origin'):
            newRectangle.origin = self.origin
        return newRectangle

    def mouseReleaseEvent(self, event):
        self.updateP1P2()
        rect = QtCore.QRectF(self.p1, self.p2)
        # Necessary so that bounding rect is drawn correctly
        self.prepareGeometryChange()
        self.setRect(rect)
        self.oldRect = rect
        super().mouseReleaseEvent(event)

    def undoEdit(self):
        rect = self.undoRectList.pop()
        self.setRect(rect)
        self.oldRect = rect
        self.updateP1P2()

    def redoEdit(self, point, **kwargs):
        if not hasattr(self, 'undoRectList'):
            self.undoRectList = []
        rect = QtCore.QRectF(self.p1, self.mapFromScene(point))
        self.setRect(rect)
        self.oldRect = rect
        self.undoRectList.append(self.rect())
        self.updateP1P2()

    def updateP1P2(self):
        # Make sure start is top left and end is bottom right
        # if self.rect().width() >= 0 and self.rect().height() >= 0:
        #     self.p1 = self.rect().topLeft()
        #     self.p2 = self.rect().bottomRight()
        # elif self.rect().width() >= 0 and self.rect().height() < 0:
        #     self.p1 = self.rect().bottomLeft()
        #     self.p2 = self.rect().topRight()
        # elif self.rect().width() < 0 and self.rect().height() >= 0:
        #     self.p1 = self.rect().topRight()
        #     self.p2 = self.rect().bottomLeft()
        # else:
        #     self.p1 = self.rect().bottomRight()
        #     self.p2 = self.rect().topLeft()
        rect = self.rect().normalized()
        self.p1, self.p2 = rect.topLeft(), rect.bottomRight()


class Ellipse(QtWidgets.QGraphicsEllipseItem, drawingElement):
    """Class responsible for drawing elliptical objects"""

    def __init__(self, parent=None, start=None, **kwargs):
        point = QtCore.QPointF(0, 0)
        rect = QtCore.QRectF(point, point)
        if not hasattr(self, 'oldRect'):
            super().__init__(rect, parent=parent, start=point)
            self.setPos(start)
        else:
            super().__init__(self.oldRect, parent=parent, start=point)
            self.setPos(self.origin)
        # Set the fixed vertex to (0, 0) in local coordinates
        # drawingElement.__init__(self, parent, start=point, **kwargs)
        self.setLocalPenOptions(**kwargs)
        self.setLocalBrushOptions(**kwargs)
        self.oldRect = self.rect()

    def boundingRect(self):
        # Make the bounding rect a little bigger so that it is easier to see
        pad = 10
        topLeft = self.rect().normalized().topLeft() + QtCore.QPointF(-pad, -pad)
        bottomRight = self.rect().normalized().bottomRight() + QtCore.QPointF(pad, pad)
        rect = QtCore.QRectF(topLeft, bottomRight)
        return rect

    def shape(self):
        path = QtGui.QPainterPath()
        path.addEllipse(self.boundingRect())
        hollowRect = self.boundingRect()
        pad = 10
        hollowRect.setWidth(hollowRect.width() - 4 * pad)
        hollowRect.setHeight(hollowRect.height() - 4 * pad)
        hollowRect.moveLeft(hollowRect.left() + 2 * pad)
        hollowRect.moveTop(hollowRect.top() + 2 * pad)
        hollowPath = QtGui.QPainterPath()
        hollowPath.addEllipse(hollowRect)
        return path.subtracted(hollowPath)

    def paint(self, painter, *args):
        # We have to manually draw out the bounding rect
        if self.isSelected() is False:
            super().paint(painter, *args)
        else:
            pen = QtGui.QPen()
            pen.setStyle(2)
            painter.setPen(pen)
            painter.drawRect(self.boundingRect())
            painter.setPen(self.localPen)
            painter.setBrush(self.localBrush)
            painter.drawEllipse(self.rect())

    def updateEllipse(self, end, edit=False):
        # Update the end point of the ellipse to end
        end = self.mapFromScene(end)
        if edit is True:
            start = self.p1
        else:
            start = self.start
        rect = QtCore.QRectF(start, end)
        self.prepareGeometryChange()
        self.setRect(rect)
        self.oldRect = rect

    def createCopy(self, parent=None):
        """Reimplemented from drawingElement. Sets the rect and origin of the
        copy the same as the current ellipse."""
        newEllipse = super().createCopy(parent)
        newEllipse.setRect(self.rect())
        newEllipse.oldRect = newEllipse.rect()
        if hasattr(self, 'origin'):
            newEllipse.origin = self.origin
        return newEllipse

    def mouseReleaseEvent(self, event):
        self.updateP1P2()
        rect = QtCore.QRectF(self.p1, self.p2)
        # Necessary so that bounding rect is drawn correctly
        self.prepareGeometryChange()
        self.setRect(rect)
        self.oldRect = rect
        # # Necessary so that bounding rect is drawn correctly
        # self.prepareGeometryChange()
        super().mouseReleaseEvent(event)

    def updateP1P2(self):
        # Make sure start is top left and end is bottom right
        # if self.rect().width() >= 0 and self.rect().height() >= 0:
        #     self.p1 = self.rect().topLeft()
        #     self.p2 = self.rect().bottomRight()
        # elif self.rect().width() >= 0 and self.rect().height() < 0:
        #     self.p1 = self.rect().bottomLeft()
        #     self.p2 = self.rect().topRight()
        # elif self.rect().width() < 0 and self.rect().height() >= 0:
        #     self.p1 = self.rect().topRight()
        #     self.p2 = self.rect().bottomLeft()
        # else:
        #     self.p1 = self.rect().bottomRight()
        #     self.p2 = self.rect().topLeft()
        rect = self.rect().normalized()
        self.p1, self.p2 = rect.topLeft(), rect.bottomRight()

    def undoEdit(self):
        rect = self.undoRectList.pop()
        self.setRect(rect)
        self.oldRect = rect
        self.updateP1P2()

    def redoEdit(self, point, **kwargs):
        if not hasattr(self, 'undoRectList'):
            self.undoRectList = []
        rect = QtCore.QRectF(self.p1, self.mapFromScene(point))
        self.setRect(rect)
        self.oldRect = rect
        self.undoRectList.append(self.rect())
        self.updateP1P2()


class Circle(Ellipse):
    """This is a special case of the Ellipse class where a = b."""

    def __init__(self, parent=None, start=None, **kwargs):
        super().__init__(parent, start, **kwargs)

    def updateCircle(self, end):
        # Update the opposite end of the diameter of the circle to end
        distanceLine = end - self.mapToScene(self.start)
        # Calculate the angle made by the diameter to +ve X-axis
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
            theta = 180 / math.pi * math.atan2(distanceLine.y(),
                                                   distanceLine.x())
        sideLength = math.sqrt(distanceLine.x()**2 + distanceLine.y()**2)
        square = QtCore.QRectF(self.start + QtCore.QPointF(0, -sideLength / 2),
                               QtCore.QSizeF(sideLength, sideLength))
        self.setRect(square)
        self.transform_ = QtGui.QTransform()
        self.transform_.translate(0, 0)
        self.transform_.rotate(theta)
        self.setTransform(self.transform_)
        self.oldRect = self.rect()
        self.end = QtCore.QPointF(end)

    def undoEdit(self):
        # rect = self.undoRectList.pop()
        # self.setRect(rect)
        # transform_ = self.undoTransformList.pop()
        # self.setTransform(transform_)
        point = self.undoPointList.pop()
        self.updateCircle(point)
        # self.oldRect = rect
        # self.transform_ = transform_

    def redoEdit(self, point, **kwargs):
        if not hasattr(self, 'undoPointList'):
            self.undoPointList = []
        self.updateCircle(point)
        self.undoPointList.append(point)


class TextBox(QtWidgets.QGraphicsTextItem, drawingElement):
    """Responsible for showing formatted text as well as LaTeX images.
    The following formatting options are supported:
        1. Bold
        2. Italic
        3. Underline
        4. Subscript
        5. Superscript
    LaTeX images are displayed in place of the text.
    TODO: Fix size issues with rendered LaTeX images
    TODO: Grey out LaTeX images on mouse hover
    """

    def __init__(self, parent=None, start=None, text='', **kwargs):
        point = QtCore.QPointF(0, 0)
        # For some reason, checking hasattr(self, 'origin')
        # worked with Python 2 but not with Python 3. The following
        # approach works with both though
        if 'origin' not in self.__dict__:
            super().__init__(parent, start=point)
            self.setPos(start)
        else:
            super().__init__(parent, start=point)
            self.setPos(self.origin)
        # Set the fixed vertex to (0, 0) in local coordinates
        # drawingElement.__init__(self, parent, start=point, **kwargs)
        if not hasattr(self, 'latexImageBinary'):
            self.latexImageHtml = None
            self.latexExpression = None
            self.latexImageBinary = None
        # For backwards compatibility
        if not hasattr(self, 'latexImageColour'):
            self.latexImageColour = QtGui.QColor('black')
        if not hasattr(self, 'textScale'):
            self.textScale = 4
        self.setLocalPenOptions(**kwargs)
        self.setLocalBrushOptions(**kwargs)
        self.setTextWidth(-1)
        if hasattr(self, 'font_'):
            self.changeFont(self.font_)
        elif 'font' in kwargs:
            # Default font
            self.font_ = kwargs['font']
            self.changeFont(self.font_)
        # Sets the desired DPI for the image being generated
        self.latexImageDpi = 300
        # Scale the DPI in order to avoid pixelation
        self.latexImageDpiScale = 4
        if text != '':
            self.setHtml(text)
        elif self.latexImageHtml is not None:
            self.setHtml(self.latexImageHtml)
        elif hasattr(self, 'htmlText'):
            self.setHtml(self.htmlText)
        else:
            self.showEditor()

    def __getstate__(self):
        localDict = super().__getstate__()
        # Create copy of localDict and return that so that autosave does not
        # remove important required properties
        localDictCopy = localDict.copy()
        localDictCopy.pop('textEditor', None)
        # Add htmlText to the dict
        localDictCopy['htmlText'] = self.toHtml()
        # Change the font to a string for pickling
        localDictCopy['font_'] = self.font().toString()
        if hasattr(self, 'latexImageBinary'):
            localDictCopy['latexImageColour'] = QtGui.QColor(self.localPenColour)
        return localDictCopy

    def __setstate__(self, state):
        super().__setstate__(state)
        if 'font_' in state:
            font = QtGui.QFont()
            font.fromString(state.pop('font_'))
            self.font_ = font

    def boundingRect(self):
        if self.latexImageBinary is None:
            return super().boundingRect()
        else:
            if not hasattr(self, 'rect_'):
                pix = QtGui.QPixmap()
                pix.loadFromData(self.latexImageBinary.getvalue(), format='png')
                self.rect_ = QtCore.QRectF(QtCore.QPointF(0, 0), QtCore.QSizeF(pix.size()/self.latexImageDpiScale))
            return self.rect_

    def paint(self, painter, option, widget):
        if self.latexImageBinary is None:
            super().paint(painter, option, widget)
        else:
            if self.isSelected() is True:
                pen = QtGui.QPen()
                pen.setWidth(0.5)
                pen.setStyle(2)
                painter.setPen(pen)
                painter.drawRect(self.boundingRect())
            pix = QtGui.QPixmap()
            pix.loadFromData(self.latexImageBinary.getvalue(), format='png')
            # painter.setPen(self.localPen)
            # painter.setBrush(self.localBrush)
            self.rect_ = QtCore.QRectF(QtCore.QPointF(0, 0), QtCore.QSizeF(pix.size()/self.latexImageDpiScale))
            painter.drawPixmap(self.rect_.toRect(), pix)

    def shape(self):
        path = QtGui.QPainterPath()
        path.addRect(self.boundingRect())
        return path

    def showEditor(self):
        self.textEditor = TextEditor(self)
        self.textEditor.exec_()

    def setLocalPenOptions(self, **kwargs):
        """Reimplemented from drawingElement. QGraphicsTextItem objects do not
        have pens and brushes. Further, they have fonts whose sizes and widths
        can be changed.
        """
        # Necessary for objects with modified bounding rects
        self.prepareGeometryChange()
        if 'pen' in kwargs:
            self.localPen = kwargs['pen']
            self.localPenColour = str(self.localPen.color().name())
            self.localPenStyle = self.localPen.style()
        if 'penColour' in kwargs:
            self.localPenColour = kwargs['penColour']
        if 'penStyle' in kwargs:
            self.localPenStyle = kwargs['penStyle']
        self.changeTextColour(self.localPenColour)

    def changeTextColour(self, colour='gray'):
        if self.latexImageBinary is None:
            # Create a textedit to conveniently change the text color
            textEdit = QtWidgets.QTextEdit()
            textEdit.setHtml(self.toHtml())
            textEdit.selectAll()
            textEdit.setTextColor(QtGui.QColor(colour))
            self.setHtml(textEdit.toHtml())
            # self.setDefaultTextColor(QtGui.QColor(colour))
        else:
            # Do not regenerate the latex image if the colour is the same.
            # Speeds up loading times by using the saved binary image instead
            # of generating the image again
            if hasattr(self, 'latexImageColour'):
                if self.latexImageColour == QtGui.QColor(colour):
                    return
            # When loading from file, textEditor will not be present
            # In that case, first create the textEditor
            if not hasattr(self, 'textEditor'):
                self.textEditor = TextEditor(self)
            self.latexImageBinary = self.textEditor.mathTexToQImage(
                '$' + self.latexExpression + '$',
                self.localPenWidth,
                self.localPenColour)

    def changeFont(self, font):
        # Create a textedit to conveniently change the font
        textEdit = QtWidgets.QTextEdit()
        textEdit.setHtml(self.toHtml())
        textEdit.selectAll()
        textEdit.setCurrentFont(font)
        self.localPenWidth = font.pointSize() * self.textScale
        textEdit.setFontPointSize(self.localPenWidth)
        self.setHtml(textEdit.toHtml())
        self.font_ = font
        self.setFont(self.font_)

    def lightenColour(self, lighten=False):
        # Only process this if text is not latex
        if self.latexImageBinary is None:
            if lighten is True:
                self.changeTextColour('gray')
            else:
                self.changeTextColour(self.localPenColour)

    def mouseDoubleClickEvent(self, event):
        # Show the editor on double click
        super().mouseDoubleClickEvent(event)
        # Reset the text colour from gray
        self.lightenColour(False)
        self.showEditor()

    def createCopy(self, parent=None):
        if self.isSelected() is True:
            self.setSelected(False)
        _start = self.pos()
        pen = QtGui.QPen()
        pen.setWidth(self.localPenWidth)
        pen.setColor(QtGui.QColor(self.localPenColour))
        pen.setStyle(self.localPenStyle)
        brush = QtGui.QBrush()
        brush.setColor(QtGui.QColor(self.localBrushColour))
        brush.setStyle(self.localBrushStyle)
        if self.latexImageBinary is not None:
            newItem = self.__class__(
                parent,
                _start,
                text=self.toHtml(),
                pen=pen,
                brush=brush,
                penColour = self.localPenColour,
                brushColour = self.localBrushColour)
            newItem.latexExpression = self.latexExpression
            newItem.latexImageBinary = self.latexImageBinary
        else:
            newItem = self.__class__(
                parent,
                _start,
                text=self.toHtml(),
                pen=pen,
                brush=brush,
                penColour = self.localPenColour,
                brushColour = self.localBrushColour)
            newItem.changeFont(self.font())
        if hasattr(self, 'reflections'):
            newItem.reflections = self.reflections
        if hasattr(self, 'height'):
            newItem.height = self.height
            newItem.setZValue(newItem.height)
        newItem.setTransform(self.transform())
        self.scene().addItem(newItem)
        newItem.setSelected(True)
        newItem.moveTo(self.scenePos(), 'start')
        return newItem


class Arc(Wire):
    """This is a special case of the Wire class where repeated clicks change the curvature
    of the wire."""

    def __init__(self, parent=None, start=None, **kwargs):
        super().__init__(parent=parent, start=start, **kwargs)
        if 'points' in kwargs:
            self.points = kwargs['points']
        self.clicks = 0
        self.setFocus()
        self.undoPointsList = []
        self.startPoint = QtCore.QPointF(0, 0)
        self.localPen.setCapStyle(QtCore.Qt.RoundCap)

    def __getstate__(self):
        localDict = super().__getstate__()
        # Create copy of localDict and return that so that autosave does not
        # remove important required properties
        localDictCopy = localDict.copy()
        localDictCopy['undoPointsList'] = []
        return localDictCopy

    def createCopy(self, parent=None):
        newArc = super().createCopy(parent)
        newArc.points = self.points
        newArc.startPoint = self.startPoint
        newArc.endPoint = self.endPoint
        newArc.controlPoint = self.controlPoint
        if self.points == 4:
            newArc.controlPointAlt = self.controlPointAlt
        return newArc

    def updateArc(self, newEnd, click=False, edit=False):
        self.setFocus()
        self.prepareGeometryChange()
        newEnd = self.mapFromScene(newEnd)
        if edit is False:
            if click is True:
                self.clicks += 1
                if self.clicks == 1:
                    self.endPoint = newEnd
                elif self.clicks == 2:
                    self.controlPoint = newEnd
                elif self.clicks == 3:
                    self.controlPointAlt = newEnd
            self.clicks %= self.points
            if self.clicks == 0:
                self.endPoint = newEnd
                self.controlPoint = newEnd
                self.controlPointAlt = newEnd
            elif self.clicks == 1:
                self.controlPoint = newEnd
                self.controlPointAlt = newEnd
            elif self.clicks == 2:
                if self.points == 3:
                    self.createSegment()
                    self.clicks = 3
                    return True
                elif self.points == 4:
                    self.controlPointAlt = newEnd
            elif self.clicks == 3:
                self.createSegment()
                self.clicks = 4
                return True
            self.setPath(self.oldPath)
            path = self.path()
            if self.points == 3:
                path.quadTo(self.controlPoint, self.endPoint)
            elif self.points == 4:
                path.cubicTo(self.controlPoint, self.controlPointAlt, self.endPoint)
            self.setPath(path)
        else:
            if self.editPointNumber == 0:
                path = QtGui.QPainterPath(newEnd)
                if self.points == 3:
                    path.quadTo(self.controlPoint, self.endPoint)
                elif self.points == 4:
                    path.cubicTo(self.controlPoint, self.controlPointAlt, self.endPoint)
            else:
                path = QtGui.QPainterPath(self.startPoint)
            if self.editPointNumber == 1:
                if self.points == 3:
                    path.quadTo(self.controlPoint, newEnd)
                elif self.points == 4:
                    path.cubicTo(self.controlPoint, self.controlPointAlt, newEnd)
            elif self.editPointNumber == 2:
                if self.points == 3:
                    path.quadTo(newEnd, self.endPoint)
                elif self.points == 4:
                    path.cubicTo(newEnd, self.controlPointAlt, self.endPoint)
            elif self.editPointNumber == 3:
                if self.points == 4:
                    path.cubicTo(self.controlPoint, newEnd, self.endPoint)
            self.setPath(path)

    def createSegment(self):
        # Create a new segment (e.g. when LMB is clicked)
        if self.points == 3:
            self.oldPath.quadTo(self.controlPoint, self.endPoint)
        elif self.points == 4:
            self.oldPath.cubicTo(self.controlPoint, self.controlPointAlt, self.endPoint)
        self.setPath(self.oldPath)

    def editPointLocation(self, editPointNumber):
        if editPointNumber == 0:
            return self.startPoint
        elif editPointNumber == 1:
            return self.endPoint
        elif editPointNumber == 2:
            return self.controlPoint
        elif editPointNumber == 3:
            return self.controlPointAlt

    def undoEdit(self):
        points = self.undoPointsList.pop()
        if points is None:
            self.setPath(self.oldPath)
            return
        self.startPoint = points[0]
        # Create a new path
        path = QtGui.QPainterPath(self.startPoint)
        if self.points == 3:
            self.controlPoint = points[1]
            self.endPoint = points[2]
            path.quadTo(self.controlPoint, self.endPoint)
        elif self.points == 4:
            self.controlPoint = points[1]
            self.controlPointAlt = points[2]
            self.endPoint = points[3]
            path.cubicTo(self.controlPoint, self.controlPointAlt, self.endPoint)
        self.oldPath = path
        self.setPath(path)
        self.editPointNumber -= 1
        self.editPointNumber %= self.points

    def redoEdit(self, point=None, clicked=False):
        point = self.mapFromScene(point)
        if self.editPointLocation(self.editPointNumber) == point:
            self.undoPointsList.append(None)
            if clicked is True:
                if self.editPointNumber == 0:
                    self.startPoint = point
                elif self.editPointNumber == 1:
                    self.endPoint = point
                elif self.editPointNumber == 2:
                    self.controlPoint = point
                elif self.editPointNumber == 3 and self.points == 4:
                    self.controlPointAlt = point
                self.editPointNumber += 1
                self.editPointNumber %= self.points
            return
        if self.points == 3:
            self.undoPointsList.append([self.startPoint, self.controlPoint, self.endPoint])
        elif self.points == 4:
            self.undoPointsList.append([self.startPoint, self.controlPoint, self.controlPointAlt, self.endPoint])
        if clicked is True:
            if self.editPointNumber == 0:
                self.startPoint = point
            elif self.editPointNumber == 1:
                self.endPoint = point
            elif self.editPointNumber == 2:
                self.controlPoint = point
            elif self.editPointNumber == 3 and self.points == 4:
                self.controlPointAlt = point
            self.editPointNumber += 1
            self.editPointNumber %= self.points
        # Create a new path
        path = QtGui.QPainterPath(self.startPoint)
        if self.points == 3:
            path.quadTo(self.controlPoint, self.endPoint)
        elif self.points == 4:
            path.cubicTo(self.controlPoint, self.controlPointAlt, self.endPoint)
        self.oldPath = path
        self.setPath(path)
