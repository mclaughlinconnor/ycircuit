# Missing SVG import
from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport, QtSvg
from src.commands import *
from src.components import *
from src.drawingitems import *
import pickle
import os
from numpy import ceil, floor
# from src import components
# import sys
# sys.modules['components'] = components


class DrawingArea(QtWidgets.QGraphicsView):
    """The drawing area is subclassed from QGraphicsView to provide additional
    functionality specific to this schematic drawing tool. Further information about
    these modifications is present in the method docstrings.
    """

    statusbarMessage = QtCore.pyqtSignal(str, int)
    resetToolbarButtons = QtCore.pyqtSignal()

    def __init__(self, parent=None):
        """Initializes the object and various parameters to default values"""
        super().__init__(parent)
        self.setScene(QtWidgets.QGraphicsScene(self))
        # The default BSP tree index method could lead to segfaults
        # If that happens, uncomment the line below
        # self.scene().setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        self.scene().setSceneRect(QtCore.QRectF(-10000, -10000, 20000, 20000))
        self.parent = parent
        self._keys = {'c': False, 'm': False, 'r': False, 'w': False,
                      'arc': False, 'rectangle': False, 'circle': False,
                      'ellipse': False, 'textBox': False, 'add': False,
                      'edit': False, 'net': False}
        self._mouse = {'1': False}
        self._grid = Grid(None, self, 10)
        self._grid.createGrid()
        self.enableGrid = True
        self.snapToGrid = True
        self.undoStack = QtWidgets.QUndoStack(self)
        self.undoStack.setUndoLimit(1000)
        self.reflections = 0
        self.rotations = 0
        self.rotateAngle = 45
        self.selectedWidth = 4
        self.selectedPenColour = 'black'
        self.selectedPenStyle = 1
        self.selectedBrushColour = 'black'
        self.selectedBrushStyle = 0
        self.items = []
        self.moveItems = []
        self.schematicFileName = None
        self.symbolFileName = None
        self.selectOrigin = False
        self.currentPos = QtCore.QPoint(0, 0)
        # Fit to view when scroll bars are changed, e.g. when program starts, window is resized
        # self.horizontalScrollBar().valueChanged.connect(self.fitToViewRoutine)
        # self.verticalScrollBar().valueChanged.connect(self.fitToViewRoutine)

    def keyReleaseEvent(self, event):
        """Run escapeRoutine when the escape button is pressed"""
        super().keyReleaseEvent(event)
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
        """Set _key to rectangle mode so that a rectangle is added when LMB is pressed"""
        self.escapeRoutine()
        self._keys['rectangle'] = True
        self.currentRectangle = None

    def addCircle(self):
        """Set _key to circle mode so that a circle is added when LMB is pressed"""
        self.escapeRoutine()
        self._keys['circle'] = True
        self.currentCircle = None

    def addEllipse(self):
        """Set _key to ellipse mode so that an ellipse is added when LMB is pressed"""
        self.escapeRoutine()
        self._keys['ellipse'] = True
        self.currentEllipse = None

    def addTextBox(self):
        """Set _key to textBox mode so that a textbox is added when LMB is pressed"""
        self.escapeRoutine()
        cursor = self.cursor()
        cursor.setShape(QtCore.Qt.IBeamCursor)
        self.setCursor(cursor)
        self._keys['textBox'] = True
        self.currentTextBox = None

    def addNet(self):
        """Set _key to net mode so that a net is added when LMB is pressed"""
        self.escapeRoutine()
        self._keys['net'] = True
        self.currentNet = None

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
        # Return if no items are present
        if len(self.scene().items()) == 0:
            return
        if mode in possibleModes:
            listOfItems = self.scene().items()
            listOfItems = [item for item in listOfItems if item.parentItem() is None]
            x = min([item.scenePos().x() for item in listOfItems])
            y = min([item.scenePos().y() for item in listOfItems])
            origin = QtCore.QPointF(x, y)
            # Override origin if it is to be saved as a symbol
            if mode == 'symbol' or mode == 'symbolAs':
                self.selectOrigin = True
                for item in listOfItems:
                    item.setAcceptedMouseButtons(QtCore.Qt.NoButton)
                    item.setAcceptHoverEvents(False)
                    item.setSelected(False)
                self.statusbarMessage.emit("Pick an origin for the symbol (press ESC to cancel)", 0)
                while self.selectOrigin is True:
                    QtCore.QCoreApplication.processEvents()
                origin = self.mapToGrid(self.currentPos)
                self.statusbarMessage.emit("", 0)
                for item in listOfItems:
                    item.setAcceptedMouseButtons(QtCore.Qt.AllButtons)
                    item.setAcceptHoverEvents(True)
                    item.setSelected(False)
                # Pressing escape sets selectOrigin to None
                if self.selectOrigin is None:
                    return

            saveObject = myGraphicsItemGroup(None, origin, [])
            self.scene().addItem(saveObject)
            saveObject.origin = origin

            # Set relative origins of child items
            for item in listOfItems:
                item.origin = item.pos() - saveObject.origin
                # print item, item.origin
            saveObject.setItems(listOfItems)

            saveFile = ''
            if mode == 'symbol':
                if self.symbolFileName is None:
                    fileDialog = myFileDialog(self, 'Save symbol', './Resources/Symbols/Custom/untitled.sym', filt='Symbols (*.sym)', mode='save')
                    if (fileDialog.exec_()):
                        saveFile = str(fileDialog.selectedFiles()[0])
                else:
                    saveFile = self.symbolFileName
            elif mode == 'symbolAs':
                fileDialog = myFileDialog(self, 'Save symbol as', './Resources/Symbols/Custom/untitled.sym', filt='Symbols (*.sym)', mode='save')
                if (fileDialog.exec_()):
                    saveFile = str(fileDialog.selectedFiles()[0])
            elif mode == 'schematic':
                if self.schematicFileName is None:
                    fileDialog = myFileDialog(self, 'Save schematic', './untitled.sch', filt='Schematics (*.sch)', mode='save')
                    if (fileDialog.exec_()):
                        saveFile = str(fileDialog.selectedFiles()[0])
                else:
                    saveFile = self.schematicFileName
            elif mode == 'schematicAs':
                fileDialog = myFileDialog(self, 'Save schematic as', './untitled.sch', filt='Schematics (*.sch)', mode='save')
                if (fileDialog.exec_()):
                    saveFile = str(fileDialog.selectedFiles()[0])

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

    def exportRoutine(self):
        """
        For images, a rect slightly larger than the bounding rect of all items is
        created. This rect is then projected onto a QPixmap at a higher resolution to
        create the final image.
        """
        # Remove grid from the scene to avoid saving it
        self._grid.removeGrid()
        # Return if no items are present
        if len(self.scene().items()) == 0:
            self._grid.createGrid()
            return
        # Deselect items before exporting
        selectedItems = self.scene().selectedItems()
        for item in selectedItems:
            item.setSelected(False)
        saveFile = str(QtWidgets.QFileDialog.getSaveFileName(self, 'Export File', './untitled.pdf', 'PDF files (*.pdf);;SVG files(*.svg);;PNG Files (*.png);;JPG files (*.jpg *.jpeg);;BMP files (*.bmp);;TIFF files (*.tiff)')[0])
        # Check that file is valid
        if saveFile == '':
            # Add the grid back to the scene
            self._grid.createGrid()
            return
        if saveFile[-3:] in ['pdf']:
            mode = 'pdf'
        elif saveFile[-3:] == 'svg':
            mode = 'svg'
        elif saveFile[-3:] in ['jpg', 'png', 'bmp']:
            mode = 'image'
            extension = saveFile[-3:]
            if extension == 'jpg':
                quality = 90
            elif extension == 'png':
                quality = 50
            elif extension == 'bmp':
                quality = 1
        elif saveFile[-4:] in ['jpeg', 'tiff']:
            mode = 'image'
            extension = saveFile[-4:]
            if extension == 'jpeg':
                quality = 90
            elif extension == 'tiff':
                quality = 1
        if mode == 'pdf':
            # Initialize printer
            printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
            sourceRect = self.scene().itemsBoundingRect()
            # Choose appropriate format
            if saveFile[-3:] == 'pdf':
                printer.setOutputFormat(printer.PdfFormat)
            printer.setOutputFileName(saveFile)
            pageSize = QtGui.QPageSize(sourceRect.size().toSize(), matchPolicy=QtGui.QPageSize.ExactMatch)
            printer.setPageSize(pageSize)
            painter = QtGui.QPainter(printer)
            self.scene().render(painter, source=sourceRect)
        elif mode == 'svg':
            svgGenerator = QtSvg.QSvgGenerator()
            svgGenerator.setFileName(saveFile)
            sourceRect = self.scene().itemsBoundingRect()
            width, height = sourceRect.width(), sourceRect.height()
            svgGenerator.setSize(QtCore.QSize(width, height))
            svgGenerator.setResolution(96)
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
            # Create an image object
            img = QtGui.QImage(QtCore.QSize(2*width, 2*height), QtGui.QImage.Format_RGB32)
            # Set background to white
            img.fill(QtGui.QColor('white'))
            painter = QtGui.QPainter(img)
            painter.setRenderHint(painter.SmoothPixmapTransform, True)
            painter.setRenderHint(painter.Antialiasing, True)
            painter.setRenderHint(painter.TextAntialiasing, True)
            targetRect = QtCore.QRectF(img.rect())
            self.scene().render(painter, targetRect, sourceRect)
            img.save(saveFile, extension, quality=quality)

        # Need to stop painting to avoid errors about painter getting deleted
        painter.end()
        # Add the grid back to the scene when saving is done
        self._grid.createGrid()
        # Reselect items after exporting is completed
        for item in selectedItems:
            item.setSelected(True)

    def loadRoutine(self, mode='symbol', loadFile=None):
        """This is the counterpart of the save routine. Used to load both schematics
        and symbols.
        """
        possibleModes = ['schematic', 'symbol', 'symbolModify']
        if mode in possibleModes:
            if loadFile is None:
                loadFile = ''
                if mode == 'symbol' or mode == 'symbolModify':
                    fileDialog = myFileDialog(self, 'Load Symbol', './Resources/Symbols/', filt='Symbols (*.sym)', mode='load')
                elif mode == 'schematic':
                    fileDialog = myFileDialog(self, 'Load Schematic', './', filt='Schematics (*.sch)', mode='load')
                if (fileDialog.exec_()):
                    loadFile = str(fileDialog.selectedFiles()[0])
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
                    self._grid.removeGrid()
                self.scene().clear()
                self._grid.createGrid()
                loadItem.__init__(None, QtCore.QPointF(0, 0), loadItem.listOfItems, mode='symbol')
                self.scene().addItem(loadItem)
                # loadItem.loadItems(mode)
            elif mode == 'symbol':
                self.loadItem = loadItem
                loadItem.__init__(None, self.mapToGrid(self.currentPos), loadItem.listOfItems, mode='symbol')
                self.scene().addItem(self.loadItem)
                # loadItem.loadItems('symbol')
            if mode == 'schematic' or mode == 'symbolModify':
                loadItem.setPos(loadItem.origin)
                loadItem.reparentItems()
                self.scene().removeItem(loadItem)
                self.fitToViewRoutine()
                self.undoStack.clear()
            elif mode == 'symbol':
                # Symbols are created with the pen/brush that they were saved in
                # loadItem.setPos(self.mapToGrid(self.currentPos))
                for item in self.scene().selectedItems():
                    item.setSelected(False)
                loadItem.setSelected(True)
                self.currentX = self.currentPos.x()
                self.currentY = self.currentPos.y()
                self.moveStartPoint = self.mapToGrid(self.currentPos)
                self._keys['add'], self._mouse['1'] = True, True
                loadItem.moveTo(self.moveStartPoint, 'start')
                self.updateMoveItems()
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
                # The failed move command still exists in the stack. Not sure how to remove it
                self.undoStack.undo()
                self.resetToolbarButtons.emit()
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
                self.resetToolbarButtons.emit()
            # Remove last wire being drawn
            if self._keys['w'] is True:
                # self.scene().removeItem(self.currentWire)
                self.currentWire.cancelSegment()
            if self._keys['net'] is True:
                self.currentNet.cancelSegment()
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
        if self._keys['add'] is True:
            for item in self.scene().selectedItems():
                self.scene().removeItem(item)
        if self._keys['edit'] is True:
            self.undoStack.endMacro()
            self.undoStack.undo()
        # Cancel symbol save
        if self.selectOrigin is True:
            self.selectOrigin = None
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
        # Clear the statusbar
        self.statusbarMessage.emit("", 0)

    def moveRoutine(self):
        """Preps to begin moving items"""
        self.escapeRoutine()
        self.updateMoveItems()
        self._keys['m'] = True
        self.statusbarMessage.emit("Move (Press ESC to cancel)", 0)

    def copyRoutine(self):
        """Preps to begin copying items"""
        self.escapeRoutine()
        self._keys['c'] = True
        self.statusbarMessage.emit("Copy (Press ESC to cancel)", 0)

    def deleteRoutine(self):
        """Delete selected items"""
        self.undoStack.beginMacro('')
        for item2 in self.scene().selectedItems():
            if isinstance(item2, Net):
                netList = [item for item in self.scene().items() if (isinstance(item, Net) and item.collidesWithItem(item2))]
                if item2 in netList:
                    netList.remove(item2)
                for item in netList:
                    mergedNet = item.mergeNets(netList, self.undoStack)
                    if mergedNet is not None:
                        mergedNet.splitNets(netList, self.undoStack)
        del1 = Delete(None, self.scene(), self.scene().selectedItems())
        self.undoStack.push(del1)
        self.undoStack.endMacro()
        self.statusbarMessage.emit("Delete", 1000)

    def fitToViewRoutine(self):
        """Resizes viewport so that all items drawn are visible"""
        if len(self.scene().items()) == 1:
            # Fit to (0, 0, 800, 800) if nothing is present
            rect = QtCore.QRectF(0, 0, 800, 800)
            self.fitInView(rect, QtCore.Qt.KeepAspectRatio)
        else:
            self.fitInView(self.scene().itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

    def toggleGridRoutine(self):
        """Toggles grid on and off"""
        self.enableGrid = not self.enableGrid
        if self.enableGrid is True:
            self._grid.createGrid()
        else:
            self.setBackgroundBrush(QtGui.QBrush())

    def toggleSnapToGridRoutine(self, state):
        """Toggles drawings snapping to grid"""
        self.snapToGrid = state

    def changeWidthRoutine(self, selectedWidth):
        if selectedWidth != self.selectedWidth:
            self.selectedWidth = selectedWidth
            if self.scene().selectedItems() != []:
                changePen = ChangePen(None, self.scene().selectedItems(), width=self.selectedWidth)
                self.undoStack.push(changePen)
        self.statusbarMessage.emit("Changed pen width to %d" %(self.selectedWidth), 1000)

    def changePenColourRoutine(self, selectedPenColour):
        if selectedPenColour != self.selectedPenColour:
            self.selectedPenColour = selectedPenColour
            if self.scene().selectedItems() != []:
                changePen = ChangePen(None, self.scene().selectedItems(), penColour=self.selectedPenColour)
                self.undoStack.push(changePen)
        self.statusbarMessage.emit("Changed pen colour to %s" %(self.selectedPenColour), 1000)

    def changePenStyleRoutine(self, selectedPenStyle):
        if selectedPenStyle != self.selectedPenStyle:
            self.selectedPenStyle = selectedPenStyle
            if self.scene().selectedItems() != []:
                changePen = ChangePen(None, self.scene().selectedItems(), penStyle=self.selectedPenStyle)
                self.undoStack.push(changePen)
        self.statusbarMessage.emit("Changed pen style to %s" %(self.selectedPenStyle), 1000)

    def changeBrushColourRoutine(self, selectedBrushColour):
        if selectedBrushColour != self.selectedBrushColour:
            self.selectedBrushColour = selectedBrushColour
            if self.scene().selectedItems() != []:
                changeBrush = ChangeBrush(None, self.scene().selectedItems(), brushColour=self.selectedBrushColour)
                self.undoStack.push(changeBrush)
        self.statusbarMessage.emit("Changed brush colour to %s" %(self.selectedBrushColour), 1000)

    def changeBrushStyleRoutine(self, selectedBrushStyle):
        if selectedBrushStyle != self.selectedBrushStyle:
            self.selectedBrushStyle = selectedBrushStyle
            if self.scene().selectedItems() != []:
                changeBrush = ChangeBrush(None, self.scene().selectedItems(), brushStyle=self.selectedBrushStyle)
                self.undoStack.push(changeBrush)
        self.statusbarMessage.emit("Changed brush style to %s" %(self.selectedBrushStyle), 1000)

    def mousePressEvent(self, event):
        self.currentPos = event.pos()
        self.currentX = self.currentPos.x()
        self.currentY = self.currentPos.y()
        # If copy mode is on
        if self._keys['c'] is True:
            # Check to make sure this is the first click
            if self._mouse['1'] is False:
                for item in self.scene().selectedItems():
                    item.createCopy()
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
                self.moveStartPoint = self.mapToGrid(event.pos())
                for i in self.moveItems:
                    i.moveTo(self.moveStartPoint, 'start')
                # Create a macro and save all rotate/mirror commands
                self.undoStack.beginMacro('')
                # Evaluate if any new nets need to be split/merged
                # Only do this check if moving and *not* for copying
                if self._keys['c'] is False:
                    for item2 in self.moveItems:
                        if isinstance(item2, Net):
                            netList = [item for item in self.scene().items() if (isinstance(item, Net) and item.collidesWithItem(item2))]
                            if item2 in netList:
                                netList.remove(item2)
                            for item in netList:
                                mergedNet = item.mergeNets(netList, self.undoStack)
                                if mergedNet is not None:
                                    mergedNet.splitNets(netList, self.undoStack)
            # End moving if LMB is clicked again and selection is not empty
            elif self.moveItems != []:
                point = self.mapToGrid(event.pos())
                if self._keys['c'] is True:
                    copy_ = Copy(None, self.scene(), self.moveItems, point=point)
                    self.undoStack.push(copy_)
                else:
                    # Cancel the move and add the move to undo stack properly
                    for item in self.moveItems:
                        item.moveTo(None, 'cancel')
                    move = Move(None, self.scene(), self.moveItems, startPoint=self.moveStartPoint, stopPoint=point)
                    self.undoStack.push(move)
                # Evaluate if any new nets need to be split/merged
                # if self._keys['c'] is False:
                if True:
                    for item2 in self.moveItems:
                        if isinstance(item2, Net):
                            netList = [item for item in self.scene().items() if (isinstance(item, Net) and item.collidesWithItem(item2))]
                            mergedNet = item2.mergeNets(netList, self.undoStack)
                            if mergedNet is not None:
                                mergedNet.splitNets(netList, self.undoStack)
                            elif item2.scene() is not None:
                                item2.splitNets(netList, self.undoStack)
                # End move command once item has been placed
                self._keys['m'] = False
                self._keys['c'] = False
                self.statusbarMessage.emit("", 0)
                self.undoStack.endMacro()
                self.resetToolbarButtons.emit()
                for item in self.moveItems:
                    item.setSelected(False)
        if self._keys['add'] is True:
            if (event.button() == QtCore.Qt.LeftButton):
                # add = Add(None, self.scene(), self.loadItem, symbol=True, origin=self.mapToGrid(event.pos()), rotateAngle=self.rotations*self.rotateAngle, reflect=self.reflections)
                add = Add(None, self.scene(), self.loadItem, symbol=True, origin=self.mapToGrid(event.pos()), transform=self.loadItem.transform())
                self.undoStack.push(add)
        if self._keys['edit'] is True:
            self._keys['edit'] = False
            if (event.button() == QtCore.Qt.LeftButton):
                self._mouse['1'] = False
                edit = Edit(None, self.scene(), self.scene().selectedItems()[0], self.mapToGrid(event.pos()))
                self.undoStack.push(edit)
                self.undoStack.endMacro()
        # Only propagate these events downwards if move and copy are disabled or if nothing is selected or if a symbol is not being added
        if self.moveItems == []:
            super().mousePressEvent(event)
        elif self._keys['c'] is False and self._keys['m'] is False and self._keys['add'] is False:
            super().mousePressEvent(event)

    def updateMoveItems(self):
        """Simple function that generates a list of selected items"""
        self.moveItems = self.scene().selectedItems()

    def rotateRoutine(self, modifier=None):
        """Handles rotation and reflection of selected items"""
        self.updateMoveItems()
        # If items have been selected
        if self.moveItems != []:
            if modifier is None:
                modifier = QtWidgets.QApplication.keyboardModifiers()
            # If reflect mode is on
            if modifier == QtCore.Qt.ShiftModifier:
                # Keep track of number of reflections
                self.reflections += 1
                self.reflections %= 2
                point = self.mapToGrid(self.currentPos)
                mirror = Mirror(None, self.scene(), self.moveItems, self._keys['m'] and self._mouse['1'], point)
                # If a new item is being added, don't push mirror onto the undo stack
                if self._keys['add'] is False:
                    self.undoStack.push(mirror)
                else:
                    mirror.redo()
                self.statusbarMessage.emit("Mirrored item(s)", 1000)
                # for item in self.moveItems:
                #     item.reflect(self._keys['m'], point)
            else:
                # Keep track of number of rotations
                self.rotations += 1
                self.rotations %= 360/self.rotateAngle
                point = self.mapToGrid(self.currentPos)
                rotate = Rotate(None, self.scene(), self.moveItems, self._keys['m'] and self._mouse['1'], point, self.rotateAngle)
                # If a new item is being added, don't push rotate onto the undo stack
                if self._keys['add'] is False:
                    self.undoStack.push(rotate)
                else:
                    rotate.redo()
                self.statusbarMessage.emit("Rotated item(s) by %d degrees" %(self.rotateAngle), 1000)
                # for item in self.moveItems:
                #     item.rotateBy(self._keys['m'], point, self.rotateAngle)

    def mouseReleaseEvent(self, event):
        # Only propagate these events downwards if move and copy are disabled or if nothing is selected or if a symbol is not being added
        if self.moveItems == []:
            super().mouseReleaseEvent(event)
        elif self._keys['c'] is False and self._keys['m'] is False and self._keys['add'] is False:
            super().mouseReleaseEvent(event)
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
        if self._keys['net'] is True:
            if event.button () == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.currentPos = event.pos()
                start = self.mapToGrid(self.currentPos)
                # Create new net if none exists
                if self.currentNet is None:
                    self.currentNet = Net(None, start, penColour=self.selectedPenColour, width=self.selectedWidth, penStyle=self.selectedPenStyle, brushColour=self.selectedBrushColour, brushStyle=self.selectedBrushStyle)
                    # Add the original net
                    self.scene().addItem(self.currentNet)
            else:
                if self.currentNet is not None:
                    netList = [item for item in self.scene().items() if (isinstance(item, Net) and item.collidesWithItem(self.currentNet))]
                    netList.remove(self.currentNet)
                    self.scene().removeItem(self.currentNet)
                    self.undoStack.beginMacro('')
                    add = Add(None, self.scene(), self.currentNet)
                    self.undoStack.push(add)
                    mergedNet = self.currentNet.mergeNets(netList, self.undoStack)
                    self.currentNet.splitNets(netList, self.undoStack)
                    # Add the perpendicular line properly, if it exists
                    if self.currentNet.perpLine is not None:
                        netList = [item for item in self.scene().items() if (isinstance(item, Net) and item.collidesWithItem(self.currentNet.perpLine))]
                        netList.remove(self.currentNet.perpLine)
                        perpLineObscured = False
                        for net in netList:
                            p1 = self.currentNet.perpLine.mapToItem(net, self.currentNet.perpLine.line().p1())
                            p2 = self.currentNet.perpLine.mapToItem(net, self.currentNet.perpLine.line().p2())
                            if (net.contains(p1) and net.contains(p2)) and net != self.currentNet.perpLine:
                                perpLineObscured = True
                        self.scene().removeItem(self.currentNet.perpLine)
                        if perpLineObscured is False:
                            self.undoStack.endMacro()
                            self.undoStack.beginMacro('')
                            add = Add(None, self.scene(), self.currentNet.perpLine)
                            self.undoStack.push(add)
                            mergedNet = self.currentNet.perpLine.mergeNets(netList, self.undoStack)
                            self.currentNet.perpLine.splitNets(netList, self.undoStack)
                    self.undoStack.endMacro()
                    self.currentNet = None
            if event.button() == QtCore.Qt.RightButton:
                self.currentNet.changeRightAngleMode(self.mapToGrid(event.pos()))
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
        if self.selectOrigin is True:
            if event.button() == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.currentPos = event.pos()
                self.selectOrigin = False

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.currentPos = event.pos()
        if (self._mouse['1'] is True):
            self.oldX = self.currentX
            self.oldY = self.currentY
            self.currentX = self.currentPos.x()
            self.currentY = self.currentPos.y()
            modifiers = QtWidgets.QApplication.keyboardModifiers()
            if modifiers != QtCore.Qt.ControlModifier:
                if self._keys['w'] is True:
                    self.currentWire.updateWire(self.mapToGrid(event.pos()))
                if self._keys['net'] is True:
                    self.currentNet.updateNet(self.mapToGrid(event.pos()))
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
                if self._keys['add'] is True:
                    point = self.mapToGrid(event.pos())
                    for item in self.moveItems:
                        item.moveTo(point, 'move')
                if self._keys['edit'] is True:
                    item = self.scene().selectedItems()[0]
                    point = self.mapToGrid(event.pos())
                    if isinstance(item, Rectangle):
                        item.updateRectangle(point, edit=True)
                    elif isinstance(item, Circle):
                        item.updateCircle(point)

    # def contextMenuEvent(self, event):
    #     # TODO: Make this work properly
    #     menu = QtGui.QMenu()
    #     actionDelete = menu.addAction('&Delete')
    #     actionDelete.triggered.connect(lambda: self.scene().removeItem(self))
    #     menu.exec_(event.screenPos())

    def mapToGrid(self, point):
        # Convenience function to map given point on to the grid
        point = self.mapToScene(point)
        if self.snapToGrid is True:
            return self._grid.snapTo(point)
        else:
            return point

    def wheelEvent(self, event):
        # Pan or zoom depending on keyboard modifiers
        eventDelta = event.angleDelta().y()
        if eventDelta >= 0:
            delta = max(120, eventDelta)
        elif eventDelta < 0:
            delta = min(-120, eventDelta)
        scaleFactor = -delta / 240.
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        if modifiers == QtCore.Qt.ControlModifier:
            self.translate(0, -scaleFactor * 100)
        elif modifiers == QtCore.Qt.ShiftModifier:
            self.translate(-scaleFactor * 100, 0)
        else:
            if scaleFactor < 0:
                scaleFactor = -1 / scaleFactor
            scaleFactor = 1 + (scaleFactor - 1) / 5.
            oldPos = self.mapToScene(event.pos())
            self.scale(scaleFactor, scaleFactor)
            newPos = self.mapToScene(event.pos())
            delta = newPos - oldPos
            self.translate(delta.x(), delta.y())

    def editShape(self):
        if len(self.scene().selectedItems()) == 1:
            item = self.scene().selectedItems()[0]
            cursor = self.cursor()
            if isinstance(item, Rectangle):
                sceneP = item.mapToScene(item.p2).toPoint()
            elif isinstance(item, Circle):
                sceneP = item.end.toPoint()
            viewP = self.mapFromScene(sceneP)
            cursor.setPos(self.viewport().mapToGlobal(viewP))
            self.editStartPoint = sceneP
            self._keys['edit'], self._mouse['1'] = True, True
            self.undoStack.beginMacro('')
            edit = Edit(None, self.scene(), item, self.editStartPoint)
            self.undoStack.push(edit)
        else:
            self.statusbarMessage.emit("Please select an item to edit", 1000)
