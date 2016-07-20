from PyQt4 import QtCore, QtGui
from components import *
from drawingitems import *
import cPickle as pickle


class DrawingArea(QtGui.QGraphicsView):
    """temp docstring"""

    def __init__(self, parent=None):
        super(DrawingArea, self).__init__(parent)
        self.setScene(QtGui.QGraphicsScene(self))
        self.scene().setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.scene().setSceneRect(QtCore.QRectF(00, 00, 2000, 1000))
        self.parent = parent
        self._keys = {'control': False, 'shift': False, 'c': False,
                      'm': False, 'r': False, 'w': False, 'rectangle': False,
                      'circle': False, 'ellipse': False, 'textBox': False}
        self._mouse = {'1': False}
        self._grid = Grid(None, self, 10)
        self.scene().addItem(self._grid)
        self._grid.createGrid()
        self.enableGrid = True
        self.snapToGrid = True
        self.reflections = 0
        self.rotations = 0
        self.rotateAngle = 90
        self.selectedWidth = 2
        self.selectedPenColour = 'black'
        self.selectedPenStyle = 1
        self.selectedBrushColour = 'black'
        self.selectedBrushStyle = 0
        self.items = []

    def keyPressEvent(self, event):
        super(DrawingArea, self).keyPressEvent(event)
        keyPressed = event.key()
        if (keyPressed == QtCore.Qt.Key_Control):
            # self.setDragMode(QtGui.QGraphicsView.ScrollHandDrag)
            self._keys['control'] = True
        if (keyPressed == QtCore.Qt.Key_Shift):
            self._keys['shift'] = True

    def keyReleaseEvent(self, event):
        super(DrawingArea, self).keyReleaseEvent(event)
        keyPressed = event.key()
        if (keyPressed == QtCore.Qt.Key_Control):
            # self.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
            self._keys['control'] = False
        if (keyPressed == QtCore.Qt.Key_Shift):
            self._keys['shift'] = False
        if (keyPressed == QtCore.Qt.Key_Escape):
            self.escapeRoutine()

    def addWire(self):
        self.escapeRoutine()
        self._keys['w'] = True
        self.currentWire = None

    def addRectangle(self):
        self.escapeRoutine()
        self._keys['rectangle'] = True
        self.currentRectangle = None

    def addCircle(self):
        self.escapeRoutine()
        self._keys['circle'] = True
        self.currentCircle = None

    def addEllipse(self):
        self.escapeRoutine()
        self._keys['ellipse'] = True
        self.currentEllipse = None

    def addTextBox(self):
        self.escapeRoutine()
        cursor = self.cursor()
        cursor.setShape(QtCore.Qt.IBeamCursor)
        self.setCursor(cursor)
        self._keys['textBox'] = True
        self.currentTextBox = None

    def addResistor(self):
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        self.loadRoutine('symbol', './Resources/resistor.pkl')

    def addCapacitor(self):
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        self.loadRoutine('symbol', './Resources/capacitor.pkl')

    def addGround(self):
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        self.loadRoutine('symbol', './Resources/ground.pkl')

    def addDot(self):
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        self.loadRoutine('symbol', './Resources/dot.pkl')

    def addTransistor(self, kind='MOS', polarity='N', arrow=False):
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        if kind == 'MOS':
            if polarity == 'N':
                if arrow is True:
                    self.loadRoutine('symbol', './Resources/nfetArrow.pkl')
                else:
                    self.loadRoutine('symbol', './Resources/nfetNoArrow.pkl')
            else:
                if arrow is True:
                    self.loadRoutine('symbol', './Resources/pfetArrow.pkl')
                else:
                    self.loadRoutine('symbol', './Resources/pfetNoArrow.pkl')
        elif kind == 'BJT':
            if polarity == 'N':
                self.loadRoutine('symbol', './Resources/npnbjt.pkl')
            if polarity == 'P':
                self.loadRoutine('symbol', './Resources/pnpbjt.pkl')

    def saveRoutine(self, mode='export'):
        # Remove grid from the scene to avoid saving it
        self.scene().removeItem(self._grid)
        # Return if no items are present
        if len(self.scene().items()) == 0:
            self.scene().addItem(self._grid)
            return
        if mode == 'symbol' or mode == 'schematic':
            listOfItems = self.scene().items()
            listOfItems = [item for item in listOfItems if item.parentItem() is None]
            x = min([item.scenePos().x() for item in listOfItems])
            y = min([item.scenePos().y() for item in listOfItems])
            origin = QtCore.QPointF(x, y)
            saveObject = myGraphicsItemGroup(None, self.scene(), origin)
            saveObject.origin = origin
            for item in listOfItems:
                item.origin = item.scenePos() - saveObject.origin
                item.transformData = item.transform()
            saveObject.setItems(listOfItems)
            saveFile = str(QtGui.QFileDialog.getSaveFileName(self, 'Save File', './untitled.pkl', 'Objects (*.pkl)'))
            if saveFile != '':
                with open(saveFile, 'wb') as file:
                    pickle.dump(saveObject, file, -1)
            if mode == 'schematic':
                saveObject.reparentItems()
                self.scene().removeItem(saveObject)
        elif mode == 'export':
            # Create a rect that's 1.5 times the boundingrect of all items
            sourceRect = self.scene().itemsBoundingRect()
            scale = 1.5
            sourceRect.setWidth(int(scale*sourceRect.width()))
            sourceRect.setHeight(int(scale*sourceRect.height()))
            width, height = sourceRect.width(), sourceRect.height()
            sourceRect.translate(-width/scale/4., -height/scale/4.)
            # Create a pixmap object
            pixmap = QtGui.QPixmap(QtCore.QSize(4*width, 4*height))
            # Set background to white
            pixmap.fill()
            painter = QtGui.QPainter(pixmap)
            targetRect = QtCore.QRectF(pixmap.rect())
            self.scene().render(painter, targetRect, sourceRect)
            saveFile = str(QtGui.QFileDialog.getSaveFileName(self, 'Save File', './untitled.jpg', 'Images (*.png *.jpg)'))
            if saveFile != '':
                pixmap.save(saveFile, saveFile[-3:])
            # Need to stop painting to avoid errors about painter getting deleted
            painter.end()
        # Add the grid back to the scene when saving is done
        self.scene().addItem(self._grid)

        # printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
        # printer.setOutputFileName('./temp.ps')
        # painter = QtGui.QPainter(printer)
        # self.scene().render(painter)

    def loadRoutine(self, mode='symbol', loadFile=None):
        if mode == 'symbol' or mode == 'schematic':
            if loadFile is None:
                loadFile = str(QtGui.QFileDialog.getOpenFileName(self, 'Load File', './', 'Objects (*.pkl)'))
            if loadFile != '':
                with open(loadFile, 'rb') as file:
                    loadItem = pickle.load(file)
            else:
                return False
            if mode == 'schematic':
                self.scene().removeItem(self._grid)
                self.scene().clear()
                self.scene().addItem(self._grid)
            loadItem.__init__(None, self.scene(), QtCore.QPointF(0, 0), loadItem.listOfItems)
            loadItem.loadItems(mode)
            if mode == 'schematic':
                loadItem.setPos(loadItem.origin)
                # self.scene().destroyItemGroup(loadItem)
                loadItem.reparentItems()
                self.scene().removeItem(loadItem)
            elif mode == 'symbol':
                # loadItem.setLocalPenOptions(penColour=self.selectedPenColour, width=self.selectedWidth, penStyle=self.selectedPenStyle)
                # loadItem.setLocalBrushOptions(brushColour=self.selectedBrushColour, brushStyle=self.selectedBrushStyle)
                loadItem.setPos(self.mapToGrid(self.currentPos))
                loadItem.setSelected(True)
        # Save a copy locally so that items don't disappear
        self.items = self.scene().items()

    def escapeRoutine(self):
        # If mouse had been clicked
        if self._mouse['1'] is True:
            # Unclick mouse
            self._mouse['1'] = False
            # Undo move commands
            if self._keys['m'] is True:
                # Undo reflection command if items were being moved
                if self.reflections == 1:
                    self.rotateRoutine(QtCore.Qt.ShiftModifier)
                # Undo rotation command if items were being moved
                if self.rotations != 0:
                    for i in range(360/self.rotateAngle - self.rotations):
                        self.rotateRoutine()
                if (hasattr(self, 'moveItems')):
                    for i in self.moveItems:
                        i.moveTo(0, 0, 'cancel')
                    self.moveItems = []
            else:
                self.moveItems = []
            # Remove items created as part of copy
            if self._keys['c'] is True:
                for item in self.scene().selectedItems():
                    self.scene().removeItem(item)
            # Remove last wire being drawn
            if self._keys['w'] is True:
                # self.scene().removeItem(self.currentWire)
                self.currentWire.cancelSegment()
            # Remove last rectangle being drawn
            if self._keys['rectangle'] is True:
                self.scene().removeItem(self.currentRectangle)
            # Remove last circle being drawn
            if self._keys['circle'] is True:
                self.scene().removeItem(self.currentCircle)
            # Remove last ellipse being drawn
            if self._keys['ellipse'] is True:
                self.scene().removeItem(self.currentEllipse)
            # Remove last text box being drawn
            if self._keys['textBox'] is True:
                self.scene().removeItem(self.currentTextBox)
        # Zero all rotations and reflections
        self.reflections = 0
        self.rotations = 0
        # Uncheck all keys
        for keys in self._keys:
            self._keys[keys] = False
        # Reset cursor
        cursor = self.cursor()
        cursor.setShape(QtCore.Qt.ArrowCursor)
        self.setCursor(cursor)
        # Save a copy locally so that items don't disappear
        self.items = self.scene().items()

    def moveRoutine(self):
        self.escapeRoutine()
        self._keys['m'] = True

    def copyRoutine(self):
        self.escapeRoutine()
        self._keys['c'] = True
        for i in self.scene().selectedItems():
            i.createCopy()
        # Save a copy locally so that items don't disappear
        self.items = self.scene().items()
        # Start moving after creating copy
        self._keys['m'] = True

    def deleteRoutine(self):
        for i in self.scene().selectedItems():
            self.scene().removeItem(i)

    def fitToViewRoutine(self):
        self.resetMatrix()
        self.ensureVisible(self.scene().itemsBoundingRect())

    def toggleGridRoutine(self):
        self.enableGrid = not self.enableGrid
        if self._grid in self.scene().items():
            self.scene().removeItem(self._grid)
        if self.enableGrid is True:
            self.scene().addItem(self._grid)

    def toggleSnapToGridRoutine(self, state):
        self.snapToGrid = state

    def changeWidthRoutine(self, selectedWidth):
        self.selectedWidth = selectedWidth
        for i in self.scene().selectedItems():
            i.setLocalPenOptions(width=self.selectedWidth)

    def changePenColourRoutine(self, selectedPenColour):
        self.selectedPenColour = selectedPenColour
        for i in self.scene().selectedItems():
            i.setLocalPenOptions(penColour=self.selectedPenColour)

    def changePenStyleRoutine(self, selectedPenStyle):
        self.selectedPenStyle = selectedPenStyle
        for i in self.scene().selectedItems():
            i.setLocalPenOptions(penStyle=self.selectedPenStyle)

    def changeBrushColourRoutine(self, selectedBrushColour):
        self.selectedBrushColour = selectedBrushColour
        for i in self.scene().selectedItems():
            i.setLocalBrushOptions(brushColour=self.selectedBrushColour)

    def changeBrushStyleRoutine(self, selectedBrushStyle):
        self.selectedBrushStyle = selectedBrushStyle
        for i in self.scene().selectedItems():
            i.setLocalBrushOptions(brushStyle=self.selectedBrushStyle)

    def mousePressEvent(self, event):
        self.currentPos = event.pos()
        self.currentX = self.currentPos.x()
        self.currentY = self.currentPos.y()
        if self._keys['m'] is True:
            self.moveItems = self.scene().selectedItems()
            if (event.button() == QtCore.Qt.LeftButton):
                if self.moveItems != []:
                    self._mouse['1'] = not self._mouse['1']
                else:
                    self._mouse['1'] = False
            if (self._mouse['1'] is True):
                self.moveStartPos = self.mapToGrid(event.pos())
                for i in self.moveItems:
                    i.moveTo(0, 0, 'start')
            else:
                for i in self.moveItems:
                    i.moveTo(0, 0, 'done')
        if self._keys['w'] is False:
            super(DrawingArea, self).mousePressEvent(event)

    def rotateRoutine(self, modifier=None):
        self.moveItems = self.scene().selectedItems()
        if self.moveItems != []:
            self.moveItemsGroup = self.scene().createItemGroup(self.moveItems)
            if modifier is None:
                modifier = QtGui.QApplication.keyboardModifiers()
            if modifier == QtCore.Qt.ShiftModifier:
                self.reflections += 1
                self.reflections %= 2
                oldPos = self.moveItemsGroup.sceneBoundingRect(
                ).center().toPoint()
                self.moveItemsGroup.scale(-1, 1)
                newPos = self.moveItemsGroup.sceneBoundingRect(
                ).center().toPoint()
                delta = newPos - oldPos
                self.moveItemsGroup.translate(delta.x(), delta.y())
                if self._keys['m'] is True:
                    for item in self.moveItems:
                        item.modifyMoveOrigin(self.moveStartPos, 'R', True)
            else:
                self.rotations += 1
                self.rotations %= 360/self.rotateAngle
                oldPos = self.moveItemsGroup.sceneBoundingRect(
                ).center().toPoint()
                self.moveItemsGroup.rotate(self.rotateAngle)
                newPos = self.moveItemsGroup.sceneBoundingRect(
                ).center().toPoint()
                delta = newPos - oldPos
                self.moveItemsGroup.translate(-delta.y(), delta.x())
                if self._keys['m'] is True:
                    for item in self.moveItems:
                        item.modifyMoveOrigin(self.moveStartPos, 'r', True)
            self.scene().destroyItemGroup(self.moveItemsGroup)

    def mouseReleaseEvent(self, event):
        if self._keys['m'] is False:
            super(DrawingArea, self).mouseReleaseEvent(event)
        if self._keys['c'] is True:
            self._keys['c'] = False
        # self.oldPos = self.currentPos
        # self.currentPos = event.pos()
        if (self._keys['w'] is True):
            if (event.button() == QtCore.Qt.LeftButton):
                # self._mouse['1'] = not self._mouse['1']
                self._mouse['1'] = True
            if (self._mouse['1'] is True):
                self.oldPos = self.currentPos
                self.currentPos = event.pos()
                self.currentX = self.currentPos.x()
                self.currentY = self.currentPos.y()
                # start = QtCore.QPointF(0, 0)
                # location = self.mapToGrid(self.currentPos)
                start = self.mapToGrid(self.currentPos)
                # self.currentWire = Wire(None, start, location)
                if self.currentWire is None:
                    self.currentWire = Wire(None, start, penColour=self.selectedPenColour, width=self.selectedWidth, penStyle=self.selectedPenStyle, brushColour=self.selectedBrushColour, brushStyle=self.selectedBrushStyle)
                    self.scene().addItem(self.currentWire)
                else:
                    self.currentWire.createSegment(self.mapToGrid(event.pos()))
                # self.scene().addItem(self.currentWire)
        if self._keys['rectangle'] is True:
            if event.button () == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.currentPos = event.pos()
                start = self.mapToGrid(self.currentPos)
                if self.currentRectangle is None:
                    self.currentRectangle = Rectangle(None, start=start, penColour=self.selectedPenColour, width=self.selectedWidth, penStyle=self.selectedPenStyle, brushColour=self.selectedBrushColour, brushStyle=self.selectedBrushStyle)
                    self.scene().addItem(self.currentRectangle)
        if self._keys['circle'] is True:
            if event.button () == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.currentPos = event.pos()
                start = self.mapToGrid(self.currentPos)
                if self.currentCircle is None:
                    self.currentCircle = Circle(None, start=start, penColour=self.selectedPenColour, width=self.selectedWidth, penStyle=self.selectedPenStyle, brushColour=self.selectedBrushColour, brushStyle=self.selectedBrushStyle)
                    self.scene().addItem(self.currentCircle)
        if self._keys['ellipse'] is True:
            if event.button () == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.currentPos = event.pos()
                start = self.mapToGrid(self.currentPos)
                if self.currentEllipse is None:
                    self.currentEllipse = Ellipse(None, start=start, penColour=self.selectedPenColour, width=self.selectedWidth, penStyle=self.selectedPenStyle, brushColour=self.selectedBrushColour, brushStyle=self.selectedBrushStyle)
                    self.scene().addItem(self.currentEllipse)
        if self._keys['textBox'] is True:
            if event.button () == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.currentPos = event.pos()
                start = self.mapToGrid(self.currentPos)
                if self.currentTextBox is None:
                    self.currentTextBox = TextBox(None, start=start, penColour=self.selectedPenColour, width=self.selectedWidth, penStyle=self.selectedPenStyle, brushColour=self.selectedBrushColour, brushStyle=self.selectedBrushStyle)
                    self.scene().addItem(self.currentTextBox)
                self._keys['textBox'] = False
                cursor = self.cursor()
                cursor.setShape(QtCore.Qt.ArrowCursor)
                self.setCursor(cursor)

    def mouseMoveEvent(self, event):
        super(DrawingArea, self).mouseMoveEvent(event)
        self.currentPos = event.pos()
        if (self._mouse['1'] is True):
            # self.oldPos = self.currentPos
            self.oldX = self.currentX
            self.oldY = self.currentY
            self.currentX = self.currentPos.x()
            self.currentY = self.currentPos.y()
            if (self._keys['control'] is False):
                if self._keys['w'] is True:
                    self.currentWire.updateWire(self.mapToGrid(event.pos()))
                if self._keys['rectangle'] is True:
                    self.currentRectangle.updateRectangle(self.mapToGrid(event.pos()))
                if self._keys['circle'] is True:
                    self.currentCircle.updateCircle(self.mapToGrid(event.pos()))
                if self._keys['ellipse'] is True:
                    self.currentEllipse.updateEllipse(self.mapToGrid(event.pos()))
                if self._keys['m'] is True:
                # elif (self._keys['m'] is True):
                    self.moveStopPos = self.mapToGrid(event.pos())
                    for i in self.moveItems:
                        x = self.moveStopPos.x() - self.moveStartPos.x()
                        y = self.moveStopPos.y() - self.moveStartPos.y()
                        i.moveTo(x, y, 'move')
            else:
                self.translate(self.oldX - self.currentX,
                               self.oldY - self.currentY)

    def contextMenuEvent(self, event):
        menu = QtGui.QMenu()
        actionDelete = menu.addAction('&Delete')
        actionDelete.triggered.connect(lambda: self.scene().removeItem(self))
        menu.exec_(event.screenPos())

    def mapToGrid(self, point):
        point = self.mapToScene(point)
        if self.snapToGrid is True:
            return self._grid.snapTo(point)
        else:
            return point

    def wheelEvent(self, event):
        scaleFactor = -event.delta() / 240.
        if self._keys['control'] is True:
            self.translate(0, -scaleFactor * 20)
        elif self._keys['shift'] is True:
            self.translate(-scaleFactor * 20, 0)
        else:
            if scaleFactor < 0:
                scaleFactor = -1 / scaleFactor
            scaleFactor = 1 + (scaleFactor - 1) / 5.
            # else:
            #     scaleFactor = scaleFactor*1.5
            oldPos = self.mapToScene(event.pos())
            self.scale(scaleFactor, scaleFactor)
            self._grid.createGrid()
            newPos = self.mapToScene(event.pos())
            delta = newPos - oldPos
            self.translate(delta.x(), delta.y())
