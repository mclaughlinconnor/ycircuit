from drawingarea import DrawingArea
from PyQt4 import QtCore, QtGui
from schematic_mainWindow import Ui_MainWindow
import sys
import sip


class myMainWindow(QtGui.QMainWindow):

    def __init__(self):
        super(myMainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect actions to relevant slots
        self.ui.action_saveSchematic.triggered.connect(lambda x: self.ui.drawingArea.saveRoutine('schematic'))
        self.ui.action_loadSchematic.triggered.connect(lambda x: self.ui.drawingArea.loadRoutine('schematic'))
        self.ui.action_saveSymbol.triggered.connect(lambda x: self.ui.drawingArea.saveRoutine('symbol'))
        self.ui.action_loadSymbol.triggered.connect(lambda x: self.ui.drawingArea.loadRoutine('symbol'))
        self.ui.action_exportFile.triggered.connect(lambda x: self.ui.drawingArea.saveRoutine('export'))
        self.ui.action_quit.triggered.connect(self.close)
        self.ui.action_rotate.triggered.connect(self.ui.drawingArea.rotateRoutine)
        self.ui.action_mirror.triggered.connect(lambda x:self.ui.drawingArea.rotateRoutine(modifier=QtCore.Qt.ShiftModifier))
        self.ui.action_move.triggered.connect(self.ui.drawingArea.moveRoutine)
        self.ui.action_copy.triggered.connect(self.ui.drawingArea.copyRoutine)
        self.ui.action_delete.triggered.connect(self.ui.drawingArea.deleteRoutine)

        self.ui.action_addWire.triggered.connect(self.ui.drawingArea.addWire)
        self.ui.action_addResistor.triggered.connect(self.ui.drawingArea.addResistor)
        self.ui.action_addCapacitor.triggered.connect(self.ui.drawingArea.addCapacitor)
        self.ui.action_addGround.triggered.connect(self.ui.drawingArea.addGround)
        self.ui.action_addDot.triggered.connect(self.ui.drawingArea.addDot)
        self.ui.action_addNMOSWithArrow.triggered.connect(lambda x: self.ui.drawingArea.addTransistor('MOS', 'N', True))
        self.ui.action_addNMOSWithoutArrow.triggered.connect(lambda x: self.ui.drawingArea.addTransistor('MOS', 'N', False))
        self.ui.action_addPMOSWithArrow.triggered.connect(lambda x: self.ui.drawingArea.addTransistor('MOS', 'P', True))
        self.ui.action_addPMOSWithoutArrow.triggered.connect(lambda x: self.ui.drawingArea.addTransistor('MOS', 'P', False))

        self.ui.action_fitToView.triggered.connect(self.ui.drawingArea.fitToViewRoutine)
        self.ui.action_showGrid.setChecked(True)
        self.ui.action_showGrid.triggered.connect(self.ui.drawingArea.toggleGridRoutine)

        self.ui.menu_Edit.hovered.connect(self.menu_Edit_hovered)
        self.ui.action_setWidth2.triggered.connect(lambda x:self.action_setWidth_triggered(2))
        self.ui.action_setWidth2.setChecked(True)
        self.ui.action_setWidth4.triggered.connect(lambda x:self.action_setWidth_triggered(4))
        self.ui.action_setWidth6.triggered.connect(lambda x:self.action_setWidth_triggered(6))
        self.ui.action_setWidth8.triggered.connect(lambda x:self.action_setWidth_triggered(8))
        self.ui.action_setWidth10.triggered.connect(lambda x:self.action_setWidth_triggered(10))

        self.ui.action_setPenColourBlack.triggered.connect(lambda x: self.action_setPenColour_triggered('black'))
        self.ui.action_setPenColourBlack.setChecked(True)
        self.ui.action_setPenColourRed.triggered.connect(lambda x: self.action_setPenColour_triggered('red'))
        self.ui.action_setPenColourGreen.triggered.connect(lambda x: self.action_setPenColour_triggered('green'))
        self.ui.action_setPenColourBlue.triggered.connect(lambda x: self.action_setPenColour_triggered('blue'))

        self.ui.action_setPenStyleSolid.triggered.connect(lambda x: self.action_setPenStyle_triggered(1))
        self.ui.action_setPenStyleSolid.setChecked(True)
        self.ui.action_setPenStyleDash.triggered.connect(lambda x: self.action_setPenStyle_triggered(2))
        self.ui.action_setPenStyleDot.triggered.connect(lambda x: self.action_setPenStyle_triggered(3))
        self.ui.action_setPenStyleDashDot.triggered.connect(lambda x: self.action_setPenStyle_triggered(4))
        self.ui.action_setPenStyleDashDotDot.triggered.connect(lambda x: self.action_setPenStyle_triggered(5))

        self.ui.action_setBrushColourBlack.triggered.connect(lambda x: self.action_setBrushColour_triggered('black'))
        self.ui.action_setBrushColourBlack.setChecked(True)
        self.ui.action_setBrushColourRed.triggered.connect(lambda x: self.action_setBrushColour_triggered('red'))
        self.ui.action_setBrushColourGreen.triggered.connect(lambda x: self.action_setBrushColour_triggered('green'))
        self.ui.action_setBrushColourBlue.triggered.connect(lambda x: self.action_setBrushColour_triggered('blue'))

        self.ui.action_setBrushStyleNone.triggered.connect(lambda x: self.action_setBrushStyle_triggered(0))
        self.ui.action_setBrushStyleNone.setChecked(True)
        self.ui.action_setBrushStyleSolid.triggered.connect(lambda x: self.action_setBrushStyle_triggered(1))

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
        if penColour == 'black':
            self.ui.action_setPenColourBlack.setChecked(True)
        if penColour == 'red':
            self.ui.action_setPenColourRed.setChecked(True)
        if penColour == 'green':
            self.ui.action_setPenColourGreen.setChecked(True)
        if penColour == 'blue':
            self.ui.action_setPenColourBlue.setChecked(True)
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
        if brushColour == 'black':
            self.ui.action_setBrushColourBlack.setChecked(True)
        if brushColour == 'red':
            self.ui.action_setBrushColourRed.setChecked(True)
        if brushColour == 'green':
            self.ui.action_setBrushColourGreen.setChecked(True)
        if brushColour == 'blue':
            self.ui.action_setBrushColourBlue.setChecked(True)
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
    sip.setdestroyonexit(False)
    app.exec_()
