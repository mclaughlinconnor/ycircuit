import sys
sys.path.append('./Resources/icons/')
from src.drawingarea import DrawingArea
from PyQt4 import QtCore, QtGui
from src.gui.ycircuit_mainWindow import Ui_MainWindow
import platform
import sip


class myMainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(myMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect actions to relevant slots
        # File menu
        self.ui.action_saveSchematic.triggered.connect(lambda x: self.ui.drawingArea.saveRoutine('schematic'))
        self.ui.action_saveSchematicAs.triggered.connect(lambda x: self.ui.drawingArea.saveRoutine('schematicAs'))
        self.ui.action_loadSchematic.triggered.connect(lambda x: self.ui.drawingArea.loadRoutine('schematic'))
        self.ui.action_loadSchematic.triggered.connect(lambda x: self.changeWindowTitle(True))
        self.ui.action_saveSymbol.triggered.connect(lambda x: self.ui.drawingArea.saveRoutine('symbol'))
        self.ui.action_loadSymbol.triggered.connect(lambda x: self.ui.drawingArea.loadRoutine('symbol'))
        self.ui.action_modifySymbol.triggered.connect(lambda x: self.ui.drawingArea.loadRoutine('symbolModify'))
        self.ui.action_modifySymbol.triggered.connect(lambda x: self.changeWindowTitle(True))
        self.ui.action_exportFile.triggered.connect(self.ui.drawingArea.exportRoutine)
        self.ui.action_quit.triggered.connect(self.close)

        # Edit menu
        self.ui.action_undo.triggered.connect(self.ui.drawingArea.undoStack.undo)
        self.ui.action_undo.triggered.connect(lambda x: self.ui.statusbar.showMessage("Undo", 1000))
        self.ui.action_redo.triggered.connect(self.ui.drawingArea.undoStack.redo)
        self.ui.action_redo.triggered.connect(lambda x: self.ui.statusbar.showMessage("Redo", 1000))
        self.ui.drawingArea.undoStack.canRedoChanged.connect(self.ui.action_redo.setEnabled)
        self.ui.drawingArea.undoStack.canUndoChanged.connect(self.ui.action_undo.setEnabled)
        self.ui.action_rotate.triggered.connect(self.ui.drawingArea.rotateRoutine)
        self.ui.action_mirror.triggered.connect(lambda x:self.ui.drawingArea.rotateRoutine(modifier=QtCore.Qt.ShiftModifier))
        self.ui.action_move.triggered.connect(self.ui.drawingArea.moveRoutine)
        self.ui.action_copy.triggered.connect(self.ui.drawingArea.copyRoutine)
        self.ui.action_delete.triggered.connect(self.ui.drawingArea.deleteRoutine)
        self.ui.drawingArea.resetToolbarButtons.connect(lambda: self.ui.action_move.setChecked(False))
        self.ui.drawingArea.resetToolbarButtons.connect(lambda: self.ui.action_copy.setChecked(False))
        self.ui.drawingArea.resetToolbarButtons.connect(lambda: self.ui.action_delete.setChecked(False))

        self.ui.menu_Edit.hovered.connect(self.menu_Edit_hovered)
        self.ui.action_setWidth2.triggered.connect(lambda x:self.action_setWidth_triggered(2))
        self.ui.action_setWidth4.triggered.connect(lambda x:self.action_setWidth_triggered(4))
        self.ui.action_setWidth6.triggered.connect(lambda x:self.action_setWidth_triggered(6))
        self.ui.action_setWidth8.triggered.connect(lambda x:self.action_setWidth_triggered(8))
        self.ui.action_setWidth10.triggered.connect(lambda x:self.action_setWidth_triggered(10))

        self.ui.action_setPenColourBlack.triggered.connect(lambda x: self.action_setPenColour_triggered('black'))
        self.ui.action_setPenColourRed.triggered.connect(lambda x: self.action_setPenColour_triggered('red'))
        self.ui.action_setPenColourGreen.triggered.connect(lambda x: self.action_setPenColour_triggered('green'))
        self.ui.action_setPenColourBlue.triggered.connect(lambda x: self.action_setPenColour_triggered('blue'))
        self.ui.action_setPenColourCyan.triggered.connect(lambda x: self.action_setPenColour_triggered('cyan'))
        self.ui.action_setPenColourMagenta.triggered.connect(lambda x: self.action_setPenColour_triggered('magenta'))
        self.ui.action_setPenColourYellow.triggered.connect(lambda x: self.action_setPenColour_triggered('yellow'))

        self.ui.action_setPenStyleSolid.triggered.connect(lambda x: self.action_setPenStyle_triggered(1))
        self.ui.action_setPenStyleDash.triggered.connect(lambda x: self.action_setPenStyle_triggered(2))
        self.ui.action_setPenStyleDot.triggered.connect(lambda x: self.action_setPenStyle_triggered(3))
        self.ui.action_setPenStyleDashDot.triggered.connect(lambda x: self.action_setPenStyle_triggered(4))
        self.ui.action_setPenStyleDashDotDot.triggered.connect(lambda x: self.action_setPenStyle_triggered(5))

        self.ui.action_setBrushColourBlack.triggered.connect(lambda x: self.action_setBrushColour_triggered('black'))
        self.ui.action_setBrushColourRed.triggered.connect(lambda x: self.action_setBrushColour_triggered('red'))
        self.ui.action_setBrushColourGreen.triggered.connect(lambda x: self.action_setBrushColour_triggered('green'))
        self.ui.action_setBrushColourBlue.triggered.connect(lambda x: self.action_setBrushColour_triggered('blue'))
        self.ui.action_setBrushColourCyan.triggered.connect(lambda x: self.action_setBrushColour_triggered('cyan'))
        self.ui.action_setBrushColourMagenta.triggered.connect(lambda x: self.action_setBrushColour_triggered('magenta'))
        self.ui.action_setBrushColourYellow.triggered.connect(lambda x: self.action_setBrushColour_triggered('yellow'))

        self.ui.action_setBrushStyleNone.triggered.connect(lambda x: self.action_setBrushStyle_triggered(0))
        self.ui.action_setBrushStyleSolid.triggered.connect(lambda x: self.action_setBrushStyle_triggered(1))

        # View menu
        self.ui.action_fitToView.triggered.connect(self.ui.drawingArea.fitToViewRoutine)
        self.ui.action_showGrid.triggered.connect(self.ui.drawingArea.toggleGridRoutine)
        self.ui.action_snapToGrid.triggered.connect(self.ui.drawingArea.toggleSnapToGridRoutine)

        # Shape menu
        self.ui.action_addLine.triggered.connect(self.ui.drawingArea.addWire)
        self.ui.action_addArc3Point.triggered.connect(lambda x: self.ui.drawingArea.addArc(3))
        self.ui.action_addArc4Point.triggered.connect(lambda x: self.ui.drawingArea.addArc(4))
        self.ui.action_addRectangle.triggered.connect(self.ui.drawingArea.addRectangle)
        self.ui.action_addCircle.triggered.connect(self.ui.drawingArea.addCircle)
        self.ui.action_addEllipse.triggered.connect(self.ui.drawingArea.addEllipse)
        self.ui.action_addTextBox.triggered.connect(self.ui.drawingArea.addTextBox)
        self.ui.action_editShape.triggered.connect(self.ui.drawingArea.editShape)

        # Symbol menu
        self.ui.action_addWire.triggered.connect(self.ui.drawingArea.addWire)
        self.ui.action_addResistor.triggered.connect(self.ui.drawingArea.addResistor)
        self.ui.action_addCapacitor.triggered.connect(self.ui.drawingArea.addCapacitor)
        self.ui.action_addGround.triggered.connect(self.ui.drawingArea.addGround)
        self.ui.action_addDot.triggered.connect(self.ui.drawingArea.addDot)
        self.ui.action_addNMOSWithArrow.triggered.connect(lambda x: self.ui.drawingArea.addTransistor('MOS', 'N', True))
        self.ui.action_addNMOSWithoutArrow.triggered.connect(lambda x: self.ui.drawingArea.addTransistor('MOS', 'N', False))
        self.ui.action_addPMOSWithArrow.triggered.connect(lambda x: self.ui.drawingArea.addTransistor('MOS', 'P', True))
        self.ui.action_addPMOSWithoutArrow.triggered.connect(lambda x: self.ui.drawingArea.addTransistor('MOS', 'P', False))
        self.ui.action_addNPNBJT.triggered.connect(lambda x: self.ui.drawingArea.addTransistor('BJT', 'N', True))
        self.ui.action_addPNPBJT.triggered.connect(lambda x: self.ui.drawingArea.addTransistor('BJT', 'P', True))
        self.ui.action_addDCVoltageSource.triggered.connect(lambda x: self.ui.drawingArea.addSource('DCV'))
        self.ui.action_addDCCurrentSource.triggered.connect(lambda x: self.ui.drawingArea.addSource('DCI'))
        self.ui.action_addACSource.triggered.connect(lambda x: self.ui.drawingArea.addSource('AC'))
        self.ui.action_addVCVS.triggered.connect(lambda x: self.ui.drawingArea.addSource('VCVS'))
        self.ui.action_addVCCS.triggered.connect(lambda x: self.ui.drawingArea.addSource('VCCS'))
        self.ui.action_addCCVS.triggered.connect(lambda x: self.ui.drawingArea.addSource('CCVS'))
        self.ui.action_addCCCS.triggered.connect(lambda x: self.ui.drawingArea.addSource('CCCS'))

        # Miscellaneous signal and slot connections
        self.ui.drawingArea.undoStack.cleanChanged.connect(self.changeWindowTitle)
        self.ui.drawingArea.statusbarMessage.connect(self.ui.statusbar.showMessage)

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

    def closeEvent(self, event):
        if self.ui.drawingArea.undoStack.isClean():
            event.accept()
        elif self.ui.drawingArea.schematicFileName is None:
            msgBox = QtGui.QMessageBox(self)
            msgBox.setText("The schematic has been modified")
            msgBox.setInformativeText("Do you wish to save your changes?")
            msgBox.setStandardButtons(msgBox.Save | msgBox.Discard | msgBox.Cancel)
            msgBox.setDefaultButton(msgBox.Save)
            msgBox.setIcon(msgBox.Information)
            ret = msgBox.exec_()
            if ret == msgBox.Save:
                self.ui.drawingArea.saveRoutine('schematic')
                event.accept()
            elif ret == msgBox.Discard:
                event.accept()
            else:
                event.ignore()
        elif self.ui.drawingArea.symbolFileName is None:
            msgBox = QtGui.QMessageBox(self)
            msgBox.setText("The symbol has been modified")
            msgBox.setInformativeText("Do you wish to save your changes?")
            msgBox.setStandardButtons(msgBox.Save | msgBox.Discard | msgBox.Cancel)
            msgBox.setDefaultButton(msgBox.Save)
            msgBox.setIcon(msgBox.Information)
            ret = msgBox.exec_()
            if ret == msgBox.Save:
                self.ui.drawingArea.saveRoutine('symbol')
                event.accept()
            elif ret == msgBox.Discard:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()

    def menu_Edit_hovered(self):
        widthList = []
        penColourList = []
        penStyleList = []
        brushColourList = []
        brushStyleList = []
        for item in self.ui.drawingArea.scene().selectedItems():
            widthList.append(item.localPenWidth)
            penColourList.append(item.localPenColour)
            penStyleList.append(item.localPenStyle)
            brushColourList.append(item.localBrushColour)
            brushStyleList.append(item.localBrushStyle)

        if len(set(widthList)) == 1:
            self.action_setWidth_triggered(widthList[0], temporary=True)
        elif len(set(widthList)) > 1:
            self.action_setWidth_triggered(-1, temporary=True)
        elif len(set(widthList)) == 0:
            self.action_setWidth_triggered(self.ui.drawingArea.selectedWidth)

        if len(set(penColourList)) == 1:
            self.action_setPenColour_triggered(penColourList[0], temporary=True)
        elif len(set(penColourList)) > 1:
            self.action_setPenColour_triggered(-1, temporary=True)
        elif len(set(penColourList)) == 0:
            self.action_setPenColour_triggered(self.ui.drawingArea.selectedPenColour)

        if len(set(penStyleList)) == 1:
            self.action_setPenStyle_triggered(penStyleList[0], temporary=True)
        elif len(set(penStyleList)) > 1:
            self.action_setPenStyle_triggered(-1, temporary=True)
        elif len(set(penStyleList)) == 0:
            self.action_setPenStyle_triggered(self.ui.drawingArea.selectedPenStyle)

        if len(set(brushColourList)) == 1:
            self.action_setBrushColour_triggered(brushColourList[0], temporary=True)
        elif len(set(brushColourList)) > 1:
            self.action_setBrushColour_triggered(-1, temporary=True)
        elif len(set(brushColourList)) == 0:
            self.action_setBrushColour_triggered(self.ui.drawingArea.selectedBrushColour)

        if len(set(brushStyleList)) == 1:
            self.action_setBrushStyle_triggered(brushStyleList[0], temporary=True)
        elif len(set(brushStyleList)) > 1:
            self.action_setBrushStyle_triggered(-1, temporary=True)
        elif len(set(brushStyleList)) == 0:
            self.action_setBrushStyle_triggered(self.ui.drawingArea.selectedBrushStyle)

    def action_setWidth_triggered(self, width, temporary=False):
        self.ui.action_setWidth2.setChecked(False)
        self.ui.action_setWidth4.setChecked(False)
        self.ui.action_setWidth6.setChecked(False)
        self.ui.action_setWidth8.setChecked(False)
        self.ui.action_setWidth10.setChecked(False)
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
        if temporary is False:
            self.ui.drawingArea.changeWidthRoutine(width)

    def action_setPenColour_triggered(self, penColour, temporary=False):
        self.ui.action_setPenColourBlack.setChecked(False)
        self.ui.action_setPenColourRed.setChecked(False)
        self.ui.action_setPenColourGreen.setChecked(False)
        self.ui.action_setPenColourBlue.setChecked(False)
        self.ui.action_setPenColourCyan.setChecked(False)
        self.ui.action_setPenColourMagenta.setChecked(False)
        self.ui.action_setPenColourYellow.setChecked(False)
        if penColour == 'black':
            self.ui.action_setPenColourBlack.setChecked(True)
        if penColour == 'red':
            self.ui.action_setPenColourRed.setChecked(True)
        if penColour == 'green':
            self.ui.action_setPenColourGreen.setChecked(True)
        if penColour == 'blue':
            self.ui.action_setPenColourBlue.setChecked(True)
        if penColour == 'cyan':
            self.ui.action_setPenColourCyan.setChecked(True)
        if penColour == 'magenta':
            self.ui.action_setPenColourMagenta.setChecked(True)
        if penColour == 'yellow':
            self.ui.action_setPenColourYellow.setChecked(True)
        if temporary is False:
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
            self.ui.drawingArea.changePenStyleRoutine(penStyle)

    def action_setBrushColour_triggered(self, brushColour, temporary=False):
        self.ui.action_setBrushColourBlack.setChecked(False)
        self.ui.action_setBrushColourRed.setChecked(False)
        self.ui.action_setBrushColourGreen.setChecked(False)
        self.ui.action_setBrushColourBlue.setChecked(False)
        self.ui.action_setBrushColourCyan.setChecked(False)
        self.ui.action_setBrushColourMagenta.setChecked(False)
        self.ui.action_setBrushColourYellow.setChecked(False)
        if brushColour == 'black':
            self.ui.action_setBrushColourBlack.setChecked(True)
        if brushColour == 'red':
            self.ui.action_setBrushColourRed.setChecked(True)
        if brushColour == 'green':
            self.ui.action_setBrushColourGreen.setChecked(True)
        if brushColour == 'blue':
            self.ui.action_setBrushColourBlue.setChecked(True)
        if brushColour == 'cyan':
            self.ui.action_setBrushColourCyan.setChecked(True)
        if brushColour == 'magenta':
            self.ui.action_setBrushColourMagenta.setChecked(True)
        if brushColour == 'yellow':
            self.ui.action_setBrushColourYellow.setChecked(True)
        if temporary is False:
            self.ui.drawingArea.changeBrushColourRoutine(brushColour)

    def action_setBrushStyle_triggered(self, brushStyle, temporary=False):
        self.ui.action_setBrushStyleNone.setChecked(False)
        self.ui.action_setBrushStyleSolid.setChecked(False)
        if brushStyle == 0:
            self.ui.action_setBrushStyleNone.setChecked(True)
        if brushStyle == 1:
            self.ui.action_setBrushStyleSolid.setChecked(True)
        if temporary is False:
            self.ui.drawingArea.changeBrushStyleRoutine(brushStyle)


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    form = myMainWindow()
    form.showMaximized()
    form.ui.drawingArea.fitToViewRoutine()
    if platform.system() == 'Windows':
        sip.setdestroyonexit(False)
    app.exec_()
