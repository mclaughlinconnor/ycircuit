from PyQt5 import QtCore, QtGui, QtWidgets, QtPrintSupport, QtSvg
from src.commands import *
from src.components import *
from src.drawingitems import *
from .optionswindow import MyOptionsWindow
import pickle
import os
import glob
import logging

logger = logging.getLogger('YCircuit.drawingarea')

# from src import components
# import sys
# sys.modules['components'] = components


class DrawingArea(QtWidgets.QGraphicsView):
    """The drawing area is subclassed from QGraphicsView to provide additional
    functionality specific to this schematic drawing tool. Further information about
    these modifications is present in the method docstrings.
    """

    statusbarMessage = QtCore.pyqtSignal(str, int)

    def __init__(self, parent=None):
        """Initializes the object and various parameters to default values"""
        super().__init__(parent)
        self.setScene(QtWidgets.QGraphicsScene(self))
        # The default BSP tree index method could lead to segfaults
        # If that happens, uncomment the line below
        # self.scene().setItemIndexMethod(QtWidgets.QGraphicsScene.NoIndex)
        self.scene().setSceneRect(QtCore.QRectF(-10000, -10000, 20000, 20000))
        self.parent = parent
        self._keys = {
            'c': False,
            'm': False,
            'r': False,
            'v': False,
            'w': False,
            'arc': False,
            'rectangle': False,
            'circle': False,
            'ellipse': False,
            'image': False,
            'textBox': False,
            'add': False,
            'edit': False,
            'net': False
        }
        self._mouse = {'1': False}
        self._grid = Grid(None, self)
        self.showPins = True
        self.undoStack = QtWidgets.QUndoStack(self)
        self.undoStack.setUndoLimit(1000)
        self.reflections = 0
        self.rotations = 0
        self.rotateAngle = 45
        self.defaultSchematicSaveFolder = './'
        self.defaultSymbolSaveFolder = 'Resources/Symbols/Custom/'
        self.defaultExportFolder = './'
        self.dragMove = False

        # Set up the autobackup timer
        self.autobackupTimer = QtCore.QTimer()
        self.autobackupTimer.setInterval(10000)
        self.autobackupTimer.timeout.connect(self.autobackupRoutine)

        self.settingsFileName = '.config'

        self.mouseRect = QtWidgets.QGraphicsRectItem(QtCore.QRectF(-4, -4, 8, 8))
        self.mouseRect.setPen(QtGui.QPen(QtGui.QColor('darkGray')))
        self.mouseRect.setTransform(QtGui.QTransform().rotate(45))
        self.mouseRect.setZValue(1000)
        self.showMouseRect = True # Required for autobackup load routine below
        self.autobackupEnable = True # Required for autobackup load routine below

        self.items = []
        self.moveItems = []
        self.schematicFileName = None
        self.symbolFileName = None
        self.selectOrigin = False
        self.currentPos = QtCore.QPoint(0, 0)

        # Check to see if a default autobackup file already exists
        autobackupFileNameTemplate = 'autobackup.sch'
        loadFile = autobackupFileNameTemplate
        if glob.glob(autobackupFileNameTemplate + '*') != []:
            loadFile = self.loadAutobackupRoutine(autobackupFileNameTemplate)
        if loadFile != autobackupFileNameTemplate:
            self.loadRoutine(mode='schematic', loadFile=loadFile)
            self.schematicFileName = None
            # Push a dummy undo command so that the user is prompted to save
            self.undoStack.push(QtWidgets.QUndoCommand(None))
        else:
            # If backup existed, delete it
            if glob.glob(autobackupFileNameTemplate + '*') != []:
                os.remove(glob.glob(autobackupFileNameTemplate + '*')[0])
            # Must setup the file only after checking if one already exists
            self.autobackupFile = QtCore.QTemporaryFile(autobackupFileNameTemplate)
            self.autobackupFile.open()
            self.autobackupFile.setAutoRemove(False)
            logger.info('Creating autobackup file %s', self.autobackupFile.fileName())
        self.autobackupTimer.start()

    def applySettingsFromFile(self, fileName=None):
        """When provided with an appropriate settings filename, this method
        opens it for reading and extracts various parameters and sets them."""
        # Load settings file
        settings = QtCore.QSettings(fileName, QtCore.QSettings.IniFormat)
        logger.info('Applying settings from file %s', fileName)

        # Font settings
        fontFamily = settings.value('Painting/Font/Family', 'Arial')
        fontPointSize = settings.value('Painting/Font/Point size', '10', type=int)
        self.selectedFont = QtGui.QFont()
        self.selectedFont.setFamily(fontFamily)
        self.selectedFont.setPointSize(fontPointSize)
        self.useEulerFontForLatex = settings.value('Painting/Font/Use Euler font for LaTeX', True, type=bool)
        # Painting settings
        self.selectedWidth = settings.value('Painting/Pen/Width', '4', type=int)
        self.selectedPenColour = settings.value('Painting/Pen/Colour', 'Black')
        penStyles = {'Solid': 1, 'Dash': 2, 'Dot': 3, 'Dash-dot': 4, 'Dash-dot-dot': 5}
        self.selectedPenStyle = penStyles[settings.value('Painting/Pen/Style', 'Solid')]
        self.selectedBrushColour = settings.value('Painting/Brush/Colour', 'Black')
        brushStyles = {'No fill': 0, 'Solid': 1}
        self.selectedBrushStyle = brushStyles[settings.value('Painting/Brush/Style', 'No fill')]
        penCapStyles = {'Square': 0x10, 'Round': 0x20, 'Flat': 0x00}
        self.selectedPenCapStyle = penCapStyles[settings.value('Painting/Pen/Cap Style', 'Square')]
        penJoinStyles = {'Round': 0x80, 'Miter': 0x00, 'Bevel': 0x40}
        self.selectedPenJoinStyle = penJoinStyles[settings.value('Painting/Pen/Join Style', 'Round')]
        self.rotateDirection = settings.value('Painting/Rotation/Direction', 'Clockwise')
        self.rotateAngle = settings.value('Painting/Rotation/Angle', '45', type=float)
        if self.rotateDirection == 'Counter-clockwise':
            self.rotateAngle *= -1

        # Grid settings
        self._grid.enableGrid = settings.value('Grid/Visibility', True, type=bool)
        self._grid.snapToGrid = settings.value('Grid/Snapping/Snap to grid', True, type=bool)
        self._grid.snapToGridSpacing = settings.value('Grid/Snapping/Snap to grid spacing', '10', type=int)
        self._grid.majorSpacingVisibility = settings.value('Grid/Major and minor grid points/Major grid points visibility', True, type=bool)
        self._grid.majorSpacing = settings.value('Grid/Major and minor grid points/Major grid points spacing', '100', type=int)
        self._grid.minorSpacingVisibility = settings.value('Grid/Major and minor grid points/Minor grid points visibility', True, type=bool)
        self._grid.minorSpacing = settings.value('Grid/Major and minor grid points/Minor grid points spacing', '20', type=int)
        if self._grid.enableGrid:
            self._grid.createGrid()
        else:
            self._grid.removeGrid()

        # Save/export settings
        self.autobackupEnable = settings.value('SaveExport/Autobackup/Enable', True, type=bool)
        # Set autobackup timer interval in ms
        self.autobackupTimerInterval = settings.value('SaveExport/Autobackup/Timer interval', '10', type=int)*1000
        self.autobackupTimer.setInterval(self.autobackupTimerInterval)
        self.showSchematicPreview = settings.value('SaveExport/Schematic/Show preview', True, type=bool)
        if not (hasattr(self, 'defaultSchematicSaveFolder') and self.defaultSchematicSaveFolder is None):
            self.defaultSchematicSaveFolder = settings.value('SaveExport/Schematic/Default save folder', './')
        # Create default directory if it does not exist
        if self.defaultSchematicSaveFolder is not None:
            if not os.path.isdir(self.defaultSchematicSaveFolder):
                os.mkdir(self.defaultSchematicSaveFolder)
        self.showSymbolPreview = settings.value('SaveExport/Symbol/Show preview', True, type=bool)
        if not (hasattr(self, 'defaultSymbolSaveFolder') and self.defaultSymbolSaveFolder is None):
            self.defaultSymbolSaveFolder = settings.value('SaveExport/Symbol/Default save folder', 'Resources/Symbols/Custom/')
        # Create default directory if it does not exist
        if self.defaultSymbolSaveFolder is not None:
            if not os.path.isdir(self.defaultSymbolSaveFolder):
                os.mkdir(self.defaultSymbolSaveFolder)
        self.defaultExportFormat = settings.value('SaveExport/Export/Default format', 'pdf').lower()
        if not (hasattr(self, 'defaultExportFolder') and self.defaultExportFolder is None):
            self.defaultExportFolder = settings.value('SaveExport/Export/Default folder', './')
        # Create default directory if it does not exist
        if self.defaultExportFolder is not None:
            if not os.path.isdir(self.defaultExportFolder):
                os.mkdir(self.defaultExportFolder)
        self.exportImageWhitespacePadding = settings.value('SaveExport/Export/Whitespace padding', '1.1', type=float)
        self.exportImageScaleFactor = settings.value('SaveExport/Export/Image scale factor', '2.0', type=float)

        # Mouse settings
        self.showMouseRect = settings.value('Mouse/Show rect', True, type=bool)
        if hasattr(self, 'mouseRect'):
            if self.showMouseRect is True:
                if not self.mouseRect in self.scene().items():
                    self.scene().addItem(self.mouseRect)
            elif self.mouseRect in self.scene().items():
                self.scene().removeItem(self.mouseRect)
        self.showAnimationPan = settings.value('Mouse/Animations/Pan', True, type=bool)
        self.showAnimationZoom = settings.value('Mouse/Animations/Zoom', True, type=bool)
        self.scrollModifierNone = settings.value('Mouse/PanningZooming/Modifier none', 'Zoom')
        self.scrollModifierCtrl = settings.value('Mouse/PanningZooming/Modifier Ctrl', 'Pan vertically')
        self.scrollModifierShift = settings.value('Mouse/PanningZooming/Modifier Shift', 'Pan horizontally')
        self.invertZoom = settings.value('Mouse/PanningZooming/Invert zoom', False, type=bool)

        # Apply shortcuts if they exist
        if 'Shortcuts' in settings.childGroups():
            self.applyShortcuts(settings)

        # Misc settings
        self.quickAddSymbol1 = settings.value('Misc/Quick Add Symbol/1', 'Resources/Symbols/Standard/Resistor.sym')
        self.quickAddSymbol2 = settings.value('Misc/Quick Add Symbol/2', 'Resources/Symbols/Standard/Resistor.sym')
        self.quickAddSymbol3 = settings.value('Misc/Quick Add Symbol/3', 'Resources/Symbols/Standard/Resistor.sym')
        self.quickAddSymbol4 = settings.value('Misc/Quick Add Symbol/4', 'Resources/Symbols/Standard/Resistor.sym')
        self.quickAddSymbol5 = settings.value('Misc/Quick Add Symbol/5', 'Resources/Symbols/Standard/Resistor.sym')
        self.defaultSymbolPreviewFolder = settings.value('Misc/Symbol Preview Folder/Default', 'Resources/Symbols/Standard/')
        # When the program is starting, myMainWindow will not have fileSystemModel
        if hasattr(self.window(), 'fileSystemModel'):
            self.window().pickSymbolPreviewDirectory(self.defaultSymbolPreviewFolder)
        self.symbolPreviewFolder1 = settings.value('Misc/Symbol Preview Folder/1', 'Resources/Symbols/Standard/')
        self.symbolPreviewFolder2 = settings.value('Misc/Symbol Preview Folder/2', 'Resources/Symbols/Standard/')
        self.symbolPreviewFolder3 = settings.value('Misc/Symbol Preview Folder/3', 'Resources/Symbols/Standard/')

    def applyShortcuts(self, settings):
        """Applies shortcuts for the various functions part of YCircuit"""
        ui = self.window().ui
        try:
            actionShortcuts = [
                # File menu
                ['New schematic', ui.action_newSchematic],
                ['Save schematic', ui.action_saveSchematic],
                ['Save schematic as', ui.action_saveSchematicAs],
                ['Save symbol', ui.action_saveSymbol],
                ['Save symbol as', ui.action_saveSymbolAs],
                ['Load schematic', ui.action_loadSchematic],
                ['Load symbol', ui.action_loadSymbol],
                ['Modify symbol', ui.action_modifySymbol],
                ['Export file', ui.action_exportFile],
                ['Import image', ui.action_importImage],
                ['Quit', ui.action_quit],
                # Edit menu
                ['Undo', ui.action_undo],
                ['Redo', ui.action_redo],
                ['Delete', ui.action_delete],
                ['Move', ui.action_move],
                ['Copy', ui.action_copy],
                ['Paste', ui.action_paste],
                ['Rotate', ui.action_rotate],
                ['Mirror', ui.action_mirror],
                ['Font', ui.action_pickFont],
                ['Bring forward', ui.action_heightBringForward],
                ['Send back', ui.action_heightSendBack],
                ['Reset height', ui.action_heightReset],
                ['Group', ui.action_group],
                ['Ungroup', ui.action_ungroup],
                ['Options', ui.action_options],
                # View menu
                ['Fit to view', ui.action_fitToView],
                ['Show pin(s)', ui.action_showPins],
                ['Snap net to pin', ui.action_snapNetToPin],
                ['Show grid', ui.action_showGrid],
                ['Snap to grid', ui.action_snapToGrid],
                ['Show major grid points', ui.action_showMajorGridPoints],
                ['Show minor grid points', ui.action_showMinorGridPoints],
                # Shape menu
                ['Draw line', ui.action_addLine],
                ['Draw 3-point arc', ui.action_addArc3Point],
                ['Draw rectangle', ui.action_addRectangle],
                ['Draw ellipse', ui.action_addEllipse],
                ['Draw circle', ui.action_addCircle],
                ['Draw text box', ui.action_addTextBox],
                ['Edit shape', ui.action_editShape],
                # Symbol menu
                ['Draw pin', ui.action_addPin],
                ['Draw wire', ui.action_addWire],
                ['Draw resistor', ui.action_addResistor],
                ['Draw capacitor', ui.action_addCapacitor],
                ['Draw ground', ui.action_addGround],
                ['Draw connection dot', ui.action_addDot],
                ['Quick add symbol 1', ui.action_quickAddSymbol1],
                ['Quick add symbol 2', ui.action_quickAddSymbol2],
                ['Quick add symbol 3', ui.action_quickAddSymbol3],
                ['Quick add symbol 4', ui.action_quickAddSymbol4],
                ['Quick add symbol 5', ui.action_quickAddSymbol5]
            ]
            for item, action in actionShortcuts:
                if settings.contains('Shortcuts/'+item):
                    action.setShortcut(QtGui.QKeySequence(settings.value('Shortcuts/'+item)))
        except:
            pass

    def addPin(self):
        """Load standard pin"""
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        self.loadRoutine('symbol', './Resources/Symbols/Standard/Pin.sym')
        self.loadItem.isPin = True

    def addWire(self):
        """Create a poly-line. The wire name used here is a relic
        from the past where poly-lines doubled as nets."""
        # Set _key to wire mode so that a wire is added when LMB is pressed
        self.escapeRoutine()
        self._keys['w'] = True
        self.currentWire = None
        self.statusbarMessage.emit('Left click to begin drawing a new line (press ESC to cancel)', 0)

    def addArc(self, points=3):
        """Create an arc with _points_ number of points"""
        # Set _key to arc mode so that an arc is added when LMB is pressed
        self.escapeRoutine()
        self._keys['arc'] = True
        self.arcPoints = points
        self.currentArc = None
        self.statusbarMessage.emit('Left click to begin drawing a new arc (press ESC to cancel)', 0)

    def addRectangle(self):
        """Create a rectangle"""
        # Set _key to rectangle mode so that a rectangle is added when LMB is pressed
        self.escapeRoutine()
        self._keys['rectangle'] = True
        self.currentRectangle = None
        self.statusbarMessage.emit('Left click to begin drawing a new rectangle (press ESC to cancel)', 0)

    def addCircle(self):
        """Create a circle"""
        # Set _key to circle mode so that a circle is added when LMB is pressed
        self.escapeRoutine()
        self._keys['circle'] = True
        self.currentCircle = None
        self.statusbarMessage.emit('Left click to begin drawing a new circle (press ESC to cancel)', 0)

    def addEllipse(self):
        """Create an ellipse"""
        # Set _key to ellipse mode so that an ellipse is added when LMB is pressed
        self.escapeRoutine()
        self._keys['ellipse'] = True
        self.currentEllipse = None
        self.statusbarMessage.emit('Left click to begin drawing a new ellipse (press ESC to cancel)', 0)

    def addTextBox(self):
        """Create a text box"""
        # Set _key to textBox mode so that a textbox is added when LMB is pressed
        self.escapeRoutine()
        cursor = self.cursor()
        cursor.setShape(QtCore.Qt.IBeamCursor)
        self.setCursor(cursor)
        self._keys['textBox'] = True
        self.currentTextBox = None
        self.statusbarMessage.emit('Left click to pick the location of the new text box (press ESC to cancel)', 0)

    def addImage(self):
        """Import an image"""
        self.escapeRoutine()
        cursor = self.cursor()
        cursor.setShape(QtCore.Qt.IBeamCursor)
        self.setCursor(cursor)
        self._keys['image'] = True
        self.currentImage = None
        self.statusbarMessage.emit('Left click to pick the location of the new image (press ESC to cancel)', 0)

    def addNet(self):
        """Add a net. Nets are different from wires in that nets can only be
        created at right angles and automatically merge/split as needed."""
        # Set _key to net mode so that a net is added when LMB is pressed
        self.escapeRoutine()
        self._keys['net'] = True
        self.currentNet = None
        self._grid.pinsPos = []
        # Create a list of all pins in the schematic
        for item in self.scene().items():
            if isinstance(item, myGraphicsItemGroup):
                if hasattr(item, 'isPin'):
                    if item.isPin is True:
                        self._grid.pinsPos.append(item.scenePos())
        self.statusbarMessage.emit('Left click to begin drawing a new net (press S to toggle snapping to pins or press ESC to cancel)', 0)

    def addResistor(self):
        """Load the standard resistor"""
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        self.loadRoutine('symbol', './Resources/Symbols/Standard/Resistor.sym')

    def addCapacitor(self):
        """Load the standard capacitor"""
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        self.loadRoutine('symbol', './Resources/Symbols/Standard/Capacitor.sym')

    def addGround(self):
        """Load the standard ground symbol"""
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        self.loadRoutine('symbol', './Resources/Symbols/Standard/Ground_earth.sym')

    def addDot(self):
        """Load the standard dot symbol"""
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        self.loadRoutine('symbol', './Resources/Symbols/Standard/Dot.sym')

    def addTransistor(self, kind='MOS', polarity='N', arrow=False):
        """Load the standard transistor symbol based on its kind and polarity"""
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        if kind == 'MOS':
            if polarity == 'N':
                if arrow is True:
                    self.loadRoutine('symbol', './Resources/Symbols/Standard/NFET_arrow.sym')
                else:
                    self.loadRoutine('symbol', './Resources/Symbols/Standard/NFET_noArrow.sym')
            else:
                if arrow is True:
                    self.loadRoutine('symbol', './Resources/Symbols/Standard/PFET_arrow.sym')
                else:
                    self.loadRoutine('symbol', './Resources/Symbols/Standard/PFET_noArrow.sym')
        elif kind == 'BJT':
            if polarity == 'N':
                self.loadRoutine('symbol', './Resources/Symbols/Standard/BJT_NPN.sym')
            if polarity == 'P':
                self.loadRoutine('symbol', './Resources/Symbols/Standard/BJT_PNP.sym')

    def addSource(self, kind='DCV'):
        """Load the standard dependent/independent source"""
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        if kind == 'DCV':
            self.loadRoutine('symbol', './Resources/Symbols/Standard/Source_DCV.sym')
        elif kind == 'DCI':
            self.loadRoutine('symbol', './Resources/Symbols/Standard/Source_DCI.sym')
        elif kind == 'AC':
            self.loadRoutine('symbol', './Resources/Symbols/Standard/Source_AC.sym')
        elif kind == 'VCVS':
            self.loadRoutine('symbol', './Resources/Symbols/Standard/Source_VCVS.sym')
        elif kind == 'VCCS':
            self.loadRoutine('symbol', './Resources/Symbols/Standard/Source_VCCS.sym')
        elif kind == 'CCVS':
            self.loadRoutine('symbol', './Resources/Symbols/Standard/Source_CCVS.sym')
        elif kind == 'CCCS':
            self.loadRoutine('symbol', './Resources/Symbols/Standard/Source_CCCS.sym')

    def quickAddSymbol(self, kind=1):
        """Quickly add symbols as defined in the settings file"""
        self.escapeRoutine()
        start = self.mapToGrid(self.currentPos)
        if kind == 1:
            if os.path.isfile(self.quickAddSymbol1):
                self.loadRoutine('symbol', self.quickAddSymbol1)
            else:
                self.statusbarMessage.emit('Please check that the quick access symbol exists', 1000)
        if kind == 2:
            if os.path.isfile(self.quickAddSymbol2):
                self.loadRoutine('symbol', self.quickAddSymbol2)
            else:
                self.statusbarMessage.emit('Please check that the quick access symbol exists', 1000)
        if kind == 3:
            if os.path.isfile(self.quickAddSymbol3):
                self.loadRoutine('symbol', self.quickAddSymbol3)
            else:
                self.statusbarMessage.emit('Please check that the quick access symbol exists', 1000)
        if kind == 4:
            if os.path.isfile(self.quickAddSymbol4):
                self.loadRoutine('symbol', self.quickAddSymbol4)
            else:
                self.statusbarMessage.emit('Please check that the quick access symbol exists', 1000)
        if kind == 5:
            if os.path.isfile(self.quickAddSymbol5):
                self.loadRoutine('symbol', self.quickAddSymbol5)
            else:
                self.statusbarMessage.emit('Please check that the quick access symbol exists', 1000)

    def autobackupRoutine(self):
        """Convenience function for saving the autobackup file"""
        if self.autobackupEnable is True:
            self.saveRoutine(mode='autobackup')
            self.autobackupFile.flush()

    def listOfItemsToSave(self, mode='schematicAs'):
        """Convenience function for generating the list of items to save. Most
        useful when paired with the autobackup utility. In such a case, we do
        not wish to save items that are eg. being selected/moved."""
        listOfItems = [item for item in self.scene().items() if item.parentItem() is None]
        # Remove the mouse diamond if it is present
        if self.mouseRect in listOfItems:
            listOfItems.remove(self.mouseRect)
        # If mode is not autobackup, return everything else
        if mode != 'autobackup':
            return listOfItems
        removeItems = []
        # Remove items being added/moved
        if self._keys['m'] is True or self._keys['add'] is True:
            removeItems = self.moveItems
        # Remove the current rectangle being drawn
        if self._keys['rectangle'] is True:
            removeItems = [self.currentRectangle]
        # Remove the current circle being drawn
        if self._keys['circle'] is True:
            removeItems = [self.currentCircle]
        # Remove the current ellipse being drawn
        if self._keys['ellipse'] is True:
            removeItems = [self.currentEllipse]
        # Remove the current wire being drawn
        if self._keys['w'] is True:
            removeItems = [self.currentWire]
        # Remove the current net being drawn
        if self._keys['net'] is True:
            removeItems = [self.currentNet]
            if hasattr(self.currentNet, 'perpLine'):
                if self.currentNet.perpLine is not None:
                    removeItems.append(self.currentNet.perpLine)
        # Remove the current arc being drawn
        if self._keys['arc'] is True:
            removeItems = [self.currentArc]
        for item in removeItems:
            if item in listOfItems:
                listOfItems.remove(item)
        return listOfItems

    def saveRoutine(self, mode='schematicAs'):
        """Handles saving of both symbols and schematics. For symbols and
        schematics, items are first parented to a myGraphicsItemGroup.
        The parent item is then saved into a corresponding .sym (symbol) and
        .sch (schematic) file. If the save option is a schematic, the items are then
        unparented.
        """
        # Cancel all other modes unless autosaving
        if mode != 'autobackup':
            self.escapeRoutine()
        else:
            selectedItems = self.scene().selectedItems()
            logger.info('Starting autobackup')
        possibleModes = ['schematic', 'schematicAs', 'symbol', 'symbolAs', 'autobackup']
        # Create list of items
        listOfItems = self.listOfItemsToSave(mode)
        # Return if no items are present
        if len(listOfItems) == 0:
            logger.info('Nothing to save')
            return
        if mode in possibleModes:
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
                logger.info('Setting origin for symbol at %s', origin)

            saveObject = myGraphicsItemGroup(None, origin, [])
            self.scene().addItem(saveObject)
            saveObject.origin = origin

            # Set relative origins of child items
            for item in listOfItems:
                item.origin = item.pos() - saveObject.origin
                if hasattr(item, 'isPin'):
                    if item.isPin is True:
                        saveObject.pins.append(item)
                item.lightenColour(False)
                logger.info('Setting origin for item %s to %s', item, item.origin)
            saveObject.setItems(listOfItems)

            saveFile = ''
            if mode == 'symbol':
                if self.symbolFileName is None:
                    fileDialog = myFileDialog(
                        self,
                        'Save symbol',
                        self.defaultSymbolSaveFolder,
                        filt='Symbols (*.sym)',
                        mode='save',
                        showSymbolPreview = self.showSymbolPreview)
                    self.defaultSymbolSaveFolder = None
                    if (fileDialog.exec_()):
                        saveFile = str(fileDialog.selectedFiles()[0])
                    if not saveFile.endswith('.sym'):
                        saveFile += '.sym'
                else:
                    saveFile = self.symbolFileName
            elif mode == 'symbolAs':
                fileDialog = myFileDialog(
                    self,
                    'Save symbol as',
                    self.defaultSymbolSaveFolder,
                    filt='Symbols (*.sym)',
                    mode='save',
                    showSymbolPreview = self.showSymbolPreview)
                self.defaultSymbolSaveFolder = None
                if (fileDialog.exec_()):
                    saveFile = str(fileDialog.selectedFiles()[0])
                if not saveFile.endswith('.sym'):
                    saveFile += '.sym'
            elif mode == 'schematic':
                if self.schematicFileName is None:
                    fileDialog = myFileDialog(
                        self,
                        'Save schematic',
                        self.defaultSchematicSaveFolder,
                        filt='Schematics (*.sch)',
                        mode='save',
                        showSchematicPreview = self.showSchematicPreview)
                    self.defaultSchematicSaveFolder = None
                    if (fileDialog.exec_()):
                        saveFile = str(fileDialog.selectedFiles()[0])
                    if not saveFile.endswith('.sch'):
                        saveFile += '.sch'
                else:
                    saveFile = self.schematicFileName
            elif mode == 'schematicAs':
                fileDialog = myFileDialog(
                    self,
                    'Save schematic as',
                    self.defaultSchematicSaveFolder,
                    filt='Schematics (*.sch)',
                    mode='save',
                    showSchematicPreview = self.showSchematicPreview)
                self.defaultSchematicSaveFolder = None
                if (fileDialog.exec_()):
                    saveFile = str(fileDialog.selectedFiles()[0])
                if not saveFile.endswith('.sch'):
                    saveFile += '.sch'
            elif mode == 'autobackup':
                saveFile = self.autobackupFile.fileName()

            if saveFile[:-4] != '':
                # Delete old autobackup file
                if mode != 'autobackup':
                    self.autobackupFile.close()
                    self.autobackupFile.remove()
                    logger.info('Closing old autobackup file')
                    # Create and save a preview of the file unless when creating an autobackup
                    if self.mouseRect in self.scene().items():
                        self.scene().removeItem(self.mouseRect)
                    saveObject.lightenColour(False)
                    saveObject.icon = QtCore.QByteArray()
                    buf = QtCore.QBuffer(saveObject.icon)
                    img = myIconProvider().createIconPixmap(saveObject, self.scene()).toImage()
                    img.save(buf, 'PNG', quality=10)
                    if self.showMouseRect is True:
                        self.scene().addItem(self.mouseRect)
                with open(saveFile, 'wb') as file:
                    logger.info('Saving to file %s', saveFile)
                    pickle.dump(saveObject, file, -1)
                if mode == 'symbol' or mode == 'symbolAs':
                    self.symbolFileName = saveFile
                    self.schematicFileName = None
                    self.autobackupFile = QtCore.QTemporaryFile(self.symbolFileName)
                if mode == 'schematic' or mode == 'schematicAs':
                    self.schematicFileName = saveFile
                    self.symbolFileName = None
                    self.autobackupFile = QtCore.QTemporaryFile(self.schematicFileName)
                if mode != 'autobackup':
                    self.autobackupFile.open()
                    self.autobackupFile.setAutoRemove(False)
                    with open(self.autobackupFile.fileName(), 'wb') as file:
                        pickle.dump(saveObject, file, -1)
                    logger.info('New autobackup file created at %s', self.autobackupFile.fileName())
                    self.undoStack.setClean()
                    logger.info('Setting undo stack to clean')

            # Always reparent items
            saveObject.reparentItems()
            self.scene().removeItem(saveObject)
            if mode == 'autobackup':
                for item in selectedItems:
                    item.setSelected(True)
            if self.itemAt(self.currentPos):
                item = self.itemAt(self.currentPos).topLevelItem()
                if item != self.mouseRect:
                    item.lightenColour(True)

    def exportRoutine(self):
        """
        For images, a rect slightly larger than the bounding rect of all items is
        created. This rect is then projected onto a QPixmap at a higher resolution to
        create the final image.
        """
        logger.info('Beginning export')
        # Remove grid from the scene to avoid saving it
        self._grid.removeGrid()
        if self.mouseRect in self.scene().items():
            self.scene().removeItem(self.mouseRect)
        # Return if no items are present
        if len(self.scene().items()) == 0:
            self._grid.createGrid()
            logger.info('Nothing to export')
            return
        # Deselect items before exporting
        selectedItems = self.scene().selectedItems()
        for item in selectedItems:
            item.setSelected(False)
        saveFile, saveFilter = QtWidgets.QFileDialog.getSaveFileName(
            self,
            'Export File',
            self.defaultExportFolder,
            'PDF files (*.pdf);;SVG files(*.svg);;PNG files (*.png);;JPG files (*.jpg);;BMP files (*.bmp);;TIFF files (*.tiff)',
            self.defaultExportFormat.upper() + ' files (*.' + self.defaultExportFormat + ')'
        )
        self.defaultExportFolder = None
        if '*.pdf' in saveFilter:
            saveFilter = 'pdf'
        elif '*.svg' in saveFilter:
            saveFilter = 'svg'
        elif '*.png' in saveFilter:
            saveFilter = 'png'
        elif '*.jpg' in saveFilter:
            saveFilter = 'jpg'
        elif '*.bmp' in saveFilter:
            saveFilter = 'bmp'
        elif '*.tiff' in saveFilter:
            saveFilter = 'tiff'
        # Check that file is valid
        if saveFile != '':
            if not saveFile.endswith('.' + saveFilter):
                saveFile = str(saveFile) + '.' + saveFilter
        else:
            # Add the grid back to the scene
            self._grid.createGrid()
            if self.showMouseRect is True:
                self.scene().addItem(self.mouseRect)
            return
        logger.info('Exporting to file %s', saveFile)
        if saveFilter == 'pdf':
            mode = 'pdf'
        elif saveFilter == 'svg':
            mode = 'svg'
        elif saveFilter in ['jpg', 'png', 'bmp', 'tiff']:
            mode = 'image'
            if saveFilter == 'jpg':
                quality = 90
            elif saveFilter == 'png':
                quality = 50
            elif saveFilter == 'bmp':
                quality = 1
            elif saveFilter == 'tiff':
                quality = 1
        # Create a rect that's scaled appropriately to have some whitespace
        sourceRect = self.scene().itemsBoundingRect()
        padding = self.exportImageWhitespacePadding
        scale = self.exportImageScaleFactor
        sourceRect.setWidth(int(padding * sourceRect.width()))
        sourceRect.setHeight(int(padding * sourceRect.height()))
        width, height = sourceRect.width(), sourceRect.height()
        if padding > 1:
            sourceRect.translate(-width * (padding - 1) / (padding * 2.),
                                 -height * (padding - 1) / (padding * 2.))
        logger.info('Source rectangle set to %s', sourceRect)
        if mode == 'pdf':
            # Initialize printer
            printer = QtPrintSupport.QPrinter(QtPrintSupport.QPrinter.HighResolution)
            # Choose appropriate format
            printer.setOutputFormat(printer.PdfFormat)
            printer.setOutputFileName(saveFile)
            printer.setFullPage(True)
            pageSize = QtGui.QPageSize(QtCore.QSize(width, height), matchPolicy=QtGui.QPageSize.ExactMatch)
            printer.setPageSize(pageSize)
            painter = QtGui.QPainter(printer)
            self.scene().render(painter, source=sourceRect)
            logger.info('Rendering PDF')
        elif mode == 'svg':
            svgGenerator = QtSvg.QSvgGenerator()
            svgGenerator.setFileName(saveFile)
            svgGenerator.setSize(QtCore.QSize(width, height))
            svgGenerator.setResolution(96)
            svgGenerator.setViewBox(QtCore.QRect(0, 0, width, height))
            painter = QtGui.QPainter(svgGenerator)
            self.scene().render(painter, source=sourceRect)
            logger.info('Rendering SVG')
        elif mode == 'image':
            # Create an image object
            img = QtGui.QImage(
                QtCore.QSize(scale * width, scale * height), QtGui.QImage.Format_RGB32)
            # Set background to white
            img.fill(QtGui.QColor('white'))
            painter = QtGui.QPainter(img)
            painter.setRenderHint(painter.SmoothPixmapTransform, True)
            painter.setRenderHint(painter.Antialiasing, True)
            painter.setRenderHint(painter.TextAntialiasing, True)
            targetRect = QtCore.QRectF(img.rect())
            self.scene().render(painter, targetRect, sourceRect)
            img.save(saveFile, saveFilter, quality=quality)
            logger.info('Rendering PNG to target rectangle %s', targetRect)

        # Need to stop painting to avoid errors about painter getting deleted
        painter.end()
        # Add the grid back to the scene when saving is done
        self._grid.createGrid()
        if self.showMouseRect is True:
            self.scene().addItem(self.mouseRect)
        # Reselect items after exporting is completed
        for item in selectedItems:
            item.setSelected(True)
        logger.info('Finishing export')

    def loadAutobackupRoutine(self, loadFile=None):
        """Convenience function that generates a message box asking the user
        whether they would like to recover from the backup"""
        # Ask if you would like to recover the autobackup
        msgBox = QtWidgets.QMessageBox(self)
        msgBox.setWindowTitle("Recover file")
        msgBox.setText("An autobackup file was detected.")
        msgBox.setInformativeText("Do you wish to recover from the autobackup file?")
        msgBox.setDetailedText(("Selecting No will automatically delete the "
        "autobackup file. The safest option is to answer Yes and then opening "
        "the manually saved schematic later if the autobackup save was not "
        "something you wanted to use."))
        msgBox.setStandardButtons(msgBox.Yes | msgBox.No)
        msgBox.setDefaultButton(msgBox.Yes)
        msgBox.setIcon(msgBox.Information)
        ret = msgBox.exec_()
        if ret == msgBox.Yes:
            logger.info('Loading autobackup file')
            return glob.glob(loadFile + '.*')[0]
        elif ret == msgBox.No:
            logger.info('Loading selected file')
            return loadFile

    def loadRoutine(self, mode='symbol', loadFile=None, loadItem=None):
        """This is the counterpart of the save routine. Used to load both schematics
        and symbols.
        """
        # It is possible that loadFile may be a folder, when clicked through
        # the symbol preview on the left. If so, return
        if loadFile is not None:
            if os.path.isdir(loadFile):
                return
        logger.info('Beginning load routine')
        possibleModes = ['schematic', 'symbol', 'symbolModify']
        if mode in possibleModes:
            if loadFile is None:
                loadFile = ''
                if mode == 'symbol' or mode == 'symbolModify':
                    fileDialog = myFileDialog(
                        self,
                        'Load Symbol',
                        self.defaultSymbolSaveFolder,
                        filt='Symbols (*.sym)',
                        mode='load',
                        showSymbolPreview=self.showSymbolPreview)
                    self.defaultSymbolSaveFolder = None
                elif mode == 'schematic':
                    fileDialog = myFileDialog(
                        self,
                        'Load Schematic',
                        self.defaultSchematicSaveFolder,
                        filt='Schematics (*.sch)',
                        mode='load',
                        showSchematicPreview=self.showSchematicPreview)
                    self.defaultSchematicSaveFolder = None
                if (fileDialog.exec_()):
                    loadFile = str(fileDialog.selectedFiles()[0])
            if loadFile != '':
                # Check to see if an autobackup file exists if the mode is
                # schematic or symbolModify
                logger.info('Loading file %s', loadFile)
                if mode == 'schematic' or mode == 'symbolModify':
                    if glob.glob(loadFile + '.*') != []:
                        loadFile = self.loadAutobackupRoutine(loadFile)
                with open(loadFile, 'rb') as file:
                    loadItem = pickle.load(file)
                if mode == 'schematic' or mode == 'symbolModify':
                    # Remove trailing characters from autobackup file .XXXXXX
                    if not loadFile.endswith(('.sch', '.sym')):
                        loadFile = loadFile[:-7]
                    if glob.glob(loadFile + '.*') != []:
                        # Remove the old autobackup file
                        os.remove(glob.glob(loadFile + '.*')[0])
            elif loadItem is None:
                return False
            if mode == 'schematic' or mode == 'symbolModify':
                self.schematicFileName = None
                self.symbolFileName = None
                # Remove old autobackup file if it exists
                # This will not exist when recovering from unsaved crash
                if hasattr(self, 'autobackupFile'):
                    self.autobackupFile.close()
                    self.autobackupFile.remove()
                    logger.info('Closing old autobackup file')
                if mode == 'schematic':
                    self.schematicFileName = loadFile
                    self.autobackupFile = QtCore.QTemporaryFile(self.schematicFileName)
                elif mode == 'symbolModify':
                    self.symbolFileName = loadFile
                    self.autobackupFile = QtCore.QTemporaryFile(self.symbolFileName)
                self.autobackupFile.open()
                self.autobackupFile.setAutoRemove(False)
                logger.info('Creating new autobackup file %s', self.autobackupFile.fileName())
                # Clear the scene
                if self.mouseRect in self.scene().items():
                    self.scene().removeItem(self.mouseRect)
                self.scene().clear()
                if self.showMouseRect is True:
                    self.scene().addItem(self.mouseRect)
                loadItem.__init__(
                    None,
                    QtCore.QPointF(0, 0),
                    loadItem.listOfItems,
                    mode='symbol')
                self.scene().addItem(loadItem)
                # loadItem.loadItems(mode)
            elif mode == 'symbol':
                logger.info('Loading item %s as a symbol', loadItem)
                self.loadItem = loadItem
                loadItem.__init__(
                    None,
                    self.mapToGrid(self.currentPos),
                    loadItem.listOfItems,
                    mode='symbol')
                self.scene().addItem(self.loadItem)
                self.loadItem.pinVisibility(self.showPins)
                # loadItem.loadItems('symbol')
            if mode == 'schematic' or mode == 'symbolModify':
                loadItem.setPos(loadItem.origin)
                loadItem.reparentItems()
                self.scene().removeItem(loadItem)
                self.fitToViewRoutine()
                self.undoStack.clear()
                logger.info('Clearing the undo stack')
                # Run an autobackup once items are loaded completely
                self.autobackupRoutine()
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
                self.statusbarMessage.emit(
                    'Left click to place the symbol (press ESC to cancel)',
                    0)
                self.updateMoveItems()
        # Save a copy locally so that items don't disappear
        self.items = self.scene().items()
        # Capture focus
        self.setFocus(True)
        logger.info('Load routine complete')

    def escapeRoutine(self):
        """Resets all variables to the default state"""
        logger.info('Cancelling previous operation')
        # If mouse had been clicked
        if self._mouse['1'] is True:
            # Unclick mouse
            self._mouse['1'] = False
            # Undo move commands
            if self._keys['m'] is True:
                self.undoStack.endMacro()
                # The failed move command still exists in the stack. Not sure how to remove it
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
            if self._keys['net'] is True:
                self.currentNet.cancelSegment()
            # Remove last arc being drawn
            if self._keys['arc'] is True:
                if self.currentArc is not None:
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
            # Remove last image being drawn
            if self._keys['image'] is True:
                self.scene().removeItem(self.currentImage)
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
        # Reset all move items
        self.moveItems = []
        # Clear the statusbar
        self.statusbarMessage.emit("", 0)

    def moveRoutine(self):
        """Preps to begin moving items"""
        self.escapeRoutine()
        self.updateMoveItems()
        self._keys['m'] = True
        if self.moveItems == []:
            self.statusbarMessage.emit(
                'Select items to move, then left click to pick the origin for the move (Press ESC to cancel)',
                0)
        else:
            self.statusbarMessage.emit("Left click to pick the origin for the move (Press ESC to cancel)", 0)

    def copyRoutine(self):
        """Preps to begin copying items"""
        self.escapeRoutine()
        self._keys['c'] = True
        self.updateMoveItems()
        # self.statusbarMessage.emit("Copy (Press ESC to cancel)", 0)
        if self.moveItems == []:
            self.statusbarMessage.emit('Please select items to copy first', 2000)
            self.escapeRoutine()
        else:
            self.statusbarMessage.emit("Left click to pick the origin for the copy (Press ESC to cancel)", 0)
            self.copyItemsToClipboard(self.scene().selectedItems())

    def pasteRoutine(self):
        """Paste items from the clipboard"""
        self.escapeRoutine()
        self._keys['v'] = True
        try:
            loadItem = pickle.loads(self.clipboard.mimeData().data('YCircuit'))
            self.loadRoutine(mode='symbol', loadFile='', loadItem=loadItem)
        except:
            self._keys['v'] = False
            self.statusbarMessage.emit('Nothing to paste', 2000)

    def copyItemsToClipboard(self, copiedItems):
        """Copy items to the clipboard"""
        listOfItems = []
        for item in copiedItems:
            listOfItems.append(item.createCopy())
            item.setSelected(False)
        x = min([item.scenePos().x() for item in listOfItems])
        y = min([item.scenePos().y() for item in listOfItems])
        origin = QtCore.QPointF(x, y)
        saveObject = myGraphicsItemGroup(None, origin, [])
        # self.scene().addItem(saveObject)
        saveObject.origin = origin
        # Set relative origins of child items
        for item in listOfItems:
            item.origin = item.pos() - saveObject.origin
            logger.info('Setting origin for item %s to %s', item, item.origin)
            self.scene().removeItem(item)
        saveObject.setItems(listOfItems)
        mimeData = QtCore.QMimeData()
        mimeData.setData('YCircuit', pickle.dumps(saveObject))
        self.clipboard.setMimeData(mimeData)
        # Reselect original items
        for item in copiedItems:
            item.setSelected(True)

    def deleteRoutine(self):
        """Delete selected items"""
        if self.scene().selectedItems() == []:
            self.statusbarMessage.emit('Please select item(s) to delete first', 2000)
            return
        self.undoStack.beginMacro('')
        itemsToDelete = self.scene().selectedItems()
        for item2 in self.scene().selectedItems():
            if isinstance(item2, Net):
                netList = [item for item in self.scene().items() if
                           (isinstance(item, Net) and
                            item.collidesWithItem(item2)) and
                           item not in self.scene().selectedItems()
                ]
                pinList = [item for item in self.scene().items() if
                            (isinstance(item, myGraphicsItemGroup) and
                            hasattr(item, 'isPin') and
                            item.isPin is True and
                            item.collidesWithItem(self.currentNet))
                ]
                if item2 in netList:
                    netList.remove(item2)
                for item in netList[:]:
                    mergedNet = item.mergeNets(netList[:], self.undoStack)
                    if mergedNet is not None:
                        mergedNet.splitNets(netList[:], pinList, self.undoStack)
        del1 = Delete(None, self.scene(), itemsToDelete)
        self.undoStack.push(del1)
        self.undoStack.endMacro()
        self.statusbarMessage.emit("Delete", 2000)

    def fitToViewRoutine(self):
        """Resizes viewport so that all items drawn are visible"""
        if len(self.scene().items()) == 1:
            # Fit to (0, 0, 800, 800) if nothing is present
            rect = QtCore.QRectF(0, 0, 800, 800)
            self.fitInView(rect, QtCore.Qt.KeepAspectRatio)
            logger.info('Set viewport to %s', rect)
        else:
            if self.mouseRect in self.scene().items():
                self.scene().removeItem(self.mouseRect)
            self.fitInView(self.scene().itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)
            if self.showMouseRect is True:
                self.scene().addItem(self.mouseRect)
            logger.info('Set viewport to %s', self.scene().itemsBoundingRect())

    def togglePinsRoutine(self):
        """Toggles visibility of pins on symbols"""
        self.showPins = not self.showPins
        for item in self.scene().items():
            if isinstance(item, myGraphicsItemGroup):
                item.pinVisibility(self.showPins)

    def toggleSnapNetToPinRoutine(self):
        """Toggles snapping of nets to nearest pin while drawing nets"""
        self._grid.snapNetToPin = not self._grid.snapNetToPin

    def toggleGridRoutine(self):
        """Toggles grid on and off"""
        self._grid.enableGrid = not self._grid.enableGrid
        if self._grid.enableGrid is True:
            self._grid.createGrid()
            self.statusbarMessage.emit('The grid is now visible', 2000)
            logger.info('Grid set to visible')
        else:
            self.setBackgroundBrush(QtGui.QBrush())
            self.statusbarMessage.emit('The grid is no longer visible', 2000)
            logger.info('Grid set to invisible')

    def toggleSnapToGridRoutine(self, state):
        """Toggles drawings snapping to grid"""
        self._grid.snapToGrid = state
        if state is True:
            self.statusbarMessage.emit('Snap to grid is enabled', 2000)
            logger.info('Snap to grid is enabled')
        else:
            self.statusbarMessage.emit('Snap to grid is disabled', 2000)
            logger.info('Snap to grid is disabled')

    def changeSnapToGridSpacing(self, spacing):
        """Changes the snap to grid spacing"""
        if spacing != self._grid.snapToGridSpacing:
            self._grid.snapToGridSpacing = spacing

    def toggleMajorGridPointsRoutine(self, state):
        """Toggles major grid points on and off"""
        self._grid.majorSpacingVisibility = state
        if state is True:
            self.statusbarMessage.emit('Major grid points are now visible', 2000)
            logger.info('Major grid points set to visible')
        else:
            self.statusbarMessage.emit('Major grid points are no longer visible', 2000)
            logger.info('Major grid points set to invisible')
        if self._grid.enableGrid is True:
            self._grid.createGrid()

    def changeMajorGridPointSpacing(self, spacing):
        """Changes the major grid point spacing"""
        if spacing != self._grid.majorSpacing:
            self._grid.majorSpacing = spacing
            self.statusbarMessage.emit('Major grid point spacing changed to ' + str(spacing), 2000)
            if self._grid.enableGrid is True:
                self._grid.createGrid()

    def toggleMinorGridPointsRoutine(self, state):
        """Toggles minor grid points on and off"""
        self._grid.minorSpacingVisibility = state
        if state is True:
            self.statusbarMessage.emit('Minor grid points are now visible', 2000)
            logger.info('Minor grid points set to visible')
        else:
            self.statusbarMessage.emit('Minor grid points are no longer visible', 2000)
            logger.info('Minor grid points set to invisible')
        if self._grid.enableGrid is True:
            self._grid.createGrid()

    def changeMinorGridPointSpacing(self, spacing):
        """Changes the minor grid point spacing"""
        if spacing != self._grid.minorSpacing:
            self._grid.minorSpacing = spacing
            self.statusbarMessage.emit('Minor grid point spacing changed to ' + str(spacing), 2000)
            if self._grid.enableGrid is True:
                self._grid.createGrid()

    def changeFontRoutine(self, selectedFont):
        """Convenience function for changing the font to selectedFont"""
        if self.scene().selectedItems() != []:
            sameFont = True
            for item in self.scene().selectedItems():
                if isinstance(item, TextBox):
                    if selectedFont.toString() != item.font().toString():
                        sameFont = False
                        break
            if sameFont is False:
                changeFont = ChangeFont(
                    None,
                    self.scene().selectedItems(),
                    font=selectedFont)
                self.undoStack.push(changeFont)
        else:
            self.selectedFont = selectedFont
        self.statusbarMessage.emit("Changed font to %s %s" %
                                   (selectedFont.family(), selectedFont.pointSize()),
                                   2000)

    def changeHeightRoutine(self, mode='reset'):
        """Changes the height of the selected items. If mode is 'reset', sets
        the height to 0."""
        if self.scene().selectedItems == []:
            return
        else:
            changeHeight = ChangeHeight(
                None,
                self.scene().selectedItems(),
                mode=mode)
            self.undoStack.push(changeHeight)
        # If only 1 item is selected, report its height
        info = ''
        if len(self.scene().selectedItems()) == 1:
            info = ' to ' + str(self.scene().selectedItems()[0].zValue())
        if mode == 'forward':
            self.statusbarMessage.emit(
                "Brought selected item(s) forward" + info,
                2000)
        elif mode == 'back':
            self.statusbarMessage.emit(
                "Sent selected item(s) back" + info,
                2000)
        elif mode == 'reset':
            self.statusbarMessage.emit(
                "Reset the height(s) of the selected item(s)",
                2000)

    def changeWidthRoutine(self, selectedWidth):
        """Changes the width of the selected items to selectedWidth."""
        if self.scene().selectedItems() != []:
            sameWidth = True
            for item in self.scene().selectedItems():
                if isinstance(item, myGraphicsItemGroup):
                    if selectedWidth != item.getLocalPenParameters('width'):
                        sameWidth = False
                        break
                elif isinstance(item, TextBox):
                    pass
                elif selectedWidth != item.localPen.width():
                    sameWidth = False
                    break
            if sameWidth is False:
                changePen = ChangePen(
                    None,
                    self.scene().selectedItems(),
                    width=selectedWidth)
                self.undoStack.push(changePen)
                self.statusbarMessage.emit(
                    "Changed pen width of the selected item(s) to %d" %(selectedWidth),
                    2000)
        elif selectedWidth != self.selectedWidth:
            self.selectedWidth = selectedWidth
            self.statusbarMessage.emit(
                "Changed pen width to %d" %(selectedWidth),
                2000)

    def changePenColourRoutine(self, selectedPenColour):
        """Changes the pen colour for the selected items to selectedPenColour."""
        selectedPenColour = QtGui.QColor(selectedPenColour)
        if self.scene().selectedItems() != []:
            sameColour = True
            for item in self.scene().selectedItems():
                if isinstance(item, myGraphicsItemGroup):
                    if selectedPenColour != item.getLocalPenParameters('colour'):
                        sameColour = False
                        break
                elif selectedPenColour != item.localPen.color():
                    sameColour = False
                    break
            if sameColour is False:
                changePen = ChangePen(
                    None,
                    self.scene().selectedItems(),
                    penColour=selectedPenColour)
                self.undoStack.push(changePen)
                self.statusbarMessage.emit(
                    "Changed pen colour of the selected item(s) to %s" %(selectedPenColour.name()),
                    2000)
        elif selectedPenColour != QtGui.QColor(self.selectedPenColour):
            self.selectedPenColour = selectedPenColour
            self.statusbarMessage.emit(
                "Changed pen colour to %s" %(selectedPenColour.name()),
                2000)

    def changePenStyleRoutine(self, selectedPenStyle):
        """Changes the pen style for the selected items to selectedPenStyle."""
        styles = {
            1: 'solid',
            2: 'dash',
            3: 'dot',
            4: 'dash-dot',
            5: 'dash-dot-dot'
        }
        if self.scene().selectedItems() != []:
            samePenStyle = True
            for item in self.scene().selectedItems():
                if isinstance(item, myGraphicsItemGroup):
                    if selectedPenStyle != item.getLocalPenParameters('style'):
                        samePenStyle = False
                        break
                elif selectedPenStyle != item.localPen.style():
                    samePenStyle = False
                    break
            if samePenStyle is False:
                changePen = ChangePen(
                    None,
                    self.scene().selectedItems(),
                    penStyle=selectedPenStyle)
                self.undoStack.push(changePen)
                self.statusbarMessage.emit(
                    "Changed the pen style of the selected item(s) to %s" %(styles[selectedPenStyle]),
                    2000)
        elif selectedPenStyle != self.selectedPenStyle:
            self.selectedPenStyle = selectedPenStyle
            self.statusbarMessage.emit(
                "Changed pen style to %s" %(styles[selectedPenStyle]),
                2000)

    def changePenCapStyleRoutine(self, selectedPenCapStyle):
        """Changes the pen cap style for the selected items to
        selectedPenCapStyle."""
        styles = {
            0x10: 'square',
            0x20: 'round',
            0x00: 'flat',
        }
        if self.scene().selectedItems() != []:
            samePenCapStyle = True
            for item in self.scene().selectedItems():
                if isinstance(item, myGraphicsItemGroup):
                    if selectedPenCapStyle != item.getLocalPenParameters('capStyle'):
                        samePenCapStyle = False
                        break
                elif selectedPenCapStyle != item.localPen.capStyle():
                    samePenCapStyle = False
                    break
            if samePenCapStyle is False:
                changePen = ChangePen(
                    None,
                    self.scene().selectedItems(),
                    penCapStyle=selectedPenCapStyle)
                self.undoStack.push(changePen)
                self.statusbarMessage.emit(
                    "Changed the pen cap style of the selected item(s) to %s" %(styles[selectedPenCapStyle]),
                    2000)
        elif selectedPenCapStyle != self.selectedPenCapStyle:
            self.selectedPenCapStyle = selectedPenCapStyle
            self.statusbarMessage.emit(
                "Changed pen cap style to %s" %(styles[selectedPenCapStyle]),
                2000)

    def changePenJoinStyleRoutine(self, selectedPenJoinStyle):
        """Changes the pen join style for the selected items to
        selectedPenJoinStyle."""
        styles = {
            0x80: 'round',
            0x00: 'miter',
            0x40: 'bevel',
        }
        if self.scene().selectedItems() != []:
            samePenJoinStyle = True
            for item in self.scene().selectedItems():
                if isinstance(item, myGraphicsItemGroup):
                    if selectedPenJoinStyle != item.getLocalPenParameters('joinStyle'):
                        samePenJoinStyle = False
                        break
                elif selectedPenJoinStyle != item.localPen.joinStyle():
                    samePenJoinStyle = False
                    break
            if samePenJoinStyle is False:
                changePen = ChangePen(
                    None,
                    self.scene().selectedItems(),
                    penJoinStyle=selectedPenJoinStyle)
                self.undoStack.push(changePen)
                self.statusbarMessage.emit(
                    "Changed the pen join style of the selected item(s) to %s" %(styles[selectedPenJoinStyle]),
                    2000)
        elif selectedPenJoinStyle != self.selectedPenJoinStyle:
            self.selectedPenJoinStyle = selectedPenJoinStyle
            self.statusbarMessage.emit(
                "Changed pen join style to %s" %(styles[selectedPenJoinStyle]),
                2000)

    def changeBrushColourRoutine(self, selectedBrushColour):
        """Changes the brush colour for the selected items to
        selectedBrushColour."""
        selectedBrushColour = QtGui.QColor(selectedBrushColour)
        if self.scene().selectedItems() != []:
            sameBrushColour = True
            for item in self.scene().selectedItems():
                if isinstance(item, myGraphicsItemGroup):
                    if selectedBrushColour != item.getLocalBrushParameters('colour'):
                        sameBrushColour = False
                        break
                elif selectedBrushColour != item.localBrush.color():
                    sameBrushColour = False
                    break
            if sameBrushColour is False:
                changeBrush = ChangeBrush(
                    None,
                    self.scene().selectedItems(),
                    brushColour=selectedBrushColour)
                self.undoStack.push(changeBrush)
                self.statusbarMessage.emit(
                    "Changed the brush colour of the selected item(s) to %s" %(selectedBrushColour.name()),
                    2000)
        elif selectedBrushColour != QtGui.QColor(self.selectedBrushColour):
            self.selectedBrushColour = selectedBrushColour
            self.statusbarMessage.emit(
                "Changed brush colour to %s" %(selectedBrushColour.name()),
                2000)

    def changeBrushStyleRoutine(self, selectedBrushStyle):
        """Changes the brush style for the selected items to
        selectedBrushStyle."""
        styles = {
            0: 'no fill',
            1: 'solid',
        }
        if self.scene().selectedItems() != []:
            sameBrushStyle = True
            for item in self.scene().selectedItems():
                if isinstance(item, myGraphicsItemGroup):
                    if selectedBrushStyle != item.getLocalBrushParameters('style'):
                        sameBrushStyle = False
                        break
                elif selectedBrushStyle != item.localBrush.style():
                    sameBrushStyle = False
                    break
            if sameBrushStyle is False:
                changeBrush = ChangeBrush(
                    None,
                    self.scene().selectedItems(),
                    brushStyle=selectedBrushStyle)
                self.undoStack.push(changeBrush)
                self.statusbarMessage.emit(
                    "Changed the brush style of the selected item(s) to %s" %(styles[selectedBrushStyle]),
                    2000)
        elif selectedBrushStyle != self.selectedBrushStyle:
            self.selectedBrushStyle = selectedBrushStyle
            self.statusbarMessage.emit(
                "Changed brush style to %s" %(styles[selectedBrushStyle]),
                2000)

    def mousePressEvent(self, event):
        self.currentPos = event.pos()
        self.currentX = self.currentPos.x()
        self.currentY = self.currentPos.y()
        # Disable drag by default
        self.dragMove = False
        # If no modifiers are enabled and not selecting origin for symbol
        if event.modifiers() == QtCore.Qt.NoModifier and not self.selectOrigin is True:
            # Only if dragging using LMB
            if event.button() == QtCore.Qt.LeftButton:
                # Remove mouseRect
                if self.mouseRect in self.scene().items():
                    self.scene().removeItem(self.mouseRect)
                # If item under cursor
                if self.itemAt(self.currentPos) is not None:
                    item = self.itemAt(self.currentPos).topLevelItem()
                    # If no other items are selected, select item under cursor
                    if self.scene().selectedItems() == []:
                        item.setSelected(True)
                    # If item under cursor in selected items
                    if item in self.scene().selectedItems():
                        # If no other mode is active
                        if all(value == False for value in self._keys.values()):
                            logger.info('Beginning moving by dragging')
                            self.dragMove = True
                            self._keys['m'] = True
                if self.showMouseRect is True:
                    self.scene().addItem(self.mouseRect)
        # If copy mode is on
        if self._keys['c'] is True:
            # Check to make sure this is the first click
            if self._mouse['1'] is False:
                logger.info('Creating copies of items %s', self.scene().selectedItems())
                for item in self.scene().selectedItems():
                    item.createCopy()
                # Save a copy locally so that items don't disappear
                self.items = self.scene().items()
                # self.copyItemsToClipboard(self.scene().selectedItems())
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
                self.statusbarMessage.emit('Left click to place item(s) (press ESC to cancel)', 0)
                if self.dragMove is True:
                    self.statusbarMessage.emit('Move mouse to desired location and release to place the item(s)', 0)
                self.moveStartPoint = self.mapToGrid(event.pos())
                logger.info('Beginning move from %s', self.moveStartPoint)
                for i in self.moveItems:
                    i.moveTo(self.moveStartPoint, 'start')
                # Create a macro and save all rotate/mirror commands
                self.undoStack.beginMacro('')
                # Evaluate if any new nets need to be split/merged
                # Only do this check if moving and *not* for copying
                if self._keys['c'] is False:
                    for item2 in self.moveItems:
                        if isinstance(item2, Net):
                            netList = [item for item in self.scene().items() if
                                       (isinstance(item, Net) and
                                        item.collidesWithItem(item2)) and
                                       item not in self.scene().selectedItems()
                            ]
                            pinList = [item for item in self.scene().items() if
                                    (isinstance(item, myGraphicsItemGroup) and
                                        hasattr(item, 'isPin') and
                                        item.isPin is True and
                                        item.collidesWithItem(self.currentNet))
                            ]
                            if item2 in netList:
                                netList.remove(item2)
                            for item in netList[:]:
                                mergedNet = item.mergeNets(netList, self.undoStack)
                                if mergedNet is not None:
                                    mergedNet.splitNets(netList, pinList, self.undoStack)
            # End moving if LMB is clicked again and selection is not empty
            elif self.moveItems != []:
                point = self.mapToGrid(event.pos())
                if self._keys['c'] is True:
                    copy_ = Copy(None, self.scene(), self.moveItems, point=point)
                    self.undoStack.push(copy_)
                    logger.info('Finishing copy')
                else:
                    # Cancel the move and add the move to undo stack properly
                    for item in self.moveItems:
                        item.moveTo(None, 'cancel')
                    if self.moveStartPoint != point:
                        move = Move(
                            None,
                            self.scene(),
                            self.moveItems,
                            startPoint=self.moveStartPoint,
                            stopPoint=point)
                        self.undoStack.push(move)
                        logger.info('Finishing move')
                # Evaluate if any new nets need to be split/merged
                # if self._keys['c'] is False:
                if True:
                    for item2 in self.moveItems:
                        if isinstance(item2, Net):
                            netList = [item for item in self.scene().items() if
                                       (isinstance(item, Net) and
                                        item.collidesWithItem(item2)) and
                                       item not in self.scene().selectedItems()
                            ]
                            pinList = [item for item in self.scene().items() if
                                    (isinstance(item, myGraphicsItemGroup) and
                                        hasattr(item, 'isPin') and
                                        item.isPin is True and
                                        item.collidesWithItem(self.currentNet))
                            ]
                            mergedNet = item2.mergeNets(netList, self.undoStack)
                            if mergedNet is not None:
                                mergedNet.splitNets(netList, pinList, self.undoStack)
                            elif item2.scene() is not None:
                                item2.splitNets(netList, pinList, self.undoStack)
                # End move command once item has been placed
                self._keys['m'] = False
                self._keys['c'] = False
                self.statusbarMessage.emit("", 0)
                self.undoStack.endMacro()
                # Undo action if nothing was moved
                if point == self.moveStartPoint:
                    self.undoStack.undo()
                # for item in self.moveItems:
                #     item.setSelected(False)
                self.updateMoveItems()
        if self._keys['add'] is True:
            if (event.button() == QtCore.Qt.LeftButton):
                # add = Add(None, self.scene(), self.loadItem, symbol=True, origin=self.mapToGrid(event.pos()), rotateAngle=self.rotations*self.rotateAngle, reflect=self.reflections)
                add = Add(
                    None,
                    self.scene(),
                    self.loadItem,
                    symbol=True,
                    pinVisibility=self.window().ui.action_showPins,
                    origin=self.mapToGrid(event.pos()),
                    transform=self.loadItem.transform())
                self.undoStack.beginMacro('')
                self.undoStack.push(add)
                if self._keys['v'] is True:
                    logger.info('Ungrouping pasted items')
                    ungroup = Ungroup(None, self.scene(), add.item)
                    self.undoStack.push(ungroup)
                self.undoStack.endMacro()
        if self._keys['edit'] is True:
            item = self.scene().selectedItems()[0]
            # Also accounts for arcs because they are subclassed from Wire
            if isinstance(item, Wire):
                if (event.button() == QtCore.Qt.LeftButton):
                    self.statusbarMessage.emit('Left click to place the current vertex here and move to the next one (press ESC when done)', 0)
                    edit = Edit(
                        None,
                        self.scene(),
                        item,
                        self.mapToGrid(event.pos()),
                        clicked=True)
                    self.undoStack.push(edit)
                    self.undoStack.endMacro()
                    self.undoStack.beginMacro('')
                    # Adjust cursor if the item is a wire
                    cursor = self.cursor()
                    sceneP = item.mapToScene(item.editPointLocation(item.editPointNumber))
                    viewP = self.mapFromScene(sceneP)
                    cursor.setPos(self.viewport().mapToGlobal(viewP))
                    edit = Edit(None, self.scene(), item, sceneP)
                    self.undoStack.push(edit)
            else:
                self._keys['edit'] = False
                if (event.button() == QtCore.Qt.LeftButton):
                    self._mouse['1'] = False
                    edit = Edit(None,
                                self.scene(), item,
                                self.mapToGrid(event.pos()))
                    self.undoStack.push(edit)
                    self.statusbarMessage.emit('', 0)
            if self._mouse['1'] is False:
                self.undoStack.endMacro()
        # Only propagate these events downwards if move and copy are disabled or if nothing is selected or if a symbol is not being added
        if self.moveItems == [] and self._keys['m'] is True:
            super().mousePressEvent(event)
        if self._keys['c'] is False and self._keys['m'] is False and self._keys['add'] is False and self._keys['edit'] is False:
            super().mousePressEvent(event)

    def updateMoveItems(self):
        """Simple function that generates a list of selected items"""
        self.moveItems = self.scene().selectedItems()
        logger.debug('Updating move items list to %s', self.moveItems)

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
                mirror = Mirror(None,
                                self.scene(), self.moveItems,
                                self._keys['m'] and self._mouse['1'], point)
                # If a new item is being added, don't push mirror onto the undo stack
                if self._keys['add'] is False:
                    self.undoStack.push(mirror)
                else:
                    mirror.redo()
                self.statusbarMessage.emit("Mirrored item(s)", 2000)
                # for item in self.moveItems:
                #     item.reflect(self._keys['m'], point)
            else:
                # Keep track of number of rotations
                self.rotations += 1
                self.rotations %= 360 / self.rotateAngle
                point = self.mapToGrid(self.currentPos)
                rotate = Rotate(None,
                                self.scene(), self.moveItems,
                                self._keys['m'] and self._mouse['1'], point,
                                self.rotateAngle)
                # If a new item is being added, don't push rotate onto the undo stack
                if self._keys['add'] is False:
                    self.undoStack.push(rotate)
                else:
                    rotate.redo()
                self.statusbarMessage.emit("Rotated item(s) by %d degrees" %(self.rotateAngle), 2000)
                # for item in self.moveItems:
                #     item.rotateBy(self._keys['m'], point, self.rotateAngle)

    def mouseReleaseEvent(self, event):
        # Only propagate these events downwards if move and copy are disabled or if nothing is selected or if a symbol is not being added
        if self.moveItems == []:
            super().mouseReleaseEvent(event)
        elif self._keys['c'] is False and self._keys['m'] is False and self._keys['add'] is False:
            super().mouseReleaseEvent(event)
        # If drag move is on, generate a press event and turn it off
        if self.dragMove is True:
            self.dragMove = False
            mouseEvent = QtGui.QMouseEvent(
                event.MouseButtonPress,
                event.localPos(),
                event.screenPos(),
                QtCore.Qt.LeftButton,
                QtCore.Qt.LeftButton,
                QtCore.Qt.NoModifier)
            self.mousePressEvent(mouseEvent)
            logger.info('Finishing moving by dragging')
        # If wire or arc mode are on
        if self._keys['w'] is True or self._keys['arc'] is True:
            # Keep drawing new wire segments
            if event.button() == QtCore.Qt.LeftButton:
                self._mouse['1'] = True
            if self._mouse['1'] is True:
                self.oldPos = self.currentPos
                self.currentPos = event.pos()
                self.currentX = self.currentPos.x()
                self.currentY = self.currentPos.y()
                start = self.mapToGrid(self.currentPos)
                if self._keys['w'] is True:
                    self.statusbarMessage.emit('Left click to place the next vertex (Right click to end this line and start a new line or press ESC to cancel)', 0)
                    # If it is a right click, cancel this wire
                    # and wait for another LMB
                    if event.button() == QtCore.Qt.RightButton:
                        if self.currentWire is not None:
                            self._mouse['1'] = False
                            self.currentWire.cancelSegment()
                            self.currentWire = None
                        logger.info('End drawing wire')
                    # Create new wire if none exists
                    elif self.currentWire is None:
                        logger.info('Begin drawing a wire at %s', start)
                        self.currentWire = Wire(
                            None,
                            start,
                            penColour=self.selectedPenColour,
                            width=self.selectedWidth,
                            penStyle=self.selectedPenStyle,
                            penCapStyle=self.selectedPenCapStyle,
                            penJoinStyle=self.selectedPenJoinStyle,
                            brushColour=self.selectedBrushColour,
                            brushStyle=self.selectedBrushStyle)
                        self.scene().addItem(self.currentWire)
                    # If wire exists, add segments
                    else:
                        draw = Draw(None, self.scene(), self.currentWire, start)
                        self.undoStack.push(draw)
                elif self._keys['arc'] is True:
                    self.statusbarMessage.emit('Left click to place the next vertex (press ESC to cancel)', 0)
                    # Create new arc if none exists
                    if self.currentArc is None:
                        logger.info('Begin drawing arc')
                        self.currentArc = Arc(
                            None,
                            start,
                            penColour=self.selectedPenColour,
                            width=self.selectedWidth,
                            penStyle=self.selectedPenStyle,
                            penCapStyle=self.selectedPenCapStyle,
                            penJoinStyle=self.selectedPenJoinStyle,
                            brushColour=self.selectedBrushColour,
                            brushStyle=self.selectedBrushStyle,
                            points=self.arcPoints)
                        add = Add(None, self.scene(), self.currentArc)
                        self.undoStack.push(add)
                    # If arc exists, add segments
                    else:
                        logger.info('Setting arc point %d to %s', self.currentArc.clicks, start)
                        self.currentArc.updateArc(start, click=True)
                        if self.currentArc.clicks == self.currentArc.points:
                            self.currentArc = None
            for item in self.scene().selectedItems():
                item.setSelected(False)
        if self._keys['net'] is True:
            if event.button() == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.statusbarMessage.emit('Left click to complete drawing this net (Right click to change the orientation, press S to toggle snapping to pins or press ESC to cancel)', 0)
                self.currentPos = event.pos()
                start = self.mapToGrid(self.currentPos, pin=True)
                # Create new net if none exists
                if self.currentNet is None:
                    logger.info('Begin drawing net at %s', start)
                    self.currentNet = Net(
                        None,
                        start,
                        penColour=self.selectedPenColour,
                        width=self.selectedWidth,
                        penStyle=self.selectedPenStyle,
                        penCapStyle=self.selectedPenCapStyle,
                        penJoinStyle=self.selectedPenJoinStyle,
                        brushColour=self.selectedBrushColour,
                        brushStyle=self.selectedBrushStyle)
                    # Add the original net
                    self.scene().addItem(self.currentNet)
            else:
                self.statusbarMessage.emit('Left click to begin drawing a new net (press S to toggle snapping to pins or press ESC to cancel)', 0)
                if self.currentNet is not None:
                    netList = [item for item in self.scene().items() if
                               (isinstance(item, Net) and
                                item.collidesWithItem(self.currentNet))
                    ]
                    pinList = [item for item in self.scene().items() if
                               (isinstance(item, myGraphicsItemGroup) and
                                hasattr(item, 'isPin') and
                                item.isPin is True and
                                item.collidesWithItem(self.currentNet))
                    ]
                    netList.remove(self.currentNet)
                    self.scene().removeItem(self.currentNet)
                    # Only do this if current net is not 0 length
                    if self.currentNet.line().length() > 0.01:
                        self.undoStack.beginMacro('')
                        add = Add(None, self.scene(), self.currentNet)
                        self.undoStack.push(add)
                        mergedNet = self.currentNet.mergeNets(netList, self.undoStack)
                        if mergedNet is not None:
                            mergedNet.splitNets(netList, pinList, self.undoStack)
                        else:
                            self.currentNet.splitNets(netList, pinList, self.undoStack)
                        # Add the perpendicular line properly, if it exists
                        if self.currentNet.perpLine is not None:
                            netList = [item for item in self.scene().items() if
                                       (isinstance(item, Net) and
                                        item.collidesWithItem(self.currentNet.perpLine))
                            ]
                            pinList = [item for item in self.scene().items() if
                                    (isinstance(item, myGraphicsItemGroup) and
                                        hasattr(item, 'isPin') and
                                        item.isPin is True and
                                        item.collidesWithItem(self.currentNet.perpLine))
                            ]
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
                                if mergedNet is not None:
                                    mergedNet.splitNets(netList, pinList, self.undoStack)
                                else:
                                    self.currentNet.perpLine.splitNets(netList, pinList, self.undoStack)
                        self.undoStack.endMacro()
                    self.currentNet = None
                    logger.info('Finish drawing net')
            if event.button() == QtCore.Qt.RightButton:
                if self.currentNet is not None:
                    self.currentNet.changeRightAngleMode(self.mapToGrid(event.pos()))
            for item in self.scene().selectedItems():
                item.setSelected(False)
        # If rectangle mode is on, add a new rectangle
        if self._keys['rectangle'] is True:
            if event.button() == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.statusbarMessage.emit('Left click to finish drawing the rectangle (press ESC to cancel)', 0)
                self.currentPos = event.pos()
                start = self.mapToGrid(self.currentPos)
                if self.currentRectangle is None:
                    logger.info('Start drawing rectangle at %s', start)
                    self.currentRectangle = Rectangle(
                        None,
                        start=start,
                        penColour=self.selectedPenColour,
                        width=self.selectedWidth,
                        penStyle=self.selectedPenStyle,
                        penCapStyle=self.selectedPenCapStyle,
                        penJoinStyle=self.selectedPenJoinStyle,
                        brushColour=self.selectedBrushColour,
                        brushStyle=self.selectedBrushStyle)
                    add = Add(None, self.scene(), self.currentRectangle)
                    self.undoStack.push(add)
            else:
                if self.currentRectangle is not None:
                    self.currentRectangle.mouseReleaseEvent(event)
                logger.info('Finish drawing rectangle')
                self.statusbarMessage.emit('Left click to begin drawing a new rectangle (press ESC to cancel)', 0)
                self.currentRectangle = None
            for item in self.scene().selectedItems():
                item.setSelected(False)
        # If circle mode is on, add a new circle
        if self._keys['circle'] is True:
            if event.button() == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.statusbarMessage.emit('Left click to finish drawing the circle (press ESC to cancel)', 0)
                self.currentPos = event.pos()
                start = self.mapToGrid(self.currentPos)
                if self.currentCircle is None:
                    logger.info('Start drawing circle at %s', start)
                    self.currentCircle = Circle(
                        None,
                        start=start,
                        penColour=self.selectedPenColour,
                        width=self.selectedWidth,
                        penStyle=self.selectedPenStyle,
                        penCapStyle=self.selectedPenCapStyle,
                        penJoinStyle=self.selectedPenJoinStyle,
                        brushColour=self.selectedBrushColour,
                        brushStyle=self.selectedBrushStyle)
                    add = Add(None, self.scene(), self.currentCircle)
                    self.undoStack.push(add)
                    # self.scene().addItem(self.currentCircle)
            else:
                if self.currentCircle is not None:
                    self.currentCircle.mouseReleaseEvent(event)
                logger.info('Finish drawing circle')
                self.statusbarMessage.emit('Left click to begin drawing a new circle (press ESC to cancel)', 0)
                self.currentCircle = None
            for item in self.scene().selectedItems():
                item.setSelected(False)
        # If ellipse mode is on, add a new ellipse
        if self._keys['ellipse'] is True:
            if event.button() == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.statusbarMessage.emit('Left click to finish drawing the ellipse (press ESC to cancel)', 0)
                self.currentPos = event.pos()
                start = self.mapToGrid(self.currentPos)
                if self.currentEllipse is None:
                    logger.info('Start drawing ellipse at %s', start)
                    self.currentEllipse = Ellipse(
                        None,
                        start=start,
                        penColour=self.selectedPenColour,
                        width=self.selectedWidth,
                        penStyle=self.selectedPenStyle,
                        penCapStyle=self.selectedPenCapStyle,
                        penJoinStyle=self.selectedPenJoinStyle,
                        brushColour=self.selectedBrushColour,
                        brushStyle=self.selectedBrushStyle)
                    add = Add(None, self.scene(), self.currentEllipse)
                    self.undoStack.push(add)
                    # self.scene().addItem(self.currentEllipse)
            else:
                if self.currentEllipse is not None:
                    self.currentEllipse.mouseReleaseEvent(event)
                logger.info('Finish drawing ellipse')
                self.statusbarMessage.emit('Left click to begin drawing a new rectangle (press ESC to cancel)', 0)
                self.currentEllipse = None
            for item in self.scene().selectedItems():
                item.setSelected(False)
        # If textbox mode is on, add a new textbox
        if self._keys['textBox'] is True:
            if event.button() == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.currentPos = event.pos()
                start = self.mapToGrid(self.currentPos)
                logger.info('Draw text box at %s', start)
                if self.currentTextBox is None:
                    self.currentTextBox = TextBox(
                        None,
                        start=start,
                        penColour=self.selectedPenColour,
                        width=self.selectedWidth,
                        penStyle=self.selectedPenStyle,
                        penCapStyle=self.selectedPenCapStyle,
                        penJoinStyle=self.selectedPenJoinStyle,
                        brushColour=self.selectedBrushColour,
                        brushStyle=self.selectedBrushStyle,
                        font=self.selectedFont,
                        eulerFont=self.useEulerFontForLatex)
                    add = Add(None, self.scene(), self.currentTextBox)
                    self.undoStack.push(add)
                    # self.scene().addItem(self.currentTextBox)
                self._keys['textBox'] = False
                self._mouse['1'] = False
                self.statusbarMessage.emit('', 0)
                # Change cursor shape to a text editing style
                cursor = self.cursor()
                cursor.setShape(QtCore.Qt.ArrowCursor)
                self.setCursor(cursor)
            for item in self.scene().selectedItems():
                item.setSelected(False)
        # If image mode is on, add a new image
        if self._keys['image'] is True:
            if event.button() == QtCore.Qt.LeftButton:
                self._mouse['1'] = not self._mouse['1']
            if self._mouse['1'] is True:
                self.currentPos = event.pos()
                start = self.mapToGrid(self.currentPos)
                logger.info('Draw image at %s', start)
                if self.currentImage is None:
                    self.currentImage = Image(
                        None,
                        start=start)
                    add = Add(None, self.scene(), self.currentImage)
                    self.undoStack.push(add)
                self._keys['image'] = False
                self._mouse['1'] = False
                self.statusbarMessage.emit('', 0)
                # Change cursor shape to a text editing style
                cursor = self.cursor()
                cursor.setShape(QtCore.Qt.ArrowCursor)
                self.setCursor(cursor)
            for item in self.scene().selectedItems():
                item.setSelected(False)
        if self.selectOrigin is True:
            self.currentPos = event.pos()
            self.selectOrigin = False

    def mouseDoubleClickEvent(self, event):
        items = self.scene().selectedItems()
        if len(items) == 1:
            if isinstance(items[0], TextBox):
                items[0].lightenColour(False)
                oldTextBox = items[0].createCopy()
                oldTextBox.mouseDoubleClickEvent(event)
        if len(items) == 1:
            if isinstance(items[0], TextBox):
                if items[0].latexExpression == oldTextBox.latexExpression and\
                   items[0].toHtml() == oldTextBox.toHtml() and\
                   items[0].useEulerFont == oldTextBox.useEulerFont:
                    self.scene().removeItem(oldTextBox)
                else:
                    logger.info('Edited text box')
                    self.scene().removeItem(oldTextBox)
                    self.undoStack.beginMacro('')
                    add = Add(None, self.scene(), oldTextBox)
                    del_ = Delete(None, self.scene(), [items[0]])
                    self.undoStack.push(add)
                    self.undoStack.push(del_)
                    self.undoStack.endMacro()

    def mouseMoveEvent(self, event):
        super().mouseMoveEvent(event)
        self.currentPos = event.pos()
        self.updateMousePosLabel(self.currentPos)
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
                    self.currentNet.updateNet(self.mapToGrid(event.pos(), pin=True))
                if self._keys['arc'] is True:
                    if self.currentArc is not None:
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
                    # Check for circle before ellipse because circle is a subclass of ellipse
                    elif isinstance(item, Circle):
                        item.updateCircle(point)
                    elif isinstance(item, Ellipse):
                        item.updateEllipse(point, edit=True)
                    elif isinstance(item, Arc):
                        item.updateArc(point, edit=True)
                    elif isinstance(item, Wire):
                        item.updateWire(point, edit=True)
                    elif isinstance(item, Image):
                        item.updateImage(point, edit=True)

    # def contextMenuEvent(self, event):
    #     # TODO: Make this work properly
    #     menu = QtGui.QMenu()
    #     actionDelete = menu.addAction('&Delete')
    #     actionDelete.triggered.connect(lambda: self.scene().removeItem(self))
    #     menu.exec_(event.screenPos())

    def mapToGrid(self, point, pin=False):
        """Convenience function to map given point on to the grid"""
        point = self.mapToScene(point)
        if self._grid.snapToGrid is True:
            return self._grid.snapTo(point, pin=pin)
        else:
            return point

    def wheelEvent(self, event):
        """Handles mouse wheel interactions."""
        # Pan or zoom depending on keyboard modifiers
        eventDelta = event.angleDelta().y()
        if eventDelta >= 0:
            # Ignore event for fast scrolls where delta > 240
            if eventDelta > 240:
                event.ignore()
                return
            delta = max(120, eventDelta)
        elif eventDelta < 0:
            # Ignore event for fast scrolls where delta < -240
            if eventDelta < -240:
                event.ignore()
                return
            delta = min(-120, eventDelta)
        scaleFactor = -delta / 240.
        modifiers = QtWidgets.QApplication.keyboardModifiers()
        timeline = QtCore.QTimeLine(300, self)
        timeline.setFrameRange(0, 100)
        if modifiers == QtCore.Qt.ControlModifier:
            if self.scrollModifierCtrl == 'Zoom':
                panZoom = 'zoom'
            elif self.scrollModifierCtrl == 'Pan vertically':
                panZoom = 'vertical'
            elif self.scrollModifierCtrl == 'Pan horizontally':
                panZoom = 'horizontal'
        elif modifiers == QtCore.Qt.ShiftModifier:
            if self.scrollModifierShift == 'Zoom':
                panZoom = 'zoom'
            elif self.scrollModifierShift == 'Pan vertically':
                panZoom = 'vertical'
            elif self.scrollModifierShift == 'Pan horizontally':
                panZoom = 'horizontal'
        else:
            if self.scrollModifierNone == 'Zoom':
                panZoom = 'zoom'
            elif self.scrollModifierNone == 'Pan vertically':
                panZoom = 'vertical'
            elif self.scrollModifierNone == 'Pan horizontally':
                panZoom = 'horizontal'
        if panZoom in ['vertical', 'horizontal']:
            self.setTransformationAnchor(self.NoAnchor)
            if self.showAnimationPan is True:
                timeline.setUpdateInterval(20)
                timeline.frameChanged.connect(lambda: self.modifyView(scaleFactor, panZoom))
            else:
                self.modifyView(scaleFactor*15, panZoom)
            logger.debug('Pan in the %s direction by %d', panZoom, -scaleFactor*150)
        else:
            if self.invertZoom is False:
                if scaleFactor < 0:
                    scaleFactor = -1 / scaleFactor
            else:
                if scaleFactor > 0:
                    scaleFactor = 1 / scaleFactor
                else:
                    scaleFactor = -scaleFactor
            scaleFactor = 1 + (scaleFactor - 1) / 2.5
            self.setTransformationAnchor(self.AnchorUnderMouse)
            if self.showAnimationZoom is True:
                timeline.setDuration(100)
                timeline.setUpdateInterval(20)
                scaleFactor = scaleFactor**(1/5)
                timeline.frameChanged.connect(lambda: self.modifyView(scaleFactor, panZoom))
            else:
                self.modifyView(scaleFactor, panZoom)
            logger.debug('Viewport scaled by %.2f', scaleFactor)
        timeline.start()

    def modifyView(self, scaleFactor, panZoom='vertical'):
        """Convenience function for handling panning/zooming"""
        if panZoom == 'vertical':
            self.translate(0, -scaleFactor * 10)
        elif panZoom == 'horizontal':
            self.translate(-scaleFactor*10, 0)
        elif panZoom == 'zoom':
            self.scale(scaleFactor, scaleFactor)

    def editShape(self):
        """Convenience function for handling the editing of shapes."""
        # Only process this if edit mode is not already active
        if self._keys['edit'] is False:
            if len(self.scene().selectedItems()) == 1:
                logger.info('Begin editing')
                item = self.scene().selectedItems()[0]
                self.ensureVisible(item)
                cursor = self.cursor()
                if isinstance(item, Circle):
                    sceneP = item.mapToScene(item.end.toPoint())
                    self.statusbarMessage.emit('Left click to place the current vertex here and finish editing (press ESC to cancel)', 0)
                elif isinstance(item, Rectangle) or isinstance(item, Ellipse):
                    sceneP = item.mapToScene(item.p2).toPoint()
                    self.statusbarMessage.emit('Left click to place the current vertex here and finish editing (press ESC to cancel)', 0)
                elif isinstance(item, Image):
                    sceneP = item.sceneBoundingRect().bottomRight().toPoint()
                    self.statusbarMessage.emit('Left click to finish resizing the image (press ESC to cancel)', 0)
                elif isinstance(item, Wire):
                    # poly = item.oldPath.toSubpathPolygons(item.transform())[0]
                    # item.editPointNumber = poly.size() - 1
                    item.editPointNumber = 0
                    sceneP = item.mapToScene(item.editPointLocation(item.editPointNumber))
                    self.statusbarMessage.emit('Left click to place the current vertex here and move to the next vertex (press ESC to cancel)', 0)
                else:
                    self.statusbarMessage.emit("The selected item cannot be edited", 2000)
                    return
                viewP = self.mapFromScene(sceneP)
                cursor.setPos(self.viewport().mapToGlobal(viewP))
                self.editStartPoint = sceneP
                self.undoStack.beginMacro('')
                self._keys['edit'], self._mouse['1'] = True, True
                edit = Edit(None, self.scene(), item, self.editStartPoint)
                self.undoStack.push(edit)
                # Adjust cursor if the item is a wire
                if isinstance(item, Wire):
                    viewP = self.mapFromScene(item.mapToScene(item.editPointLocation(item.editPointNumber)))
                    cursor.setPos(self.viewport().mapToGlobal(viewP))
            else:
                self.statusbarMessage.emit("Please select an item to edit", 2000)

    def optionsRoutine(self):
        """Convenience function that creates the options box and then applies
        any changes needed."""
        self.optionswindow = MyOptionsWindow(self, self.settingsFileName)
        self.optionswindow.applied.connect(lambda:self.applySettingsFromFile(self.settingsFileName))
        self.optionswindow.finished.connect(lambda:self.applySettingsFromFile(self.settingsFileName))
        self.optionswindow.exec_()

    def updateMousePosLabel(self, pos=None):
        """Updates the current mouse position."""
        if pos is None:
            return
        gridPos = self.mapToGrid(pos)
        text = "Current position: "
        text += '(%s, %s)' %(gridPos.x(), gridPos.y())
        self.mousePosLabel.setText(text)
        if self.showMouseRect is True:
            if self._keys['net'] is True:
                pinPos = self.mapToGrid(pos, pin=True)
            else:
                pinPos = gridPos
            self.mouseRect.setPos(pinPos)

    def groupItems(self, mode='group'):
        """Groups or ungroups selected items depending on mode."""
        listOfItems = self.scene().selectedItems()
        if listOfItems == []:
            return
        if mode == 'ungroup' and len(listOfItems) > 1:
            self.statusbarMessage.emit('Please select only one item to ungroup', 2000)
            return
        if mode == 'group' and len(listOfItems) == 1:
            self.statusbarMessage.emit('Please select at least two items to group', 2000)
            return
        if mode == 'group':
            group = Group(None, self.scene(), listOfItems)
            self.undoStack.push(group)
        if mode == 'ungroup':
            if isinstance(listOfItems[0], myGraphicsItemGroup):
                ungroup = Ungroup(None, self.scene(), listOfItems[0])
                self.undoStack.push(ungroup)
            else:
                self.statusbarMessage.emit('Selected instance needs to be a group/symbol', 2000)
