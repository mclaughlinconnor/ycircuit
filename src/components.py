from PyQt4 import QtCore, QtGui
import numpy
from src.drawingitems import TextEditor
import sys

class drawingElement(object):
    """The drawingElement forms part of the basis for all drawing classes.
    It contains methods for setting pen and brush options, moving, copying etc.
    """
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
        self.reflections = 0

    def __getstate__(self):
        """Pen and brush objects are not picklable so remove them"""
        localDict = self.__dict__
        localDict.pop('localPen', None)
        localDict.pop('localBrush', None)
        localDict['transformData'] = self.transform()
        return localDict

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
        rotation_ = 180/numpy.pi * numpy.arctan2(-transform_.m21(), transform_.m11())
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
        newItem = self.__class__(parent, _start, pen=self.localPen, brush=self.localBrush)
        # Apply any transforms (rotations, reflections etc.)
        newItem.setTransform(self.transform())
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
        self.changeColourToGray(True)

    def hoverLeaveEvent(self, event):
        """Restores the item's original pen and brush when mouse leaves
        its bounding rect
        """
        self.changeColourToGray(False)

    def changeColourToGray(self, gray=False):
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
        if gray == True:
            pen.setColor(QtGui.QColor('gray'))
            brush.setColor(QtGui.QColor('gray'))
        self.setPen(pen)
        self.setBrush(brush)

    def undoEdit(self):
        """Handled by classes individually"""
        pass

    def redoEdit(self, point=None):
        """Handled by classes individually"""
        pass


class myGraphicsItemGroup(QtGui.QGraphicsItem, drawingElement):
    """Subclassed from QGraphicsItem. Provides additional methods so that
    the parent item remembers all the items that are its children.
    """
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
        """Call child paint methods individually"""
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

    def sceneBoundingRect(self):
        rect = self.listOfItems[0].sceneBoundingRect()
        for item in self.listOfItems:
            rect = rect.united(item.sceneBoundingRect())
        return rect

    def __setstate__(self, state):
        """Reimplemented from drawingElement because group does not have
        pen and brush of its own.
        """
        self.__dict__ = state

    def createCopy(self, parent=None):
        """Call child copy methods individually after creating new parent"""
        self.setSelected(False)
        _start = self.pos()
        # If parent exists, will get added to parent's scene
        if parent is None:
            newItem = self.__class__(parent, self.scene(), _start)
        else:
            newItem = self.__class__(parent, None, _start)
        newItem.listOfItems = []
        for item in self.listOfItems:
            itemCopy = item.createCopy(newItem)
            newItem.listOfItems.append(itemCopy)
        newItem.setItems(newItem.listOfItems)
        newItem.setTransform(self.transform())
        newItem.origin = self.origin
        newItem.setSelected(True)
        if newItem.parentItem() is None:
            newItem.moveTo(self.scenePos(), 'start')
        else:
            newItem.setPos(newItem.origin)
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

    # def getLocalPenOptions(self, option):
    #     """Get child local pen options as a list"""
    #     if option == 'width':
    #         list_ = []
    #         for item in self.listOfItems:
    #             if isinstance(item, myGraphicsItemGroup):
    #                 list_.append(item.getLocalPenOptions(option))
    #             else:
    #                 list_.append(item.localPenWidth)
    #     return list_

    def setLocalPenOptions(self, **kwargs):
        """Set pen individually for each child item"""
        for item in self.listOfItems:
            if not hasattr(item, 'localPen'):
                item.localPen = QtGui.QPen()
            item.setLocalPenOptions(**kwargs)

    def setLocalBrushOptions(self, **kwargs):
        """Set brush individually for each child item"""
        for item in self.listOfItems:
            if not hasattr(item, 'localBrush'):
                item.localBrush = QtGui.QBrush()
            item.setLocalBrushOptions(**kwargs)

    def hoverEnterEvent(self, event):
        self.changeColourToGray(True)

    def hoverLeaveEvent(self, event):
        self.changeColourToGray(False)

    def changeColourToGray(self, gray=False):
        for item in self.listOfItems:
            item.changeColourToGray(gray)

    def loadItems(self, mode='symbol'):
        """Initializes items in self.listOfItems."""
        for item in self.listOfItems:
            if not isinstance(item, myGraphicsItemGroup):
                item.__init__(self, item.origin, penColour=item.localPenColour, width=item.localPenWidth, penStyle=item.localPenStyle, brushColour=item.localBrushColour, brushStyle=item.localBrushStyle)
            else:
                item.__init__(self, self.scene(), item.origin, item.listOfItems)
                # Call loadItems if item is also a myGraphicsItemGroup
                item.loadItems(mode)
        self.setItems(self.listOfItems)

    def undoEdit(self):
        for item in self.listOfItems:
            item.undoEdit()

    def redoEdit(self, point=None):
        for item in self.listOfItems:
            item.redoEdit(point)


class Wire(QtGui.QGraphicsPathItem, drawingElement):
    """Subclassed from the PyQt implementation of standard lines. Provides some
    added convenience functions and enables object-like interaction"""
    def __init__(self, parent=None, start=None, **kwargs):
        point = QtCore.QPointF(0, 0)
        # For when wire is being loaded from a file, oldPath already exists
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
        # Add a list of all points part of the wire
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
        # Add a polygon corresponding to the list of saved points
        a = QtGui.QPolygonF(state['polyPathPointList'][0])
        self.oldPath2 = QtGui.QPainterPath()
        for item in state['polyPathPointList']:
            poly = QtGui.QPolygonF(item)
            self.oldPath2.addPolygon(poly)
        self.oldPath = self.__dict__.pop('oldPath2', None)

    def updateWire(self, newEnd):
        # Update existing segment to end at newEnd
        newEnd = self.mapFromScene(newEnd)
        self.setPath(self.oldPath)
        path = self.path()
        path.lineTo(newEnd)
        self.setPath(path)

    def createSegment(self, newEnd):
        # Create a new segment (e.g. when LMB is clicked)
        newEnd = self.mapFromScene(newEnd)
        self.oldPath.lineTo(newEnd)
        self.setPath(self.oldPath)

    def cancelSegment(self):
        # Remove from scene if no segment exists
        if self.oldPath.toSubpathPolygons() == []:
            self.scene().removeItem(self)
        else:
            self.setPath(self.oldPath)

    def createCopy(self, parent=None):
        """Reimplemented from drawingElement. Sets path and origin of the copy
        to that of the original.
        """
        newWire = super(Wire, self).createCopy(parent)
        newWire.setPath(self.path())
        newWire.oldPath = newWire.path()
        if hasattr(self, 'origin'):
            newWire.origin = self.origin
        return newWire


    def undoEdit(self):
        if len(self.oldPath.toSubpathPolygons()) == 0:
            return False
        lastPoly = self.oldPath.toSubpathPolygons()[-1]
        lastPoly.remove(lastPoly.size()-1)
        otherPoly = self.oldPath.toSubpathPolygons()[:-1]
        path = QtGui.QPainterPath()
        for i in otherPoly:
            path.addPolygon(i)
        path.addPolygon(lastPoly)
        self.oldPath = path
        self.setPath(self.oldPath)

    def redoEdit(self, point=None):
        self.createSegment(point)


class Rectangle(QtGui.QGraphicsRectItem, drawingElement):
    """Class responsible for drawing rectangular objects"""
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
        # Make the bounding rect a little bigger so it is easier to see
        pad = 10
        bottomLeft = self.rect().bottomLeft() + QtCore.QPointF(-pad, pad)
        topRight = self.rect().topRight() + QtCore.QPointF(pad, -pad)
        rect = QtCore.QRectF(bottomLeft, topRight)
        return rect

    def paint(self, painter, *args):
        # We have to manually draw out the bounding rect
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
        # Update the end point of the rectangle to end
        end = self.mapFromScene(end)
        rect = QtCore.QRectF(self.start, end)
        self.setRect(rect)
        self.oldRect = rect
        # If items collide with this one, elevate them
        collidingItems = self.collidingItems()
        for item in collidingItems:
            if item.isObscuredBy(self):
                item.setZValue(item.zValue() + 1)

    def createCopy(self, parent=None):
        """Reimplemented from drawingElement. Sets the rect and origin of the
        copy the same as the current rect.
        """
        newRectangle = super(Rectangle, self).createCopy(parent)
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
    """Class responsible for drawing elliptical objects"""
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
        # Make the bounding rect a little bigger so that it is easier to see
        pad = 10
        # Not sure why this is different from the Rectangle boundingRect
        bottomLeft = self.rect().bottomLeft() + QtCore.QPointF(-pad, -pad)
        topRight = self.rect().topRight() + QtCore.QPointF(pad, pad)
        rect = QtCore.QRectF(bottomLeft, topRight)
        return rect

    def paint(self, painter, *args):
        # We have to manually draw out the bounding rect
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
        # Update the end point of the ellipse to end
        end = self.mapFromScene(end)
        rect = QtCore.QRectF(self.start, end)
        self.setRect(rect)
        self.oldRect = rect
        # If items collide with this one, elevate them
        collidingItems = self.collidingItems()
        for item in collidingItems:
            if item.isObscuredBy(self):
                item.setZValue(item.zValue() + 1)

    def createCopy(self, parent=None):
        """Reimplemented from drawingElement. Sets the rect and origin of the
        copy the same as the current ellipse."""
        newEllipse = super(Ellipse, self).createCopy(parent)
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
    """This is a special case of the Ellipse class where a = b."""
    def __init__(self, parent=None, start=None, **kwargs):
        super(Circle, self).__init__(parent, start, **kwargs)

    def boundingRect(self):
        # Make the bounding rect a little bigger so that it is easier to see
        pad = 10
        # This is the same as that for rectangle
        bottomLeft = self.rect().bottomLeft() + QtCore.QPointF(-pad, pad)
        topRight = self.rect().topRight() + QtCore.QPointF(pad, -pad)
        rect = QtCore.QRectF(bottomLeft, topRight)
        return rect

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
            theta = 180/numpy.pi*numpy.arctan2(distanceLine.y(), distanceLine.x())
        sideLength = numpy.sqrt(distanceLine.x()**2 + distanceLine.y()**2)
        square = QtCore.QRectF(self.start + QtCore.QPointF(0, -sideLength/2), QtCore.QSizeF(sideLength, sideLength))
        self.setRect(square)
        self.transform_ = QtGui.QTransform()
        self.transform_.translate(0, 0)
        self.transform_.rotate(theta)
        self.setTransform(self.transform_)
        self.oldRect = self.rect()
        # If items collide with this one, elevate them
        collidingItems = self.collidingItems()
        for item in collidingItems:
            if item.isObscuredBy(self):
                item.setZValue(item.zValue() + 1)


class TextBox(QtGui.QGraphicsTextItem, drawingElement):
    """Responsible for showing formatted text as well as LaTeX images.
    The current formatting options are supported:
        1. Bold
        2. Italic
        3. Underline
        4. Subscript
        5. Superscript
    LaTeX images are displayed in place of the text.
    TODO: Fix size issues with rendered LaTeX images
    TODO: Grey out LaTeX images on mouse hover
    TODO: Delete corresponding LaTeX image files when textbox is deleted
    """
    def __init__(self, parent=None, start=None, text='', **kwargs):
        point = QtCore.QPointF(0, 0)
        if not hasattr(self, 'origin'):
            super(TextBox, self).__init__(parent)
            self.setPos(start)
        else:
            super(TextBox, self).__init__(parent)
            self.setPos(self.origin)
        # Set the fixed vertex to (0, 0) in local coordinates
        drawingElement.__init__(self, parent, start=point, **kwargs)
        self.setTextWidth(-1)
        # Instantiate variables if none exist already
        if not hasattr(self, 'latexImageHtml'):
            self.latexImageHtml = None
            self.latexExpression = None
        if text != '':
            self.setHtml(text)
        elif hasattr(self, 'htmlText'):
            self.setHtml(self.htmlText)
        elif self.latexImageHtml is not None:
            self.setHtml(self.latexImageHtml)
        else:
            self.showEditor()

    def __getstate__(self):
        localDict = super(TextBox, self).__getstate__()
        localDict.pop('textEditor', None)
        # Add htmlText to the dict
        localDict['htmlText'] = self.toHtml()
        return localDict

    def showEditor(self):
        self.textEditor = TextEditor(self)
        self.textEditor.show()

    def setLocalPenOptions(self, **kwargs):
        """Reimplemented from drawingElement. QGraphicsTextItem objects do not
        have pens and brushes. Further, they have fonts whose sizes and widths
        can be changed.
        """
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
        if hasattr(self, 'setFont'):
            font = self.font()
            font.setPointSize(self.localPenWidth*10)
            font.setFamily('Arial')
            self.setFont(font)
        self.changeTextSize(self.localPenWidth)
        self.changeTextColour(self.localPenColour)

    def changeTextColour(self, colour='gray'):
        # Create a textedit to conveniently change the text color
        textEdit = QtGui.QTextEdit()
        textEdit.setHtml(self.toHtml())
        textEdit.selectAll()
        textEdit.setTextColor(QtGui.QColor(colour))
        self.setHtml(textEdit.toHtml())
        self.setDefaultTextColor(QtGui.QColor(colour))
        self.update()

    def changeTextSize(self, weight=4):
        # Create a textedit to conveniently change the text size
        textEdit = QtGui.QTextEdit()
        textEdit.setHtml(self.toHtml())
        textEdit.selectAll()
        textEdit.setFontPointSize(weight*10)
        self.setHtml(textEdit.toHtml())
        self.update()

    def hoverEnterEvent(self, event):
        self.changeTextColour('gray')

    def hoverLeaveEvent(self, event=None):
        self.changeTextColour(self.localPenColour)

    def mouseDoubleClickEvent(self, event):
        # Show the editor on double click
        super(TextBox, self).mouseDoubleClickEvent(event)
        # Reset the text colour from gray
        self.hoverLeaveEvent()
        self.showEditor()

    def createCopy(self, parent=None):
        if self.isSelected() is True:
            self.setSelected(False)
        _start = self.pos()
        newItem = self.__class__(parent, _start, text=self.toHtml(), pen=self.localPen, brush=self.localBrush)
        newItem.setTransform(self.transform())
        self.scene().addItem(newItem)
        newItem.setSelected(True)
        newItem.moveTo(self.scenePos(), 'start')
        return newItem


class Arc(Wire):
    """This is a special case of the Wire class where repeated clicks change the curvature
    of the wire."""
    def __init__(self, parent=None, start=None, **kwargs):
        super(Arc, self).__init__(parent, start, **kwargs)
        if 'points' in kwargs:
            self.points = kwargs['points']
        self.clicks = 0
        self.setFocus()

    def updateArc(self, newEnd, click=False):
        self.setFocus()
        newEnd = self.mapFromScene(newEnd)
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

    def createSegment(self):
        # Create a new segment (e.g. when LMB is clicked)
        if self.points == 3:
            self.oldPath.quadTo(self.controlPoint, self.endPoint)
        elif self.points == 4:
            self.oldPath.cubicTo(self.controlPoint, self.controlPointAlt, self.endPoint)
        self.setPath(self.oldPath)

    def undoEdit(self):
        if self.clicks > 0:
            self.clicks -= 1

    def redoEdit(self, point=None):
        self.updateArc(point, click=True)