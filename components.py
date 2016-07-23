from PyQt4 import QtCore, QtGui
import numpy
from drawingitems import TextEditor
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

    def __getstate__(self):
        """Pen and brush objects are not picklable so remove them"""
        localDict = self.__dict__
        localDict.pop('localPen', None)
        localDict.pop('localBrush', None)
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
        """Calculates new origin for when object is rotated/mirrored"""
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
        # Deselect item
        if self.isSelected() is True:
            self.setSelected(False)
        _start = self.pos()
        # Create copy with same pen and brush and start location
        newItem = self.__class__(None, _start, pen=self.localPen, brush=self.localBrush)
        # Apply any transforms (rotations, reflections etc.)
        newItem.setTransform(self.transform())
        # Add new item to scene and then select it
        self.scene().addItem(newItem)
        newItem.setSelected(True)
        newItem.moveTo(0, 0, 'start')
        return newItem

    def opaqueArea(self):
        p = QtGui.QPainterPath()
        p.addRect(self.boundingRect())
        return p

    def hoverEnterEvent(self, event):
        """Turns the item gray when mouse enters its bounding rect"""
        pen = QtGui.QPen(self.localPen)
        pen.setColor(QtGui.QColor('gray'))
        self.setPen(pen)
        brush = QtGui.QBrush(self.localBrush)
        brush.setColor(QtGui.QColor('gray'))
        self.setBrush(brush)
        self.update()

    def hoverLeaveEvent(self, event):
        """Restores the item's original pen and brush when mouse leaves
        its bounding rect
        """
        # self.localPen.setColor(QtGui.QColor(self.localPenColour))
        self.setPen(self.localPen)
        # self.localBrush.setColor(QtGui.QColor(self.localBrushColour))
        self.setBrush(self.localBrush)
        self.update()


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

    def __setstate__(self, state):
        """Reimplemented from drawingElement because group does not have
        pen and brush of its own.
        """
        self.__dict__ = state

    def createCopy(self):
        """Call child copy methods individually after creating new parent"""
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
        newItem.setSelected(True)
        newItem.moveTo(0, 0, 'start')
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
        # For some reason calling the children's hoverEnterEvent did not work
        for item in self.listOfItems:
            pen = QtGui.QPen(item.localPen)
            pen.setColor(QtGui.QColor('gray'))
            if hasattr(item, setPen):
                item.setPen(pen)
            brush = QtGui.QBrush(item.localBrush)
            brush.setColor(QtGui.QColor('gray'))
            if hasattr(item, setBrush):
                item.setBrush(brush)
        self.update()

    def hoverLeaveEvent(self, event):
        # For some reason calling the children's hoverLeaveEvent did not work
        for item in self.listOfItems:
            item.setPen(item.localPen)
            item.setBrush(item.localBrush)
        self.update()

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
        self.setPath(self.oldPath)

    def createCopy(self):
        """Reimplemented from drawingElement. Sets path and origin of the copy
        to that of the original.
        """
        newWire = super(Wire, self).createCopy()
        newWire.setPath(self.path())
        newWire.oldPath = newWire.path()
        if hasattr(self, 'origin'):
            newWire.origin = self.origin
        return newWire


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

    def createCopy(self):
        """Reimplemented from drawingElement. Sets the rect and origin of the
        copy the same as the current rect.
        """
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

    def createCopy(self):
        """Reimplemented from drawingElement. Sets the rect and origin of the
        copy the same as the current ellipse."""
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
        self.setTransformOriginPoint(self.start)
        self.setRotation(theta)
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
        self.localPen.setWidth(self.localPenWidth)
        self.localPen.setColor(QtGui.QColor(self.localPenColour))
        # self.localPen.setStyle(QtCore.Qt.PenStyle(self.localPenStyle))
        self.localPen.setStyle(self.localPenStyle)
        if hasattr(self, 'setFont'):
            font = self.font()
            font.setPointSize(self.localPenWidth*15)
            font.setFamily('Helvetica')
            self.setFont(font)
        if hasattr(self, 'setDefaultTextColor'):
            self.setDefaultTextColor(QtGui.QColor(self.localPenColour))

    def hoverEnterEvent(self, event):
        # Create a textedit to conveniently change the text color
        textEdit = QtGui.QTextEdit()
        textEdit.setHtml(self.toHtml())
        textEdit.selectAll()
        textEdit.setTextColor(QtGui.QColor('gray'))
        self.setHtml(textEdit.toHtml())
        self.setDefaultTextColor(QtGui.QColor('gray'))
        self.update()

    def hoverLeaveEvent(self, event):
        # Create a textedit to conveniently restore the text color
        textEdit = QtGui.QTextEdit()
        textEdit.setHtml(self.toHtml())
        textEdit.selectAll()
        textEdit.setTextColor(QtGui.QColor(self.localPenColour))
        self.setHtml(textEdit.toHtml())
        self.setDefaultTextColor(QtGui.QColor(self.localPenColour))
        self.update()

    def mouseDoubleClickEvent(self, event):
        # Show the editor on double click
        super(TextBox, self).mouseDoubleClickEvent(event)
        self.showEditor()

    def createCopy(self):
        if self.isSelected() is True:
            self.setSelected(False)
        _start = self.pos()
        newItem = self.__class__(None, _start, text=self.toHtml(), pen=self.localPen, brush=self.localBrush)
        newItem.setTransform(self.transform())
        self.scene().addItem(newItem)
        newItem.setSelected(True)
        newItem.moveTo(0, 0, 'start')
        return newItem
