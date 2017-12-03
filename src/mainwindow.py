import sys
sys.path.append('./Resources/icons/')
from .drawingarea import DrawingArea
from .components import TextBox, myGraphicsItemGroup
from .drawingitems import myIconProvider
from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork
from .gui.ycircuit_mainWindow import Ui_MainWindow
import zipfile
import os, shutil
import logging


class myMainWindow(QtWidgets.QMainWindow):
    def __init__(self, clipboard=None):
        self.logger = logging.getLogger('YCircuit.MainWindow')
        self.logger.info('Creating a new schematic window')

        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap('./Resources/icon.jpg'))
        self.setWindowIcon(icon)
        self.ui.drawingArea.applySettingsFromFile('.config')

        self.ui.drawingArea.mousePosLabel = QtWidgets.QLabel()
        self.ui.statusbar.addPermanentWidget(self.ui.drawingArea.mousePosLabel)
        self.downloader = QtNetwork.QNetworkAccessManager()
        self.downloader.setConfiguration(QtNetwork.QNetworkConfigurationManager().defaultConfiguration())
        if self.downloader.networkAccessible() != self.downloader.NotAccessible:
            self.ui.action_updateYCircuit.setEnabled(True)
        self.logger.info('Accessibility reported to be %d', self.downloader.networkAccessible())
        if clipboard is not None:
            self.clipboard = clipboard
            self.ui.drawingArea.clipboard = clipboard

        # Connect actions to relevant slots
        # File menu
        self.ui.action_newSchematic.triggered.connect(
            self.action_newSchematic_triggered)
        self.ui.action_saveSchematic.triggered.connect(
            lambda x: self.ui.drawingArea.saveRoutine('schematic'))
        self.ui.action_saveSchematicAs.triggered.connect(
            lambda x: self.ui.drawingArea.saveRoutine('schematicAs'))
        self.ui.action_loadSchematic.triggered.connect(
            lambda x: self.ui.drawingArea.loadRoutine('schematic'))
        self.ui.action_loadSchematic.triggered.connect(
            lambda x: self.changeWindowTitle(True))
        self.ui.action_saveSymbol.triggered.connect(
            lambda x: self.ui.drawingArea.saveRoutine('symbol'))
        self.ui.action_saveSymbolAs.triggered.connect(
            lambda x: self.ui.drawingArea.saveRoutine('symbolAs'))
        self.ui.action_loadSymbol.triggered.connect(
            lambda x: self.ui.drawingArea.loadRoutine('symbol'))
        self.ui.action_modifySymbol.triggered.connect(
            lambda x: self.ui.drawingArea.loadRoutine('symbolModify'))
        self.ui.action_modifySymbol.triggered.connect(
            lambda x: self.changeWindowTitle(True))
        self.ui.action_importImage.triggered.connect(
            lambda: self.ui.drawingArea.addImage())
        self.ui.action_exportFile.triggered.connect(
            self.ui.drawingArea.exportRoutine)
        self.ui.action_quit.triggered.connect(self.close)

        # Edit menu
        self.ui.action_undo.triggered.connect(
            self.ui.drawingArea.undoStack.undo)
        self.ui.action_undo.triggered.connect(
            lambda x: self.ui.statusbar.showMessage("Undo", 1000))
        self.ui.action_redo.triggered.connect(
            self.ui.drawingArea.undoStack.redo)
        self.ui.action_redo.triggered.connect(
            lambda x: self.ui.statusbar.showMessage("Redo", 1000))
        self.ui.drawingArea.undoStack.canRedoChanged.connect(
            self.ui.action_redo.setEnabled)
        self.ui.drawingArea.undoStack.canUndoChanged.connect(
            self.ui.action_undo.setEnabled)
        self.ui.action_rotate.triggered.connect(
            self.ui.drawingArea.rotateRoutine)
        self.ui.action_mirror.triggered.connect(
            lambda x:self.ui.drawingArea.rotateRoutine(modifier=QtCore.Qt.ShiftModifier))
        self.ui.action_move.triggered.connect(
            self.ui.drawingArea.moveRoutine)
        self.ui.action_copy.triggered.connect(
            self.ui.drawingArea.copyRoutine)
        self.ui.action_paste.triggered.connect(
            self.ui.drawingArea.pasteRoutine)
        self.ui.action_delete.triggered.connect(
            self.ui.drawingArea.deleteRoutine)
        self.ui.action_pickFont.triggered.connect(
            self.action_pickFont_triggered)
        self.ui.action_options.triggered.connect(
            self.ui.drawingArea.optionsRoutine)
        self.ui.action_escape.triggered.connect(
            self.ui.drawingArea.escapeRoutine)

        self.ui.action_heightBringForward.triggered.connect(
            lambda x: self.ui.drawingArea.changeHeightRoutine('forward'))
        self.ui.action_heightSendBack.triggered.connect(
            lambda x: self.ui.drawingArea.changeHeightRoutine('back'))
        self.ui.action_heightReset.triggered.connect(
            lambda x: self.ui.drawingArea.changeHeightRoutine('reset'))

        self.ui.action_group.triggered.connect(
            lambda x: self.ui.drawingArea.groupItems('group'))
        self.ui.action_ungroup.triggered.connect(
            lambda x: self.ui.drawingArea.groupItems('ungroup'))

        self.ui.menu_Edit.hovered.connect(self.menu_Edit_hovered)
        self.ui.action_setWidth2.triggered.connect(
            lambda x: self.action_setWidth_triggered(2))
        self.ui.action_setWidth4.triggered.connect(
            lambda x: self.action_setWidth_triggered(4))
        self.ui.action_setWidth6.triggered.connect(
            lambda x: self.action_setWidth_triggered(6))
        self.ui.action_setWidth8.triggered.connect(
            lambda x: self.action_setWidth_triggered(8))
        self.ui.action_setWidth10.triggered.connect(
            lambda x: self.action_setWidth_triggered(10))
        self.ui.action_setWidthCustom.triggered.connect(
            lambda x: self.action_setWidth_triggered('custom'))

        self.ui.action_setPenColourBlack.triggered.connect(
            lambda x: self.action_setPenColour_triggered('black'))
        self.ui.action_setPenColourRed.triggered.connect(
            lambda x: self.action_setPenColour_triggered('red'))
        self.ui.action_setPenColourGreen.triggered.connect(
            lambda x: self.action_setPenColour_triggered('green'))
        self.ui.action_setPenColourBlue.triggered.connect(
            lambda x: self.action_setPenColour_triggered('blue'))
        self.ui.action_setPenColourCyan.triggered.connect(
            lambda x: self.action_setPenColour_triggered('cyan'))
        self.ui.action_setPenColourMagenta.triggered.connect(
            lambda x: self.action_setPenColour_triggered('magenta'))
        self.ui.action_setPenColourYellow.triggered.connect(
            lambda x: self.action_setPenColour_triggered('yellow'))
        self.ui.action_setPenColourCustom.triggered.connect(
            lambda x: self.action_setPenColour_triggered('custom'))

        self.ui.action_setPenStyleSolid.triggered.connect(
            lambda x: self.action_setPenStyle_triggered(1))
        self.ui.action_setPenStyleDash.triggered.connect(
            lambda x: self.action_setPenStyle_triggered(2))
        self.ui.action_setPenStyleDot.triggered.connect(
            lambda x: self.action_setPenStyle_triggered(3))
        self.ui.action_setPenStyleDashDot.triggered.connect(
            lambda x: self.action_setPenStyle_triggered(4))
        self.ui.action_setPenStyleDashDotDot.triggered.connect(
            lambda x: self.action_setPenStyle_triggered(5))

        self.ui.action_setPenCapStyleSquare.triggered.connect(
            lambda x: self.action_setPenCapStyle_triggered(0x10))
        self.ui.action_setPenCapStyleRound.triggered.connect(
            lambda x: self.action_setPenCapStyle_triggered(0x20))
        self.ui.action_setPenCapStyleFlat.triggered.connect(
            lambda x: self.action_setPenCapStyle_triggered(0x00))

        self.ui.action_setPenJoinStyleRound.triggered.connect(
            lambda x: self.action_setPenJoinStyle_triggered(0x80))
        self.ui.action_setPenJoinStyleMiter.triggered.connect(
            lambda x: self.action_setPenJoinStyle_triggered(0x00))
        self.ui.action_setPenJoinStyleBevel.triggered.connect(
            lambda x: self.action_setPenJoinStyle_triggered(0x40))

        self.ui.action_setBrushColourBlack.triggered.connect(
            lambda x: self.action_setBrushColour_triggered('black'))
        self.ui.action_setBrushColourRed.triggered.connect(
            lambda x: self.action_setBrushColour_triggered('red'))
        self.ui.action_setBrushColourGreen.triggered.connect(
            lambda x: self.action_setBrushColour_triggered('green'))
        self.ui.action_setBrushColourBlue.triggered.connect(
            lambda x: self.action_setBrushColour_triggered('blue'))
        self.ui.action_setBrushColourCyan.triggered.connect(
            lambda x: self.action_setBrushColour_triggered('cyan'))
        self.ui.action_setBrushColourMagenta.triggered.connect(
            lambda x: self.action_setBrushColour_triggered('magenta'))
        self.ui.action_setBrushColourYellow.triggered.connect(
            lambda x: self.action_setBrushColour_triggered('yellow'))
        self.ui.action_setBrushColourCustom.triggered.connect(
            lambda x: self.action_setBrushColour_triggered('custom'))

        self.ui.action_setBrushStyleNone.triggered.connect(
            lambda x: self.action_setBrushStyle_triggered(0))
        self.ui.action_setBrushStyleSolid.triggered.connect(
            lambda x: self.action_setBrushStyle_triggered(1))

        # View menu
        self.ui.menu_View.hovered.connect(self.menu_View_hovered)
        self.ui.action_fitToView.triggered.connect(
            self.ui.drawingArea.fitToViewRoutine)
        self.ui.action_showPins.triggered.connect(
            self.ui.drawingArea.togglePinsRoutine)
        self.ui.action_snapNetToPin.triggered.connect(
            self.ui.drawingArea.toggleSnapNetToPinRoutine)
        self.ui.action_showGrid.triggered.connect(
            self.ui.drawingArea.toggleGridRoutine)
        self.ui.action_snapToGrid.triggered.connect(
            self.ui.drawingArea.toggleSnapToGridRoutine)
        self.ui.action_snapToGridSpacing1.triggered.connect(
            lambda x: self.action_snapToGridSpacing(1))
        self.ui.action_snapToGridSpacing2.triggered.connect(
            lambda x: self.action_snapToGridSpacing(2))
        self.ui.action_snapToGridSpacing5.triggered.connect(
            lambda x: self.action_snapToGridSpacing(5))
        self.ui.action_snapToGridSpacing10.triggered.connect(
            lambda x: self.action_snapToGridSpacing(10))
        self.ui.action_snapToGridSpacing20.triggered.connect(
            lambda x: self.action_snapToGridSpacing(20))
        self.ui.action_snapToGridSpacing30.triggered.connect(
            lambda x: self.action_snapToGridSpacing(30))
        self.ui.action_snapToGridSpacing40.triggered.connect(
            lambda x: self.action_snapToGridSpacing(40))
        self.ui.action_showMajorGridPoints.triggered.connect(
            self.ui.drawingArea.toggleMajorGridPointsRoutine)
        self.ui.action_majorGridPointSpacing100.triggered.connect(
            lambda x: self.action_majorGridPointSpacing(100))
        self.ui.action_majorGridPointSpacing200.triggered.connect(
            lambda x: self.action_majorGridPointSpacing(200))
        self.ui.action_majorGridPointSpacing300.triggered.connect(
            lambda x: self.action_majorGridPointSpacing(300))
        self.ui.action_majorGridPointSpacing400.triggered.connect(
            lambda x: self.action_majorGridPointSpacing(400))
        self.ui.action_showMinorGridPoints.triggered.connect(
            self.ui.drawingArea.toggleMinorGridPointsRoutine)
        self.ui.action_minorGridPointSpacing1.triggered.connect(
            lambda x: self.action_minorGridPointSpacing(1))
        self.ui.action_minorGridPointSpacing2.triggered.connect(
            lambda x: self.action_minorGridPointSpacing(2))
        self.ui.action_minorGridPointSpacing5.triggered.connect(
            lambda x: self.action_minorGridPointSpacing(5))
        self.ui.action_minorGridPointSpacing10.triggered.connect(
            lambda x: self.action_minorGridPointSpacing(10))
        self.ui.action_minorGridPointSpacing20.triggered.connect(
            lambda x: self.action_minorGridPointSpacing(20))
        self.ui.action_minorGridPointSpacing30.triggered.connect(
            lambda x: self.action_minorGridPointSpacing(30))
        self.ui.action_minorGridPointSpacing40.triggered.connect(
            lambda x: self.action_minorGridPointSpacing(40))

        # Shape menu
        self.ui.action_addLine.triggered.connect(self.ui.drawingArea.addWire)
        self.ui.action_addArc3Point.triggered.connect(
            lambda x: self.ui.drawingArea.addArc(3))
        self.ui.action_addArc4Point.triggered.connect(
            lambda x: self.ui.drawingArea.addArc(4))
        self.ui.action_addRectangle.triggered.connect(
            self.ui.drawingArea.addRectangle)
        self.ui.action_addCircle.triggered.connect(
            self.ui.drawingArea.addCircle)
        self.ui.action_addEllipse.triggered.connect(
            self.ui.drawingArea.addEllipse)
        self.ui.action_addTextBox.triggered.connect(
            self.ui.drawingArea.addTextBox)
        self.ui.action_addImage.triggered.connect(
            self.ui.drawingArea.addImage)
        self.ui.action_editShape.triggered.connect(
            self.ui.drawingArea.editShape)

        # Symbol menu
        self.ui.action_addPin.triggered.connect(self.ui.drawingArea.addPin)
        self.ui.action_addWire.triggered.connect(self.ui.drawingArea.addNet)
        self.ui.action_addResistor.triggered.connect(
            self.ui.drawingArea.addResistor)
        self.ui.action_addCapacitor.triggered.connect(
            self.ui.drawingArea.addCapacitor)
        self.ui.action_addGround.triggered.connect(
            self.ui.drawingArea.addGround)
        self.ui.action_addDot.triggered.connect(self.ui.drawingArea.addDot)
        self.ui.action_addNMOSWithArrow.triggered.connect(
            lambda x: self.ui.drawingArea.addTransistor('MOS', 'N', True))
        self.ui.action_addNMOSWithoutArrow.triggered.connect(
            lambda x: self.ui.drawingArea.addTransistor('MOS', 'N', False))
        self.ui.action_addPMOSWithArrow.triggered.connect(
            lambda x: self.ui.drawingArea.addTransistor('MOS', 'P', True))
        self.ui.action_addPMOSWithoutArrow.triggered.connect(
            lambda x: self.ui.drawingArea.addTransistor('MOS', 'P', False))
        self.ui.action_addNPNBJT.triggered.connect(
            lambda x: self.ui.drawingArea.addTransistor('BJT', 'N', True))
        self.ui.action_addPNPBJT.triggered.connect(
            lambda x: self.ui.drawingArea.addTransistor('BJT', 'P', True))
        self.ui.action_addDCVoltageSource.triggered.connect(
            lambda x: self.ui.drawingArea.addSource('DCV'))
        self.ui.action_addDCCurrentSource.triggered.connect(
            lambda x: self.ui.drawingArea.addSource('DCI'))
        self.ui.action_addACSource.triggered.connect(
            lambda x: self.ui.drawingArea.addSource('AC'))
        self.ui.action_addVCVS.triggered.connect(
            lambda x: self.ui.drawingArea.addSource('VCVS'))
        self.ui.action_addVCCS.triggered.connect(
            lambda x: self.ui.drawingArea.addSource('VCCS'))
        self.ui.action_addCCVS.triggered.connect(
            lambda x: self.ui.drawingArea.addSource('CCVS'))
        self.ui.action_addCCCS.triggered.connect(
            lambda x: self.ui.drawingArea.addSource('CCCS'))
        self.ui.action_quickAddSymbol1.triggered.connect(
            lambda x: self.ui.drawingArea.quickAddSymbol(1))
        self.ui.action_quickAddSymbol2.triggered.connect(
            lambda x: self.ui.drawingArea.quickAddSymbol(2))
        self.ui.action_quickAddSymbol3.triggered.connect(
            lambda x: self.ui.drawingArea.quickAddSymbol(3))
        self.ui.action_quickAddSymbol4.triggered.connect(
            lambda x: self.ui.drawingArea.quickAddSymbol(4))
        self.ui.action_quickAddSymbol5.triggered.connect(
            lambda x: self.ui.drawingArea.quickAddSymbol(5))

        # Help menu
        self.ui.action_updateYCircuit.triggered.connect(
            self.updateYCircuit)
        self.ui.action_tutorialInverterSchematic.triggered.connect(
            lambda x: QtGui.QDesktopServices.openUrl(
                QtCore.QUrl(
                'https://siddharthshekar.bitbucket.io/YCircuit/Tutorial/1/tutorial1.html')))
        self.ui.action_tutorialCustomSymbols.triggered.connect(
            lambda x: QtGui.QDesktopServices.openUrl(
                QtCore.QUrl(
                'https://siddharthshekar.bitbucket.io/YCircuit/Tutorial/2/tutorial2.html')))

        # Miscellaneous signal and slot connections
        self.ui.drawingArea.undoStack.cleanChanged.connect(self.changeWindowTitle)
        self.ui.drawingArea.statusbarMessage.connect(self.ui.statusbar.showMessage)

        # Initialize the symbol viewer
        self.initialiseSymbolViewer()
        self.logger.info('Successfully created a new window')

    def changeWindowTitle(self, clean=True):
        if self.ui.drawingArea.schematicFileName is not None:
            fileName = self.ui.drawingArea.schematicFileName
            self.setWindowTitle('YCircuit - ' + fileName)
            if clean is False:
                self.setWindowTitle(self.windowTitle() + '*')
        elif self.ui.drawingArea.symbolFileName is not None:
            fileName = self.ui.drawingArea.symbolFileName
            self.setWindowTitle('YCircuit - ' + fileName)
            if clean is False:
                self.setWindowTitle(self.windowTitle() + '*')
        self.logger.info('Window title set to %s', self.windowTitle())

    def closeEvent(self, event):
        modified = ''
        if sys.exc_info()[0] != None:
            self.logger.error(exc_info=sys.exc_info())
        if self.ui.drawingArea.undoStack.isClean():
            self.ui.drawingArea.autobackupFile.close()
            self.ui.drawingArea.autobackupFile.remove()
            self.logger.info('Closing with a clean undo stack')
            event.accept()
        elif self.ui.drawingArea.schematicFileName is not None:
            modified = 'schematic'
        elif self.ui.drawingArea.symbolFileName is not None:
            modified = 'symbol'
        else:
            modified = 'schematic'
        if modified != '':
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setWindowTitle("Confirm exit")
            msgBox.setText("The " + modified + " has been modified")
            msgBox.setInformativeText("Do you wish to save your changes?")
            msgBox.setStandardButtons(msgBox.Save | msgBox.Discard | msgBox.Cancel)
            msgBox.setDefaultButton(msgBox.Save)
            msgBox.setIcon(msgBox.Information)
            ret = msgBox.exec_()
            if ret == msgBox.Save:
                self.ui.drawingArea.saveRoutine(modified)
                self.logger.info('Deleting autobackup file %s', self.ui.drawingArea.autobackupFile.fileName())
                self.ui.drawingArea.autobackupFile.close()
                self.ui.drawingArea.autobackupFile.remove()
                self.logger.info('Closing with changes saved as %s', modified)
                event.accept()
            elif ret == msgBox.Discard:
                self.logger.info('Deleting autobackup file %s', self.ui.drawingArea.autobackupFile.fileName())
                self.ui.drawingArea.autobackupFile.close()
                self.ui.drawingArea.autobackupFile.remove()
                self.logger.info('Closing with unsaved changes')
                event.accept()
            else:
                event.ignore()

    def action_newSchematic_triggered(self):
        self.logger.info('Creating a new window')
        if self.ui.drawingArea.schematicFileName is None and self.ui.drawingArea.symbolFileName is None:
            msgBox = QtWidgets.QMessageBox(self)
            msgBox.setText("Please save the current window with a new name first")
            msgBox.setStandardButtons(msgBox.Ok)
            msgBox.exec_()
            return
        self.form = myMainWindow(self.clipboard)
        self.form.showMaximized()
        self.form.ui.drawingArea.fitToViewRoutine()

    def action_pickFont_triggered(self):
        fontList = []
        for item in self.ui.drawingArea.scene().selectedItems():
            if not isinstance(item, TextBox):
                fontList = []
                break
            else:
                fontList.append(item.font().toString())
        if fontList != [] and len(set(fontList)) == 1:
            initialFont = QtGui.QFont()
            initialFont.fromString(fontList[0])
        elif hasattr(self.ui.drawingArea, 'selectedFont'):
            initialFont = self.ui.drawingArea.selectedFont
        else:
            initialFont = QtGui.QFont('Arial', 10)
        (font, accept) = QtWidgets.QFontDialog.getFont(initialFont, parent=self)
        if accept is True:
            self.logger.info('Changing font to %s %d', font.family(), font.pointSize())
            self.ui.drawingArea.changeFontRoutine(font)

    def menu_Edit_hovered(self):
        widthList = []
        penColourList = []
        penStyleList = []
        penCapStyleList = []
        penJoinStyleList = []
        brushColourList = []
        brushStyleList = []
        for item in self.ui.drawingArea.scene().selectedItems():
            if not isinstance(item, TextBox):
                widthList.append(item.localPenWidth)
                penCapStyleList.append(item.localPenCapStyle)
                penJoinStyleList.append(item.localPenJoinStyle)
            penColourList.append(item.localPenColour)
            penStyleList.append(item.localPenStyle)
            brushColourList.append(item.localBrushColour)
            brushStyleList.append(item.localBrushStyle)

        # This will fail if the datatypes are unhashable (QColor, for example)
        try:
            set(widthList)
            set(penColourList)
            set(penStyleList)
            set(penCapStyleList)
            set(penJoinStyleList)
            set(brushColourList)
            set(brushStyleList)
        except:
            return

        if len(set(widthList)) == 1:
            self.action_setWidth_triggered(widthList[0], temporary=True)
        elif len(set(widthList)) > 1:
            self.action_setWidth_triggered(-1, temporary=True)
        elif len(set(widthList)) == 0:
            self.action_setWidth_triggered(self.ui.drawingArea.selectedWidth, temporary=True)

        if len(set(penColourList)) == 1:
            self.action_setPenColour_triggered(penColourList[0], temporary=True)
        elif len(set(penColourList)) > 1:
            self.action_setPenColour_triggered(-1, temporary=True)
        elif len(set(penColourList)) == 0:
            self.action_setPenColour_triggered(self.ui.drawingArea.selectedPenColour, temporary=True)

        if len(set(penStyleList)) == 1:
            self.action_setPenStyle_triggered(penStyleList[0], temporary=True)
        elif len(set(penStyleList)) > 1:
            self.action_setPenStyle_triggered(-1, temporary=True)
        elif len(set(penStyleList)) == 0:
            self.action_setPenStyle_triggered(self.ui.drawingArea.selectedPenStyle, temporary=True)

        if len(set(penCapStyleList)) == 1:
            self.action_setPenCapStyle_triggered(penCapStyleList[0], temporary=True)
        elif len(set(penCapStyleList)) > 1:
            self.action_setPenCapStyle_triggered(-1, temporary=True)
        elif len(set(penCapStyleList)) == 0:
            self.action_setPenCapStyle_triggered(self.ui.drawingArea.selectedPenCapStyle, temporary=True)

        if len(set(penJoinStyleList)) == 1:
            self.action_setPenJoinStyle_triggered(penJoinStyleList[0], temporary=True)
        elif len(set(penJoinStyleList)) > 1:
            self.action_setPenJoinStyle_triggered(-1, temporary=True)
        elif len(set(penJoinStyleList)) == 0:
            self.action_setPenJoinStyle_triggered(self.ui.drawingArea.selectedPenJoinStyle, temporary=True)

        if len(set(brushColourList)) == 1:
            self.action_setBrushColour_triggered(brushColourList[0], temporary=True)
        elif len(set(brushColourList)) > 1:
            self.action_setBrushColour_triggered(-1, temporary=True)
        elif len(set(brushColourList)) == 0:
            self.action_setBrushColour_triggered(self.ui.drawingArea.selectedBrushColour, temporary=True)

        if len(set(brushStyleList)) == 1:
            self.action_setBrushStyle_triggered(brushStyleList[0], temporary=True)
        elif len(set(brushStyleList)) > 1:
            self.action_setBrushStyle_triggered(-1, temporary=True)
        elif len(set(brushStyleList)) == 0:
            self.action_setBrushStyle_triggered(self.ui.drawingArea.selectedBrushStyle, temporary=True)

    def action_setWidth_triggered(self, width, temporary=False):
        self.ui.action_setWidth2.setChecked(False)
        self.ui.action_setWidth4.setChecked(False)
        self.ui.action_setWidth6.setChecked(False)
        self.ui.action_setWidth8.setChecked(False)
        self.ui.action_setWidth10.setChecked(False)
        self.ui.action_setWidthCustom.setChecked(False)
        if width == 2:
            self.ui.action_setWidth2.setChecked(True)
        if width == 4:
            self.ui.action_setWidth4.setChecked(True)
        if width == 6:
            self.ui.action_setWidth6.setChecked(True)
        if width == 8:
            self.ui.action_setWidth8.setChecked(True)
        if width == 10:
            self.ui.action_setWidth10.setChecked(True)
        if width == 'custom':
            selectedItems = self.ui.drawingArea.scene().selectedItems()
            oldWidth = self.ui.drawingArea.selectedWidth
            if len(selectedItems) == 1:
                item = selectedItems[0]
                if not isinstance(item, myGraphicsItemGroup):
                    if not isinstance(item, TextBox):
                        oldWidth = item.localPenWidth
            width, accept = QtWidgets.QInputDialog.getInt(
                self,
                'Set custom pen width',
                'Width',
                oldWidth,
                1,
                100)
            if accept is False:
                return
            self.ui.action_setWidthCustom.setChecked(True)
        if temporary is False:
            self.logger.info('Set pen width to %d', width)
            self.ui.drawingArea.changeWidthRoutine(width)

    def action_setPenColour_triggered(self, penColour, temporary=False):
        self.ui.action_setPenColourBlack.setChecked(False)
        self.ui.action_setPenColourRed.setChecked(False)
        self.ui.action_setPenColourGreen.setChecked(False)
        self.ui.action_setPenColourBlue.setChecked(False)
        self.ui.action_setPenColourCyan.setChecked(False)
        self.ui.action_setPenColourMagenta.setChecked(False)
        self.ui.action_setPenColourYellow.setChecked(False)
        self.ui.action_setPenColourCustom.setChecked(False)
        # This will fail if the colour is not a string (hex colours, for example)
        try:
            penColour = penColour.lower()
        except:
            return
        if penColour == 'black':
            self.ui.action_setPenColourBlack.setChecked(True)
        elif penColour == 'red':
            self.ui.action_setPenColourRed.setChecked(True)
        elif penColour == 'green':
            self.ui.action_setPenColourGreen.setChecked(True)
        elif penColour == 'blue':
            self.ui.action_setPenColourBlue.setChecked(True)
        elif penColour == 'cyan':
            self.ui.action_setPenColourCyan.setChecked(True)
        elif penColour == 'magenta':
            self.ui.action_setPenColourMagenta.setChecked(True)
        elif penColour == 'yellow':
            self.ui.action_setPenColourYellow.setChecked(True)
        elif penColour == 'custom':
            penColour = QtWidgets.QColorDialog().getColor(parent=self)
            self.ui.action_setPenColourCustom.setChecked(True)
        if temporary is False:
            if QtGui.QColor(penColour).isValid():
                self.logger.info('Set pen colour to %s', QtGui.QColor(penColour).name())
                self.ui.drawingArea.changePenColourRoutine(penColour)

    def action_setPenStyle_triggered(self, penStyle, temporary=False):
        self.ui.action_setPenStyleSolid.setChecked(False)
        self.ui.action_setPenStyleDash.setChecked(False)
        self.ui.action_setPenStyleDot.setChecked(False)
        self.ui.action_setPenStyleDashDot.setChecked(False)
        self.ui.action_setPenStyleDashDotDot.setChecked(False)
        if penStyle == 1:
            self.ui.action_setPenStyleSolid.setChecked(True)
        if penStyle == 2:
            self.ui.action_setPenStyleDash.setChecked(True)
        if penStyle == 3:
            self.ui.action_setPenStyleDot.setChecked(True)
        if penStyle == 4:
            self.ui.action_setPenStyleDashDot.setChecked(True)
        if penStyle == 5:
            self.ui.action_setPenStyleDashDotDot.setChecked(True)
        if temporary is False:
            self.logger.info('Set pen style to %d', penStyle)
            self.ui.drawingArea.changePenStyleRoutine(penStyle)

    def action_setPenCapStyle_triggered(self, penCapStyle, temporary=False):
        self.ui.action_setPenCapStyleSquare.setChecked(False)
        self.ui.action_setPenCapStyleRound.setChecked(False)
        self.ui.action_setPenCapStyleFlat.setChecked(False)
        if penCapStyle == 0x10:
            self.ui.action_setPenCapStyleSquare.setChecked(True)
        if penCapStyle == 0x20:
            self.ui.action_setPenCapStyleRound.setChecked(True)
        if penCapStyle == 0x00:
            self.ui.action_setPenCapStyleFlat.setChecked(True)
        if temporary is False:
            self.logger.info('Set pen cap style to %d', penCapStyle)
            self.ui.drawingArea.changePenCapStyleRoutine(penCapStyle)

    def action_setPenJoinStyle_triggered(self, penJoinStyle, temporary=False):
        self.ui.action_setPenJoinStyleRound.setChecked(False)
        self.ui.action_setPenJoinStyleMiter.setChecked(False)
        self.ui.action_setPenJoinStyleBevel.setChecked(False)
        if penJoinStyle == 0x80:
            self.ui.action_setPenJoinStyleRound.setChecked(True)
        if penJoinStyle == 0x00:
            self.ui.action_setPenJoinStyleMiter.setChecked(True)
        if penJoinStyle == 0x40:
            self.ui.action_setPenJoinStyleBevel.setChecked(True)
        if temporary is False:
            self.logger.info('Set pen join style to %d', penJoinStyle)
            self.ui.drawingArea.changePenJoinStyleRoutine(penJoinStyle)

    def action_setBrushColour_triggered(self, brushColour, temporary=False):
        self.ui.action_setBrushColourBlack.setChecked(False)
        self.ui.action_setBrushColourRed.setChecked(False)
        self.ui.action_setBrushColourGreen.setChecked(False)
        self.ui.action_setBrushColourBlue.setChecked(False)
        self.ui.action_setBrushColourCyan.setChecked(False)
        self.ui.action_setBrushColourMagenta.setChecked(False)
        self.ui.action_setBrushColourYellow.setChecked(False)
        self.ui.action_setBrushColourCustom.setChecked(False)
        # This will fail if the colour is not a string (hex colours, for example)
        try:
            brushColour = brushColour.lower()
        except:
            return
        if brushColour == 'black':
            self.ui.action_setBrushColourBlack.setChecked(True)
        elif brushColour == 'red':
            self.ui.action_setBrushColourRed.setChecked(True)
        elif brushColour == 'green':
            self.ui.action_setBrushColourGreen.setChecked(True)
        elif brushColour == 'blue':
            self.ui.action_setBrushColourBlue.setChecked(True)
        elif brushColour == 'cyan':
            self.ui.action_setBrushColourCyan.setChecked(True)
        elif brushColour == 'magenta':
            self.ui.action_setBrushColourMagenta.setChecked(True)
        elif brushColour == 'yellow':
            self.ui.action_setBrushColourYellow.setChecked(True)
        elif brushColour == 'custom':
            brushColour = QtWidgets.QColorDialog().getColor(parent=self)
            self.ui.action_setBrushColourCustom.setChecked(True)
        if temporary is False:
            if QtGui.QColor(brushColour).isValid():
                self.logger.info('Set brush colour to %s', QtGui.QColor(brushColour).name())
                self.ui.drawingArea.changeBrushColourRoutine(brushColour)

    def action_setBrushStyle_triggered(self, brushStyle, temporary=False):
        self.ui.action_setBrushStyleNone.setChecked(False)
        self.ui.action_setBrushStyleSolid.setChecked(False)
        if brushStyle == 0:
            self.ui.action_setBrushStyleNone.setChecked(True)
        if brushStyle == 1:
            self.ui.action_setBrushStyleSolid.setChecked(True)
        if temporary is False:
            self.logger.info('Set brush style to %d', brushStyle)
            self.ui.drawingArea.changeBrushStyleRoutine(brushStyle)

    def menu_View_hovered(self):
        self.ui.action_showGrid.setChecked(
            self.ui.drawingArea._grid.enableGrid)
        self.ui.action_snapToGrid.setChecked(
            self.ui.drawingArea._grid.snapToGrid)
        self.ui.action_showMajorGridPoints.setChecked(
            self.ui.drawingArea._grid.majorSpacingVisibility)
        self.ui.action_showMinorGridPoints.setChecked(
            self.ui.drawingArea._grid.minorSpacingVisibility)

        # Set the snap to grid spacing check appropriately
        snapToGridSpacing = self.ui.drawingArea._grid.snapToGridSpacing
        self.action_snapToGridSpacing(snapToGridSpacing, temporary=True)
        # Set the major and minor grid point checks appropriately
        majorSpacing = self.ui.drawingArea._grid.majorSpacing
        minorSpacing = self.ui.drawingArea._grid.minorSpacing
        self.action_majorGridPointSpacing(majorSpacing, temporary=True)
        self.action_minorGridPointSpacing(minorSpacing, temporary=True)

    def action_snapToGridSpacing(self, spacing, temporary=False):
        self.ui.action_snapToGridSpacing1.setChecked(False)
        self.ui.action_snapToGridSpacing2.setChecked(False)
        self.ui.action_snapToGridSpacing5.setChecked(False)
        self.ui.action_snapToGridSpacing10.setChecked(False)
        self.ui.action_snapToGridSpacing20.setChecked(False)
        self.ui.action_snapToGridSpacing30.setChecked(False)
        self.ui.action_snapToGridSpacing40.setChecked(False)
        if spacing == 1:
            self.ui.action_snapToGridSpacing1.setChecked(True)
        if spacing == 2:
            self.ui.action_snapToGridSpacing2.setChecked(True)
        if spacing == 5:
            self.ui.action_snapToGridSpacing5.setChecked(True)
        if spacing == 10:
            self.ui.action_snapToGridSpacing10.setChecked(True)
        if spacing == 20:
            self.ui.action_snapToGridSpacing20.setChecked(True)
        if spacing == 30:
            self.ui.action_snapToGridSpacing30.setChecked(True)
        if spacing == 40:
            self.ui.action_snapToGridSpacing40.setChecked(True)
        if temporary is False:
            self.logger.info('Set snap to grid spacing to %d', spacing)
            self.ui.drawingArea.changeSnapToGridSpacing(spacing)

    def action_majorGridPointSpacing(self, spacing, temporary=False):
        self.ui.action_majorGridPointSpacing100.setChecked(False)
        self.ui.action_majorGridPointSpacing200.setChecked(False)
        self.ui.action_majorGridPointSpacing300.setChecked(False)
        self.ui.action_majorGridPointSpacing400.setChecked(False)
        if spacing == 100:
            self.ui.action_majorGridPointSpacing100.setChecked(True)
        if spacing == 200:
            self.ui.action_majorGridPointSpacing200.setChecked(True)
        if spacing == 300:
            self.ui.action_majorGridPointSpacing300.setChecked(True)
        if spacing == 400:
            self.ui.action_majorGridPointSpacing400.setChecked(True)
        if temporary is False:
            self.logger.info('Set major grid point spacing to %d', spacing)
            self.ui.drawingArea.changeMajorGridPointSpacing(spacing)

    def action_minorGridPointSpacing(self, spacing, temporary=False):
        self.ui.action_minorGridPointSpacing1.setChecked(False)
        self.ui.action_minorGridPointSpacing2.setChecked(False)
        self.ui.action_minorGridPointSpacing5.setChecked(False)
        self.ui.action_minorGridPointSpacing10.setChecked(False)
        self.ui.action_minorGridPointSpacing20.setChecked(False)
        self.ui.action_minorGridPointSpacing30.setChecked(False)
        self.ui.action_minorGridPointSpacing40.setChecked(False)
        if spacing == 1:
            self.ui.action_minorGridPointSpacing1.setChecked(True)
        if spacing == 2:
            self.ui.action_minorGridPointSpacing2.setChecked(True)
        if spacing == 5:
            self.ui.action_minorGridPointSpacing5.setChecked(True)
        if spacing == 10:
            self.ui.action_minorGridPointSpacing10.setChecked(True)
        if spacing == 20:
            self.ui.action_minorGridPointSpacing20.setChecked(True)
        if spacing == 30:
            self.ui.action_minorGridPointSpacing30.setChecked(True)
        if spacing == 40:
            self.ui.action_minorGridPointSpacing40.setChecked(True)
        if temporary is False:
            self.logger.info('Set minor grid point spacing to %d', spacing)
            self.ui.drawingArea.changeMinorGridPointSpacing(spacing)

    def initialiseSymbolViewer(self):
        # Create a new file picker when the symbol directory toolbutton
        # is triggered
        self.ui.menu_symbolPreviewFolderPicker = QtWidgets.QMenu(self.ui.toolButton_symbolPreviewFolder)
        self.ui.action_symbolPreviewFolderDefault = QtWidgets.QAction('Default', self)
        self.ui.action_symbolPreviewFolderStandard = QtWidgets.QAction('Standard', self)
        self.ui.action_symbolPreviewFolderCustom = QtWidgets.QAction('Custom', self)
        self.ui.action_symbolPreviewFolder1 = QtWidgets.QAction('Folder 1', self)
        self.ui.action_symbolPreviewFolder2 = QtWidgets.QAction('Folder 2', self)
        self.ui.action_symbolPreviewFolder3 = QtWidgets.QAction('Folder 3', self)
        self.ui.menu_symbolPreviewFolderPicker.addAction(self.ui.action_symbolPreviewFolderStandard)
        self.ui.menu_symbolPreviewFolderPicker.addAction(self.ui.action_symbolPreviewFolderCustom)
        self.ui.menu_symbolPreviewFolderPicker.addAction(self.ui.action_symbolPreviewFolder1)
        self.ui.menu_symbolPreviewFolderPicker.addAction(self.ui.action_symbolPreviewFolder2)
        self.ui.menu_symbolPreviewFolderPicker.addAction(self.ui.action_symbolPreviewFolder3)
        self.ui.menu_symbolPreviewFolderPicker.addSeparator()
        self.ui.menu_symbolPreviewFolderPicker.addAction(self.ui.action_symbolPreviewFolderDefault)
        self.ui.toolButton_symbolPreviewFolder.setMenu(
            self.ui.menu_symbolPreviewFolderPicker)
        self.ui.toolButton_symbolPreviewFolder.clicked.connect(
            lambda x: self.pickSymbolPreviewDirectory())
        self.ui.action_symbolPreviewFolderDefault.triggered.connect(
            lambda x: self.pickSymbolPreviewDirectory(self.ui.drawingArea.defaultSymbolPreviewFolder))
        self.ui.action_symbolPreviewFolderStandard.triggered.connect(
            lambda x: self.pickSymbolPreviewDirectory('Resources/Symbols/Standard'))
        self.ui.action_symbolPreviewFolderCustom.triggered.connect(
            lambda x: self.pickSymbolPreviewDirectory('Resources/Symbols/Custom'))
        self.ui.action_symbolPreviewFolder1.triggered.connect(
            lambda x: self.pickSymbolPreviewDirectory(self.ui.drawingArea.symbolPreviewFolder1))
        self.ui.action_symbolPreviewFolder2.triggered.connect(
            lambda x: self.pickSymbolPreviewDirectory(self.ui.drawingArea.symbolPreviewFolder2))
        self.ui.action_symbolPreviewFolder3.triggered.connect(
            lambda x: self.pickSymbolPreviewDirectory(self.ui.drawingArea.symbolPreviewFolder3))
        # Connecting the symbol viewer to the appropriate model
        self.fileSystemModel = QtWidgets.QFileSystemModel()
        if hasattr(self.ui.drawingArea, 'defaultSymbolPreviewFolder'):
            index = self.fileSystemModel.setRootPath(self.ui.drawingArea.defaultSymbolPreviewFolder)
        else:
            index = self.fileSystemModel.setRootPath('./Resources/Symbols/Standard/')
        self.logger.info('Initialising symbol viewer directory to %s', self.fileSystemModel.rootPath())
        self.fileSystemModel.setIconProvider(myIconProvider())
        self.fileSystemModel.setNameFilterDisables(False)
        self.fileSystemModel.setNameFilters(['*.sym'])
        self.ui.listView_symbolPreview.setModel(self.fileSystemModel)
        self.ui.listView_symbolPreview.setRootIndex(index)
        self.ui.listView_symbolPreview.setIconSize(QtCore.QSize(100, 100))
        # Set double click behaviour in the list view
        self.ui.listView_symbolPreview.doubleClicked.connect(
            self.ui.drawingArea.escapeRoutine)
        self.ui.listView_symbolPreview.doubleClicked.connect(
            self.ui.drawingArea.setFocus)
        self.ui.listView_symbolPreview.doubleClicked.connect(
            lambda x: self.ui.drawingArea.loadRoutine(
                mode='symbol',
                loadFile=self.fileSystemModel.filePath(x)))
        # Set shortcut for the search filter
        shortcut = QtWidgets.QShortcut(QtGui.QKeySequence('Ctrl+F'), self)
        shortcut.activated.connect(self.ui.lineEdit_symbolPreviewFilter.selectAll)
        shortcut.activated.connect(self.ui.lineEdit_symbolPreviewFilter.setFocus)
        self.ui.lineEdit_symbolPreviewFilter.textChanged.connect(
            lambda: self.fileSystemModel.setNameFilters(
                ['*' + self.ui.lineEdit_symbolPreviewFilter.text() + '*.sym']
            )
        )

    def pickSymbolPreviewDirectory(self, dir_=None):
        if dir_ is None:
            dir_ = QtWidgets.QFileDialog().getExistingDirectory(
                self,
                'Pick directory for symbol preview',
                self.fileSystemModel.rootPath())
        if dir_ != '':
            index = self.fileSystemModel.setRootPath(dir_)
            self.ui.listView_symbolPreview.setRootIndex(index)
            self.logger.info('Set symbol viewer directory to %s', dir_)

    def updateYCircuit(self):
        # For some reason, when building on Windows, networkAccessible returns
        # unknown accessibility. Hence, instead of explicitly checking for
        # accessibility, we instead check for lack thereof
        if self.downloader.networkAccessible() == self.downloader.NotAccessible:
            self.ui.statusbar.showMessage('Please make sure you are connected to the internet', 1000)
            self.logger.info('Did not download update becase of lack of network access')
            return
        branch, accept = QtWidgets.QInputDialog.getItem(
            self,
            'Update',
            'Select branch to update from',
            ['master', 'develop'],
            1,
            False)
        if accept is False:
            return
        url = 'https://bitbucket.org/siddharthshekar/ycircuit/downloads/'
        if sys.platform == 'linux':
            self.updateFile = 'ycircuit-' + branch + '_linux64_update.zip'
        elif sys.platform == 'win32':
            self.updateFile = 'ycircuit-' + branch + '_win64_update.zip'
        url += self.updateFile
        loop = QtCore.QEventLoop()
        request = QtNetwork.QNetworkRequest(QtCore.QUrl(url))
        data = self.downloader.get(request)
        self.downloader.finished.connect(self.processDownloadedUpdate)
        self.downloader.finished.connect(loop.exit)
        self.ui.statusbar.showMessage('Downloading update', 0)
        self.logger.info('Downloading update from %s', branch)
        loop.exec_()

    def processDownloadedUpdate(self, data):
        statusCode = data.attribute(QtNetwork.QNetworkRequest.HttpStatusCodeAttribute)
        print(statusCode)
        # Handle redirects
        if statusCode == 302:
            url = data.attribute((QtNetwork.QNetworkRequest.RedirectionTargetAttribute))
            print('Redirecting to', url)
            self.logger.info('Redirected to %s', url.toDisplayString())
            request = QtNetwork.QNetworkRequest(url)
            data = self.downloader.get(request)
            return
        # Handle file not found error
        elif statusCode == 404:
            self.ui.statusbar.showMessage('Could not download the update', 1000)
            self.logger.info('Could not download the update')
            print('Update could not be downloaded')
            self.downloader.disconnect()
            return
        self.ui.statusbar.showMessage('Installing update', 0)
        self.logger.info('Installing update')
        if sys.platform == 'linux':
            self.logger.info('Renaming current executable to YCircuit_old')
            os.replace('./YCircuit', './YCircuit_old')
        elif sys.platform == 'win32':
            self.logger.info('Renaming current executable to YCircuit_old.exe')
            os.replace('./YCircuit.exe', './YCircuit_old.exe')
        with open(self.updateFile, 'wb') as f:
            f.write(data.readAll())
        with zipfile.ZipFile(self.updateFile, 'r', zipfile.ZIP_DEFLATED) as zip:
            self.logger.info('Unzipping update files')
            zip.extractall('./')
            if sys.platform == 'linux':
                shutil.copymode('./YCircuit_old', './YCircuit')
        self.ui.statusbar.showMessage('Update completed', 1000)
        self.logger.info('Update completed')
        self.downloader.disconnect()
