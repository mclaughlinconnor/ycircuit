from PyQt4 import QtCore, QtGui, QtSvg
from src.components import *
from src.drawingitems import *
from src.commands import *
import cPickle as pickle
import os
from numpy import ceil, floor
# from src import components
# import sys
# sys.modules['components'] = components


class DrawingArea(QtGui.QGraphicsView):
    """The drawing area is subclassed from QGraphicsView to provide additional
    functionality specific to this schematic drawing tool. Further information about
    these modifications is present in the method docstrings.
    """

    def __init__(self, parent=None):
        """Initializes the object and various parameters to default values"""
        super(DrawingArea, self).__init__(parent)
        self.setScene(QtGui.QGraphicsScene(self))
        self.scene().setItemIndexMethod(QtGui.QGraphicsScene.NoIndex)
        self.scene().setSceneRect(QtCore.QRectF(0, 0, 2000, 2000))
        self.parent = parent
        self._keys = {'c': False, 'm': False, 'r': False, 'w': False,
                      'arc': False, 'rectangle': False, 'circle': False,
                      'ellipse': False, 'textBox': False}
        self._mouse = {'1': False}
        self._grid = Grid(None, self, 10)
        self.scene().addItem(self._grid)
        self._grid.createGrid()
        self.enableGrid = True
        self.snapToGrid = True
        self.undoStack = QtGui.QUndoStack(self)
        self.undoStack.setUndoLimit(1000)
        self.reflections = 0
        self.rotations = 0
        self.rotateAngle = 30
        self.selectedWidth = 4
        self.selectedPenColour = 'black'
        self.selectedPenStyle = 1
        self.selectedBrushColour = 'black'
        self.selectedBrushStyle = 0
        self.items = []
        self.moveItems = []
        self.schematicFileName = None
        self.symbolFileName = None

    def keyReleaseEvent(self, event):
        """Run escapeRoutine when the escape button is pressed"""
        super(DrawingArea, self).keyReleaseEvent(event)
        keyPressed = event.key()
        if (keyPressed == QtCore.Qt.Key_Escape):
            self.escapeRoutine()

    def addWire(self):
        """Set _key to wire mode so that a wire is added when LMB is pressed"""
        self.escapeRoutine()
        self._keys['w'] = True
        self.currentWire = None

    def addArc(self, points=3):
        """Set _key to arc mode so that an arc is added when LMB is pressed"""
        self.escapeRoutine()
        self._keys['arc'] = True
        self.arcPoints = points
        self.currentArc = None

    def addRectangle(self):
        """Set _key to wire mode so that a rectangle is added when LMB is pressed"""
        self.escapeRoutine()
        self._keys['rectangle'] = True
        self.currentRectangle = None

    def addCircle(self):
        """Set _key to wire mode so that a circle is added when LMB is pressed"""
        self.escapeRoutine()
        self._keys['circle'] = True
        self.currentCircle = None

    def addEllipse(self):
        """Set _key to wire mode so that an ellipse is added when LMB is pressed"""
        self.escapeRoutine()
        self._keys['ellipse'] = True
        self.currentEllipse = None

    def addTextBox(self):
        """Set _key to wire mode so that a textbox is added when LMB is pressed"""
        self.escapeRoutine()
        cursor = self.cursor()
        cursor.setShape(QtCore.Qt.IBeamCursor)
        self.setCursor(cursor)
        self._keys['textBox'] = True
        self.currentTextBox = None

    def addResistor(self):
        """Load the standard resistor"""
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        self.loadRoutine('symbol', './Resources/Symbols/Standard/resistor.sym')

    def addCapacitor(self):
        """Load the standard capacitor"""
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        self.loadRoutine('symbol', './Resources/Symbols/Standard/capacitor.sym')

    def addGround(self):
        """Load the standard ground symbol"""
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        self.loadRoutine('symbol', './Resources/Symbols/Standard/ground.sym')

    def addDot(self):
        """Load the standard dot symbol"""
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        self.loadRoutine('symbol', './Resources/Symbols/Standard/dot.sym')

    def addTransistor(self, kind='MOS', polarity='N', arrow=False):
        """Load the standard transistor symbol based on its kind and polarity"""
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        if kind == 'MOS':
            if polarity == 'N':
                if arrow is True:
                    self.loadRoutine('symbol', './Resources/Symbols/Standard/nfetArrow.sym')
                else:
                    self.loadRoutine('symbol', './Resources/Symbols/Standard/nfetNoArrow.sym')
            else:
                if arrow is True:
                    self.loadRoutine('symbol', './Resources/Symbols/Standard/pfetArrow.sym')
                else:
                    self.loadRoutine('symbol', './Resources/Symbols/Standard/pfetNoArrow.sym')
        elif kind == 'BJT':
            if polarity == 'N':
                self.loadRoutine('symbol', './Resources/Symbols/Standard/npnbjt.sym')
            if polarity == 'P':
                self.loadRoutine('symbol', './Resources/Symbols/Standard/pnpbjt.sym')

    def addSource(self, kind='DCV'):
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        if kind == 'DCV':
            self.loadRoutine('symbol', './Resources/Symbols/Standard/dcVoltageSource.sym')
        elif kind == 'DCI':
            self.loadRoutine('symbol', './Resources/Symbols/Standard/dcCurrentSource.sym')
        elif kind == 'AC':
            self.loadRoutine('symbol', './Resources/Symbols/Standard/acSource.sym')
        elif kind == 'VCVS':
            self.loadRoutine('symbol', './Resources/Symbols/Standard/vcvs.sym')
        elif kind == 'VCCS':
            self.loadRoutine('symbol', './Resources/Symbols/Standard/vccs.sym')
        elif kind == 'CCVS':
            self.loadRoutine('symbol', './Resources/Symbols/Standard/ccvs.sym')
        elif kind == 'CCCS':
            self.loadRoutine('symbol', './Resources/Symbols/Standard/cccs.sym')

    def saveRoutine(self, mode='schematicAs'):
        """Handles saving of both symbols and schematics. For symbols and
        schematics, items are first parented to a myGraphicsItemGroup.
        The parent item is then saved into a corresponding .sym (symbol) and
        .sch (schematic) file. If the save option is a schematic, the items are then
        unparented.
        """
        possibleModes = ['schematic', 'schematicAs', 'symbol', 'symbolAs']
        # Remove grid from the scene to avoid saving it
        self.scene().removeItem(self._grid)
        # Return if no items are present
        if len(self.scene().items()) == 0:
            self.scene().addItem(self._grid)
            return
        if mode in possibleModes:
            listOfItems = self.scene().items()
            listOfItems = [item for item in listOfItems if item.parentItem() is None]
            x = min([item.scenePos().x() for item in listOfItems])
            y = min([item.scenePos().y() for item in listOfItems])
            origin = QtCore.QPointF(x, y)
            saveObject = myGraphicsItemGroup(None, self.scene(), origin)
            saveObject.origin = origin
            # print saveObject, saveObject.origin
            # Set relative origins of child items

            for item in listOfItems:
                item.origin = item.pos() - saveObject.origin
                # print item, item.origin
            saveObject.setItems(listOfItems)

            if mode == 'symbol':
                if self.symbolFileName is None:
                    saveFile = str(QtGui.QFileDialog.getSaveFileName(self, 'Save symbol', './Resources/Symbols/Custom/untitled.sym', 'Symbols (*.sym)'))
                else:
                    saveFile = self.symbolFileName
            elif mode == 'symbolAs':
                saveFile = str(QtGui.QFileDialog.getSaveFileName(self, 'Save symbol as', './Resources/Symbols/Custom/untitled.sym', 'Symbols (*.sym)'))
            elif mode == 'schematic':
                if self.schematicFileName is None:
                    saveFile = str(QtGui.QFileDialog.getSaveFileName(self, 'Save schematic', './untitled.sch', 'Schematics (*.sch)'))
                else:
                    saveFile = self.schematicFileName
            elif mode == 'schematicAs':
                saveFile = str(QtGui.QFileDialog.getSaveFileName(self, 'Save schematic as', './untitled.sch', 'Schematics (*.sch)'))

            if saveFile != '':
                with open(saveFile, 'wb') as file:
                    pickle.dump(saveObject, file, -1)
                if mode == 'symbol' or mode == 'symbolAs':
                    self.symbolFileName = saveFile
                    self.schematicFileName = None
                if mode == 'schematic' or mode == 'schematicAs':
                    self.schematicFileName = saveFile
                    self.symbolFileName = None
                self.undoStack.clear()
            if mode == 'schematic' or mode == 'schematicAs':
                saveObject.reparentItems()
                self.scene().removeItem(saveObject)
        # Add the grid back to the scene when saving is done
        self.scene().addItem(self._grid)

    def exportRoutine(self):
        """
        For images, a rect slightly larger than the bounding rect of all items is
        created. This rect is then projected onto a QPixmap at a higher resolution to
        create the final image.
        """
        # Remove grid from the scene to avoid saving it
        self.scene().removeItem(self._grid)
        # Return if no items are present
        if len(self.scene().items()) == 0:
            self.scene().addItem(self._grid)
            return
        saveFile = str(QtGui.QFileDialog.getSaveFileName(self, 'Export File', './untitled.pdf', 'PDF and EPS files (*.pdf *.eps);; SVG files(*.svg);; Images (*.png *.jpg *.jpeg *.bmp)'))
        # Check that file is valid
        if saveFile == '':
            # Add the grid back to the scene
            self.scene().addItem(self._grid)
            return
        if saveFile[-3:] in ['pdf', 'eps']:
            mode = 'pdf'
        elif saveFile[-3:] == 'svg':
            mode = 'svg'
        elif saveFile[-3:] in ['jpg', 'png', 'bmp', 'jpeg']:
            mode = 'image'
        if mode == 'pdf':
            # Initialize printer
            printer = QtGui.QPrinter(QtGui.QPrinter.HighResolution)
            sourceRect = self.scene().itemsBoundingRect()
            # Choose appropriate format
            if saveFile[-3:] == 'pdf':
                printer.setOutputFormat(printer.PdfFormat)
            if saveFile[-3:] == 'eps':
                printer.setFullPage(True)
                printer.setOutputFormat(printer.PostScriptFormat)
            printer.setOutputFileName(saveFile)
            painter = QtGui.QPainter(printer)
            self.scene().render(painter, source=sourceRect)
        elif mode == 'svg':
            svgGenerator = QtSvg.QSvgGenerator()
            svgGenerator.setFileName(saveFile)
            sourceRect = self.scene().itemsBoundingRect()
            width, height = sourceRect.width(), sourceRect.height()
            svgGenerator.setSize(QtCore.QSize(width, height))
            svgGenerator.setViewBox(QtCore.QRect(0, 0, width, height))
            painter = QtGui.QPainter(svgGenerator)
            self.scene().render(painter, source=sourceRect)
        elif mode == 'image':
            # Create a rect that's 1.5 times the boundingrect of all items
            sourceRect = self.scene().itemsBoundingRect()
            scale = 1.1
            sourceRect.setWidth(int(scale*sourceRect.width()))
            sourceRect.setHeight(int(scale*sourceRect.height()))
            width, height = sourceRect.width(), sourceRect.height()
            if not scale < 1:
                sourceRect.translate(-width*(scale - 1)/2., -height*(scale - 1)/2.)
            # Create a pixmap object
            pixmap = QtGui.QPixmap(QtCore.QSize(4*width, 4*height))
            # Set background to white
            pixmap.fill()
            painter = QtGui.QPainter(pixmap)
            targetRect = QtCore.QRectF(pixmap.rect())
            self.scene().render(painter, targetRect, sourceRect)
            pixmap.save(saveFile, saveFile[-3:])

        # Need to stop painting to avoid errors about painter getting deleted
        painter.end()
        # Add the grid back to the scene when saving is done
        self.scene().addItem(self._grid)
        if saveFile[-3:] == 'eps':
            printerSize = printer.paperSize(printer.DevicePixel)
            self.fixEPSBoundingBox(saveFile, printerSize, sourceRect)

    def fixEPSBoundingBox(self, saveFile, printerSize, sourceRect):
        # Adapted from https://github.com/jeremysanders/veusz/blob/master/veusz/document/export.py
        width, height = sourceRect.width(), sourceRect.height()
        tempFile = '%s.eps.temp' % (saveFile[:-4])
        with open(saveFile, 'rU') as fIn:
            with open(tempFile, 'w') as fOut:
                for line in fIn:
                    if line[:14] == '%%BoundingBox:':
                        parts = line.split()
                        origwidth = float(parts[3])
                        origheight = float(parts[4])
                        if width/height >= printerSize.width()/printerSize.height():
                            stretch = origwidth/width
                            line = '%s %i %i %i %i\n' %(parts[0], 0, int(floor(origheight-stretch*height)), int(ceil(origwidth)), int(ceil(origheight)))
                        else:
                            stretch = origheight/height
                            line = '%s %i %i %i %i\n' %(parts[0], 0, 0, int(ceil(stretch*width)), int(ceil(origheight)))
                    fOut.write(line)
        os.remove(saveFile)
        os.rename(tempFile, saveFile)

    def loadRoutine(self, mode='symbol', loadFile=None):
        """This is the counterpart of the save routine. Used to load both schematics
        and symbols.
        """
        possibleModes = ['schematic', 'symbol', 'symbolModify']
        if mode in possibleModes:
            if loadFile is None:
                if mode == 'symbol' or mode == 'symbolModify':
                    loadFile = str(QtGui.QFileDialog.getOpenFileName(self, 'Load Symbol', './Resources/Symbols/', 'Symbols (*.sym)'))
                elif mode == 'schematic':
                    loadFile = str(QtGui.QFileDialog.getOpenFileName(self, 'Load Schematic', './', 'Schematics (*.sch)'))
            if loadFile != '':
                with open(loadFile, 'rb') as file:
                    loadItem = pickle.load(file)
            else:
                return False
            if mode == 'schematic' or mode == 'symbolModify':
                # Remove grid from scene, clear the scene and readd the grid
                self.schematicFileName = None
                self.symbolFileName = None
                if mode == 'schematic':
                    self.schematicFileName = loadFile
                elif mode == 'symbolModify':
                    self.symbolFileName = loadFile
                self.scene().removeItem(self._grid)
                self.scene().clear()
                self.scene().addItem(self._grid)
                loadItem.__init__(None, self.scene(), QtCore.QPointF(0, 0), loadItem.listOfItems)
                loadItem.loadItems(mode)
            elif mode == 'symbol':
                add = Add(None, self.scene(), loadItem, symbol=True, origin=self.mapToGrid(self.currentPos))
                self.undoStack.push(add)
            if mode == 'schematic' or mode == 'symbolModify':
                loadItem.setPos(loadItem.origin)
                loadItem.reparentItems()
                self.scene().removeItem(loadItem)
                self.fitToViewRoutine()
            elif mode == 'symbol':
                # Symbols are created with the pen/brush that they were saved in
                loadItem.setPos(self.mapToGrid(self.currentPos))
                loadItem.setSelected(True)
        # Save a copy locally so that items don't disappear
        self.items = self.scene().items()

    def escapeRoutine(self):
        """Resets all variables to the default state"""
        # If mouse had been clicked
        if self._mouse['1'] is True:
            # Unclick mouse
            self._mouse['1'] = False
            # Undo move commands
            if self._keys['m'] is True:
                self.undoStack.endMacro()
                self.undoStack.undo()
                # Undo reflection command if items were being moved
                # if self.reflections == 1:
                #     self.rotateRoutine(QtCore.Qt.ShiftModifier)
                # Undo rotation command if items were being moved
                # if self.rotations != 0:
                #     for i in range(360/self.rotateAngle - self.rotations):
                #         self.rotateRoutine()
                if (hasattr(self, 'moveItems')):
                    for i in self.moveItems:
                        # i.moveTo(0, 0, 'cancel')
                        i.moveTo(None, 'cancel')
                    self.moveItems = []
            else:
                self.moveItems = []
            # Remove items created as part of copy independent of mouseclick
            if self._keys['c'] is True:
                for item in self.scene().selectedItems():
                    self.scene().removeItem(item)
            # Remove last wire being drawn
            if self._keys['w'] is True:
                # self.scene().removeItem(self.currentWire)
                self.currentWire.cancelSegment()
            # Remove last arc being drawn
            if self._keys['arc'] is True:
                self.currentArc.cancelSegment()
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
        """Preps to begin moving items"""
        self.escapeRoutine()
        self.updateMoveItems()
        self._keys['m'] = True

    def copyRoutine(self):
        """Preps to begin copying items"""
        self.escapeRoutine()
        self._keys['c'] = True

    def deleteRoutine(self):
        """Delete selected items"""
        del1 = Delete(None, self.scene(), self.scene().selectedItems())
        self.undoStack.push(del1)

    def fitToViewRoutine(self):
        """Resizes viewport so that all items drawn are visible"""
        if len(self.scene().items()) == 1:
            # Fit to (0, 0, 800, 800) if nothing is present
            rect = QtCore.QRectF(0, 0, 500, 500)
            self.fitInView(rect, QtCore.Qt.KeepAspectRatio)
        else:
            self.scene().removeItem(self._grid)
            self.fitInView(self.scene().itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
            self.scene().addItem(self._grid)
        self._grid.createGrid()

    def toggleGridRoutine(self):
        """Toggles grid on and off"""
        self.enableGrid = not self.enableGrid
        if self._grid in self.scene().items():
            self.scene().removeItem(self._grid)
        if self.enableGrid is True:
            self.scene().addItem(self._grid)

    def toggleSnapToGridRoutine(self, state):
        """Toggles drawings snapping to grid"""
        self.snapToGrid = state

    def changeWidthRoutine(self, selectedWidth):
        if selectedWidth != self.selectedWidth:
            self.selectedWidth = selectedWidth
            if self.scene().selectedItems() != []:
                changePen = ChangePen(None, self.scene().selectedItems(), width=self.selectedWidth)
                self.undoStack.push(changePen)

    def changePenColourRoutine(self, selectedPenColour):
        if selectedPenColour != self.selectedPenColour:
            self.selectedPenColour = selectedPenColour
            if self.scene().selectedItems() != []:
                changePen = ChangePen(None, self.scene().selectedItems(), penColour=self.selectedPenColour)
                self.undoStack.push(changePen)

    def changePenStyleRoutine(self, selectedPenStyle):
        if selectedPenStyle != self.selectedPenStyle:
            self.selectedPenStyle = selectedPenStyle
            if self.scene().selectedItems() != []:
                changePen = ChangePen(None, self.scene().selectedItems(), penStyle=self.selectedPenStyle)
                self.undoStack.push(changePen)

    def changeBrushColourRoutine(self, selectedBrushColour):
        if selectedBrushColour != self.selectedBrushColour:
            self.selectedBrushColour = selectedBrushColour
            if self.scene().selectedItems() != []:
                changeBrush = ChangeBrush(None, self.scene().selectedItems(), brushColour=self.selectedBrushColour)
                self.undoStack.push(changeBrush)

    def changeBrushStyleRoutine(self, selectedBrushStyle):
        if selectedBrushStyle != self.selectedBrushStyle:
            self.selectedBrushStyle = selectedBrushStyle
            if self.scene().selectedItems() != []:
                changeBrush = ChangeBrush(None, self.scene().selectedItems(), brushStyle=self.selectedBrushStyle)
                self.undoStack.push(changeBrush)

    def mousePressEvent(self, event):
        self.currentPos = event.pos()
        self.currentX = self.currentPos.x()
        self.currentY = self.currentPos.y()
        # If copy mode is on
        if self._keys['c'] is True:
            # Check to make sure this is the first click
            if self._mouse['1'] is False:
                for i in self.scene().selectedItems():
                    i.createCopy()
                # Save a copy locally so that items don't disappear
                self.items = self.scene().items()
            # Start moving after creating copy
            self._keys['m'] = True
        # If move mode is on
        if self._keys['m'] is True:
            self.moveItems = self.scene().selectedItems()
            # On LMB
            if (event.button() == QtCore.Qt.LeftButton):
                # Toggle LMB if items have been selected
                if self.moveItems != []:
                    self._mouse['1'] = not self._mouse['1']
                else:
                    self._mouse['1'] = False
            # Begin moving if LMB is clicked
            if (self._mouse['1'] is True):
                # self.moveStartPos = self.mapToGrid(event.pos())
                self.moveStartPoint = self.mapToGrid(event.pos())
                for i in self.moveItems:
                    i.moveTo(self.moveStartPoint, 'start')
                # Create a macro and save all rotate/mirror commands
                self.undoStack.beginMacro('')
            # End moving if LMB is clicked again
            else:
                point = self.mapToGrid(event.pos())
                if self._keys['c'] is False:
                    move = Move(None, self.scene(), self.moveItems, startPoint=self.moveStartPoint, stopPoint=point)
                    self.undoStack.push(move)
                else:
                    copy_ = Copy(None, self.scene(), self.scene().selectedItems(), point=point)
                    self.undoStack.push(copy_)
                self.undoStack.endMacro()
        super(DrawingArea, self).mousePressEvent(event)

    def updateMoveItems(self):
        """Simple function that generates a list of selected items"""
        self.moveItems = self.scene().selectedItems()

    def rotateRoutine(self, modifier=None):
        """Handles rotation and reflection of selected items"""
        self.updateMoveItems()
        # If items have been selected
        if self.moveItems != []:
            if modifier is None:
                modifier = QtGui.QApplication.keyboardModifiers()
            # If reflect mode is on
            if modifier == QtCore.Qt.ShiftModifier:
                # Keep track of number of reflections
                self.reflections += 1
                self.reflections %= 2
                point = self.mapToGrid(self.currentPos)
                mirror = Mirror(None, self.scene(), self.moveItems, self._keys['m'], point)
                self.undoStack.push(mirror)
                # for item in self.moveItems:
                #     item.reflect(self._keys['m'], point)
            else:
                # Keep track of number of rotations
                self.rotations += 1
                self.rotations %= 360/self.rotateAngle
                point = self.mapToGrid(self.currentPos)
                rotate = Rotate(None, self.scene(), self.moveItems, self._keys['m'], point, self.rotateAngle)
                self.undoStack.push(rotate)
                # for item in self.moveItems:
                #     item.rotateBy(self._keys['m'], point, self.rotateAngle)

    def mouseReleaseEvent(self, event):
        super(DrawingArea, self).mouseReleaseEvent(event)
        # If wire or arc mode are on
        if self._keys['w'] is True or self._keys['arc'] is True:
            # Keep drawing new wire segments
            if (event.button() == QtCore.Qt.LeftButton):
                self._mouse['1'] = True
            if (self._mouse['1'] is True):
                self.oldPos = self.currentPos
                self.currentPos = event.pos()
                self.currentX = self.currentPos.x()
                self.currentY = self.currentPos.y()
                start = self.mapToGrid(self.currentPos)
                if self._keys['w'] is True:
                    # Create new wire if none exists
                    if self.currentWire is None:
                        self.currentWire = Wire(None, start, penColour=self.selectedPenColour, width=self.selectedWidth, penStyle=self.selectedPenStyle, brushColour=self.selectedBrushColour, brushStyle=self.selectedBrushStyle)
                        self.scene().addItem(self.currentWire)
                    # If wire exists, add segments
                    else:
                        edit = Edit(None, self.scene(), self.currentWire, start)
                        self.undoStack.push(edit)
                elif self._keys['arc'] is True:
                    # Create new arc if none exists
                    if self.currentArc is None:
                        self.currentArc = Arc(None, start, penColour=self.selectedPenColour, width=self.selectedWidth, penStyle=self.selectedPenStyle, brushColour=self.selectedBrushColour, brushStyle=self.selectedBrushStyle, points=self.arcPoints)
                        self.scene().addItem(self.currentArc)
                    # If arc exists, add segments
                    else:
                        edit = Edit(None, self.scene(), self.currentArc, start)
                        self.undoStack.push(edit)
            for item in self.scene().selectedItems():
                item.setSelected(False)
        # If rectangle mode is on, add a new rectangle
        if self._keys['rectangle'] is True:
            if event.button () == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.currentPos = event.pos()
                start = self.mapToGrid(self.currentPos)
                if self.currentRectangle is None:
                    self.currentRectangle = Rectangle(None, start=start, penColour=self.selectedPenColour, width=self.selectedWidth, penStyle=self.selectedPenStyle, brushColour=self.selectedBrushColour, brushStyle=self.selectedBrushStyle)
                    add = Add(None, self.scene(), self.currentRectangle)
                    self.undoStack.push(add)
                    # self.scene().addItem(self.currentRectangle)
            for item in self.scene().selectedItems():
                item.setSelected(False)
        # If circle mode is on, add a new circle
        if self._keys['circle'] is True:
            if event.button () == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.currentPos = event.pos()
                start = self.mapToGrid(self.currentPos)
                if self.currentCircle is None:
                    self.currentCircle = Circle(None, start=start, penColour=self.selectedPenColour, width=self.selectedWidth, penStyle=self.selectedPenStyle, brushColour=self.selectedBrushColour, brushStyle=self.selectedBrushStyle)
                    add = Add(None, self.scene(), self.currentCircle)
                    self.undoStack.push(add)
                    # self.scene().addItem(self.currentCircle)
            for item in self.scene().selectedItems():
                item.setSelected(False)
        # If ellipse mode is on, add a new ellipse
        if self._keys['ellipse'] is True:
            if event.button () == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.currentPos = event.pos()
                start = self.mapToGrid(self.currentPos)
                if self.currentEllipse is None:
                    self.currentEllipse = Ellipse(None, start=start, penColour=self.selectedPenColour, width=self.selectedWidth, penStyle=self.selectedPenStyle, brushColour=self.selectedBrushColour, brushStyle=self.selectedBrushStyle)
                    add = Add(None, self.scene(), self.currentEllipse)
                    self.undoStack.push(add)
                    # self.scene().addItem(self.currentEllipse)
            for item in self.scene().selectedItems():
                item.setSelected(False)
        # If textbox mode is on, add a new textbox
        if self._keys['textBox'] is True:
            if event.button () == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.currentPos = event.pos()
                start = self.mapToGrid(self.currentPos)
                if self.currentTextBox is None:
                    self.currentTextBox = TextBox(None, start=start, penColour=self.selectedPenColour, width=self.selectedWidth, penStyle=self.selectedPenStyle, brushColour=self.selectedBrushColour, brushStyle=self.selectedBrushStyle)
                    add = Add(None, self.scene(), self.currentTextBox)
                    self.undoStack.push(add)
                    # self.scene().addItem(self.currentTextBox)
                self._keys['textBox'] = False
                # Change cursor shape to a text editing style
                cursor = self.cursor()
                cursor.setShape(QtCore.Qt.ArrowCursor)
                self.setCursor(cursor)
            for item in self.scene().selectedItems():
                item.setSelected(False)

    def mouseMoveEvent(self, event):
        super(DrawingArea, self).mouseMoveEvent(event)
        self.currentPos = event.pos()
        if (self._mouse['1'] is True):
            self.oldX = self.currentX
            self.oldY = self.currentY
            self.currentX = self.currentPos.x()
            self.currentY = self.currentPos.y()
            modifiers = QtGui.QApplication.keyboardModifiers()
            if modifiers != QtCore.Qt.ControlModifier:
                if self._keys['w'] is True:
                    self.currentWire.updateWire(self.mapToGrid(event.pos()))
                if self._keys['arc'] is True:
                    self.currentArc.updateArc(self.mapToGrid(event.pos()))
                if self._keys['rectangle'] is True:
                    self.currentRectangle.updateRectangle(self.mapToGrid(event.pos()))
                if self._keys['circle'] is True:
                    self.currentCircle.updateCircle(self.mapToGrid(event.pos()))
                if self._keys['ellipse'] is True:
                    self.currentEllipse.updateEllipse(self.mapToGrid(event.pos()))
                if self._keys['m'] is True:
                    point = self.mapToGrid(event.pos())
                    for item in self.moveItems:
                        item.moveTo(point, 'move')

    def contextMenuEvent(self, event):
        # TODO: Make this work properly
        menu = QtGui.QMenu()
        actionDelete = menu.addAction('&Delete')
        actionDelete.triggered.connect(lambda: self.scene().removeItem(self))
        menu.exec_(event.screenPos())

    def mapToGrid(self, point):
        # Convenience function to map given point on to the grid
        point = self.mapToScene(point)
        if self.snapToGrid is True:
            return self._grid.snapTo(point)
        else:
            return point

    def wheelEvent(self, event):
        # Pan or zoom depending on keyboard modifiers
        scaleFactor = -event.delta() / 240.
        modifiers = QtGui.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            self.translate(0, -scaleFactor * 20)
        elif modifiers == QtCore.Qt.ShiftModifier:
            self.translate(-scaleFactor * 20, 0)
        else:
            if scaleFactor < 0:
                scaleFactor = -1 / scaleFactor
            scaleFactor = 1 + (scaleFactor - 1) / 5.
            oldPos = self.mapToScene(event.pos())
            self.scale(scaleFactor, scaleFactor)
            self._grid.createGrid()
            newPos = self.mapToScene(event.pos())
            delta = newPos - oldPos
            self.translate(delta.x(), delta.y())
