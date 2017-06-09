# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\src\gui\ycircuit_mainWindow.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(1089, 790)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("../../Resources/icon.jpg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.drawingArea = DrawingArea(self.centralwidget)
        self.drawingArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.drawingArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.drawingArea.setRenderHints(QtGui.QPainter.Antialiasing|QtGui.QPainter.TextAntialiasing)
        self.drawingArea.setDragMode(QtGui.QGraphicsView.RubberBandDrag)
        self.drawingArea.setCacheMode(QtGui.QGraphicsView.CacheBackground)
        self.drawingArea.setTransformationAnchor(QtGui.QGraphicsView.NoAnchor)
        self.drawingArea.setResizeAnchor(QtGui.QGraphicsView.AnchorUnderMouse)
        self.drawingArea.setViewportUpdateMode(QtGui.QGraphicsView.FullViewportUpdate)
        self.drawingArea.setRubberBandSelectionMode(QtCore.Qt.ContainsItemShape)
        self.drawingArea.setObjectName(_fromUtf8("drawingArea"))
        self.horizontalLayout.addWidget(self.drawingArea)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1089, 38))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menu_File = QtGui.QMenu(self.menubar)
        self.menu_File.setObjectName(_fromUtf8("menu_File"))
        self.menu_Edit = QtGui.QMenu(self.menubar)
        self.menu_Edit.setObjectName(_fromUtf8("menu_Edit"))
        self.menu_setPenWidth = QtGui.QMenu(self.menu_Edit)
        self.menu_setPenWidth.setObjectName(_fromUtf8("menu_setPenWidth"))
        self.menu_setPenColour = QtGui.QMenu(self.menu_Edit)
        self.menu_setPenColour.setObjectName(_fromUtf8("menu_setPenColour"))
        self.menu_setPenStyle = QtGui.QMenu(self.menu_Edit)
        self.menu_setPenStyle.setObjectName(_fromUtf8("menu_setPenStyle"))
        self.menu_setFillColour = QtGui.QMenu(self.menu_Edit)
        self.menu_setFillColour.setObjectName(_fromUtf8("menu_setFillColour"))
        self.menu_setFillStyle = QtGui.QMenu(self.menu_Edit)
        self.menu_setFillStyle.setObjectName(_fromUtf8("menu_setFillStyle"))
        self.menu_AddSymbol = QtGui.QMenu(self.menubar)
        self.menu_AddSymbol.setObjectName(_fromUtf8("menu_AddSymbol"))
        self.menu_Transistor = QtGui.QMenu(self.menu_AddSymbol)
        self.menu_Transistor.setObjectName(_fromUtf8("menu_Transistor"))
        self.menu_N_type_MOSFET = QtGui.QMenu(self.menu_Transistor)
        self.menu_N_type_MOSFET.setObjectName(_fromUtf8("menu_N_type_MOSFET"))
        self.menu_P_type_MOSFET = QtGui.QMenu(self.menu_Transistor)
        self.menu_P_type_MOSFET.setObjectName(_fromUtf8("menu_P_type_MOSFET"))
        self.menuSources = QtGui.QMenu(self.menu_AddSymbol)
        self.menuSources.setObjectName(_fromUtf8("menuSources"))
        self.menu_DC = QtGui.QMenu(self.menuSources)
        self.menu_DC.setObjectName(_fromUtf8("menu_DC"))
        self.menu_Controlled = QtGui.QMenu(self.menuSources)
        self.menu_Controlled.setObjectName(_fromUtf8("menu_Controlled"))
        self.menu_View = QtGui.QMenu(self.menubar)
        self.menu_View.setObjectName(_fromUtf8("menu_View"))
        self.menuSh_ape = QtGui.QMenu(self.menubar)
        self.menuSh_ape.setObjectName(_fromUtf8("menuSh_ape"))
        self.menu_Arc = QtGui.QMenu(self.menuSh_ape)
        self.menu_Arc.setObjectName(_fromUtf8("menu_Arc"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QtGui.QToolBar(MainWindow)
        self.toolBar.setMovable(False)
        self.toolBar.setObjectName(_fromUtf8("toolBar"))
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.action_exportFile = QtGui.QAction(MainWindow)
        self.action_exportFile.setObjectName(_fromUtf8("action_exportFile"))
        self.action_quit = QtGui.QAction(MainWindow)
        self.action_quit.setObjectName(_fromUtf8("action_quit"))
        self.action_move = QtGui.QAction(MainWindow)
        self.action_move.setCheckable(True)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/view-fullscreen.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_move.setIcon(icon1)
        self.action_move.setIconVisibleInMenu(False)
        self.action_move.setObjectName(_fromUtf8("action_move"))
        self.action_copy = QtGui.QAction(MainWindow)
        self.action_copy.setCheckable(True)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/edit-copy.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_copy.setIcon(icon2)
        self.action_copy.setIconVisibleInMenu(False)
        self.action_copy.setObjectName(_fromUtf8("action_copy"))
        self.action_addWire = QtGui.QAction(MainWindow)
        self.action_addWire.setObjectName(_fromUtf8("action_addWire"))
        self.action_addResistor = QtGui.QAction(MainWindow)
        self.action_addResistor.setObjectName(_fromUtf8("action_addResistor"))
        self.action_addDot = QtGui.QAction(MainWindow)
        self.action_addDot.setObjectName(_fromUtf8("action_addDot"))
        self.action_setWidth2 = QtGui.QAction(MainWindow)
        self.action_setWidth2.setCheckable(True)
        self.action_setWidth2.setChecked(False)
        self.action_setWidth2.setObjectName(_fromUtf8("action_setWidth2"))
        self.action_setWidth4 = QtGui.QAction(MainWindow)
        self.action_setWidth4.setCheckable(True)
        self.action_setWidth4.setChecked(True)
        self.action_setWidth4.setObjectName(_fromUtf8("action_setWidth4"))
        self.action_setWidth6 = QtGui.QAction(MainWindow)
        self.action_setWidth6.setCheckable(True)
        self.action_setWidth6.setObjectName(_fromUtf8("action_setWidth6"))
        self.action_setWidth8 = QtGui.QAction(MainWindow)
        self.action_setWidth8.setCheckable(True)
        self.action_setWidth8.setObjectName(_fromUtf8("action_setWidth8"))
        self.action_setWidth10 = QtGui.QAction(MainWindow)
        self.action_setWidth10.setCheckable(True)
        self.action_setWidth10.setObjectName(_fromUtf8("action_setWidth10"))
        self.action_rotate = QtGui.QAction(MainWindow)
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/object-rotate-right.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_rotate.setIcon(icon3)
        self.action_rotate.setIconVisibleInMenu(False)
        self.action_rotate.setObjectName(_fromUtf8("action_rotate"))
        self.action_mirror = QtGui.QAction(MainWindow)
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/object-flip-horizontal.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_mirror.setIcon(icon4)
        self.action_mirror.setIconVisibleInMenu(False)
        self.action_mirror.setObjectName(_fromUtf8("action_mirror"))
        self.action_fitToView = QtGui.QAction(MainWindow)
        self.action_fitToView.setObjectName(_fromUtf8("action_fitToView"))
        self.action_showGrid = QtGui.QAction(MainWindow)
        self.action_showGrid.setCheckable(True)
        self.action_showGrid.setChecked(True)
        self.action_showGrid.setObjectName(_fromUtf8("action_showGrid"))
        self.action_delete = QtGui.QAction(MainWindow)
        self.action_delete.setCheckable(False)
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/list-remove.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_delete.setIcon(icon5)
        self.action_delete.setIconVisibleInMenu(False)
        self.action_delete.setObjectName(_fromUtf8("action_delete"))
        self.action_setPenColourRed = QtGui.QAction(MainWindow)
        self.action_setPenColourRed.setCheckable(True)
        self.action_setPenColourRed.setObjectName(_fromUtf8("action_setPenColourRed"))
        self.action_setPenColourBlue = QtGui.QAction(MainWindow)
        self.action_setPenColourBlue.setCheckable(True)
        self.action_setPenColourBlue.setObjectName(_fromUtf8("action_setPenColourBlue"))
        self.action_setPenColourGreen = QtGui.QAction(MainWindow)
        self.action_setPenColourGreen.setCheckable(True)
        self.action_setPenColourGreen.setObjectName(_fromUtf8("action_setPenColourGreen"))
        self.action_setPenColourBlack = QtGui.QAction(MainWindow)
        self.action_setPenColourBlack.setCheckable(True)
        self.action_setPenColourBlack.setChecked(True)
        self.action_setPenColourBlack.setObjectName(_fromUtf8("action_setPenColourBlack"))
        self.action_setPenStyleSolid = QtGui.QAction(MainWindow)
        self.action_setPenStyleSolid.setCheckable(True)
        self.action_setPenStyleSolid.setChecked(True)
        self.action_setPenStyleSolid.setObjectName(_fromUtf8("action_setPenStyleSolid"))
        self.action_setPenStyleDash = QtGui.QAction(MainWindow)
        self.action_setPenStyleDash.setCheckable(True)
        self.action_setPenStyleDash.setObjectName(_fromUtf8("action_setPenStyleDash"))
        self.action_setPenStyleDot = QtGui.QAction(MainWindow)
        self.action_setPenStyleDot.setCheckable(True)
        self.action_setPenStyleDot.setObjectName(_fromUtf8("action_setPenStyleDot"))
        self.action_setPenStyleDashDot = QtGui.QAction(MainWindow)
        self.action_setPenStyleDashDot.setCheckable(True)
        self.action_setPenStyleDashDot.setObjectName(_fromUtf8("action_setPenStyleDashDot"))
        self.action_setPenStyleDashDotDot = QtGui.QAction(MainWindow)
        self.action_setPenStyleDashDotDot.setCheckable(True)
        self.action_setPenStyleDashDotDot.setObjectName(_fromUtf8("action_setPenStyleDashDotDot"))
        self.action_addCapacitor = QtGui.QAction(MainWindow)
        self.action_addCapacitor.setObjectName(_fromUtf8("action_addCapacitor"))
        self.action_addGround = QtGui.QAction(MainWindow)
        self.action_addGround.setObjectName(_fromUtf8("action_addGround"))
        self.action_setBrushColourBlack = QtGui.QAction(MainWindow)
        self.action_setBrushColourBlack.setCheckable(True)
        self.action_setBrushColourBlack.setChecked(True)
        self.action_setBrushColourBlack.setObjectName(_fromUtf8("action_setBrushColourBlack"))
        self.action_setBrushColourRed = QtGui.QAction(MainWindow)
        self.action_setBrushColourRed.setCheckable(True)
        self.action_setBrushColourRed.setObjectName(_fromUtf8("action_setBrushColourRed"))
        self.action_setBrushColourBlue = QtGui.QAction(MainWindow)
        self.action_setBrushColourBlue.setCheckable(True)
        self.action_setBrushColourBlue.setObjectName(_fromUtf8("action_setBrushColourBlue"))
        self.action_setBrushColourGreen = QtGui.QAction(MainWindow)
        self.action_setBrushColourGreen.setCheckable(True)
        self.action_setBrushColourGreen.setObjectName(_fromUtf8("action_setBrushColourGreen"))
        self.action_setBrushStyleNone = QtGui.QAction(MainWindow)
        self.action_setBrushStyleNone.setCheckable(True)
        self.action_setBrushStyleNone.setChecked(True)
        self.action_setBrushStyleNone.setObjectName(_fromUtf8("action_setBrushStyleNone"))
        self.action_setBrushStyleSolid = QtGui.QAction(MainWindow)
        self.action_setBrushStyleSolid.setCheckable(True)
        self.action_setBrushStyleSolid.setObjectName(_fromUtf8("action_setBrushStyleSolid"))
        self.action_addNPNBJT = QtGui.QAction(MainWindow)
        self.action_addNPNBJT.setObjectName(_fromUtf8("action_addNPNBJT"))
        self.action_addPNPBJT = QtGui.QAction(MainWindow)
        self.action_addPNPBJT.setObjectName(_fromUtf8("action_addPNPBJT"))
        self.action_addNMOSWithArrow = QtGui.QAction(MainWindow)
        self.action_addNMOSWithArrow.setObjectName(_fromUtf8("action_addNMOSWithArrow"))
        self.action_addNMOSWithoutArrow = QtGui.QAction(MainWindow)
        self.action_addNMOSWithoutArrow.setObjectName(_fromUtf8("action_addNMOSWithoutArrow"))
        self.action_addPMOSWithArrow = QtGui.QAction(MainWindow)
        self.action_addPMOSWithArrow.setObjectName(_fromUtf8("action_addPMOSWithArrow"))
        self.action_addPMOSWithoutArrow = QtGui.QAction(MainWindow)
        self.action_addPMOSWithoutArrow.setObjectName(_fromUtf8("action_addPMOSWithoutArrow"))
        self.action_saveSymbol = QtGui.QAction(MainWindow)
        self.action_saveSymbol.setObjectName(_fromUtf8("action_saveSymbol"))
        self.action_loadSymbol = QtGui.QAction(MainWindow)
        self.action_loadSymbol.setObjectName(_fromUtf8("action_loadSymbol"))
        self.action_saveSchematic = QtGui.QAction(MainWindow)
        self.action_saveSchematic.setObjectName(_fromUtf8("action_saveSchematic"))
        self.action_loadSchematic = QtGui.QAction(MainWindow)
        self.action_loadSchematic.setObjectName(_fromUtf8("action_loadSchematic"))
        self.action_addLine = QtGui.QAction(MainWindow)
        self.action_addLine.setObjectName(_fromUtf8("action_addLine"))
        self.action_addRectangle = QtGui.QAction(MainWindow)
        self.action_addRectangle.setObjectName(_fromUtf8("action_addRectangle"))
        self.action_addCircle = QtGui.QAction(MainWindow)
        self.action_addCircle.setObjectName(_fromUtf8("action_addCircle"))
        self.action_addEllipse = QtGui.QAction(MainWindow)
        self.action_addEllipse.setObjectName(_fromUtf8("action_addEllipse"))
        self.action_snapToGrid = QtGui.QAction(MainWindow)
        self.action_snapToGrid.setCheckable(True)
        self.action_snapToGrid.setChecked(True)
        self.action_snapToGrid.setObjectName(_fromUtf8("action_snapToGrid"))
        self.action_addTextBox = QtGui.QAction(MainWindow)
        self.action_addTextBox.setObjectName(_fromUtf8("action_addTextBox"))
        self.action_setPenColourCyan = QtGui.QAction(MainWindow)
        self.action_setPenColourCyan.setCheckable(True)
        self.action_setPenColourCyan.setObjectName(_fromUtf8("action_setPenColourCyan"))
        self.action_setPenColourMagenta = QtGui.QAction(MainWindow)
        self.action_setPenColourMagenta.setCheckable(True)
        self.action_setPenColourMagenta.setObjectName(_fromUtf8("action_setPenColourMagenta"))
        self.action_setPenColourYellow = QtGui.QAction(MainWindow)
        self.action_setPenColourYellow.setCheckable(True)
        self.action_setPenColourYellow.setObjectName(_fromUtf8("action_setPenColourYellow"))
        self.action_setBrushColourCyan = QtGui.QAction(MainWindow)
        self.action_setBrushColourCyan.setCheckable(True)
        self.action_setBrushColourCyan.setObjectName(_fromUtf8("action_setBrushColourCyan"))
        self.action_setBrushColourMagenta = QtGui.QAction(MainWindow)
        self.action_setBrushColourMagenta.setCheckable(True)
        self.action_setBrushColourMagenta.setObjectName(_fromUtf8("action_setBrushColourMagenta"))
        self.action_setBrushColourYellow = QtGui.QAction(MainWindow)
        self.action_setBrushColourYellow.setCheckable(True)
        self.action_setBrushColourYellow.setObjectName(_fromUtf8("action_setBrushColourYellow"))
        self.action_addDCVoltageSource = QtGui.QAction(MainWindow)
        self.action_addDCVoltageSource.setObjectName(_fromUtf8("action_addDCVoltageSource"))
        self.action_addDCCurrentSource = QtGui.QAction(MainWindow)
        self.action_addDCCurrentSource.setObjectName(_fromUtf8("action_addDCCurrentSource"))
        self.action_addVCVS = QtGui.QAction(MainWindow)
        self.action_addVCVS.setObjectName(_fromUtf8("action_addVCVS"))
        self.action_addVCCS = QtGui.QAction(MainWindow)
        self.action_addVCCS.setObjectName(_fromUtf8("action_addVCCS"))
        self.action_addCCVS = QtGui.QAction(MainWindow)
        self.action_addCCVS.setObjectName(_fromUtf8("action_addCCVS"))
        self.action_addCCCS = QtGui.QAction(MainWindow)
        self.action_addCCCS.setObjectName(_fromUtf8("action_addCCCS"))
        self.action_addACSource = QtGui.QAction(MainWindow)
        self.action_addACSource.setObjectName(_fromUtf8("action_addACSource"))
        self.action_addArc3Point = QtGui.QAction(MainWindow)
        self.action_addArc3Point.setObjectName(_fromUtf8("action_addArc3Point"))
        self.action_addArc4Point = QtGui.QAction(MainWindow)
        self.action_addArc4Point.setObjectName(_fromUtf8("action_addArc4Point"))
        self.action_undo = QtGui.QAction(MainWindow)
        self.action_undo.setEnabled(False)
        icon6 = QtGui.QIcon()
        icon6.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/edit-undo.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_undo.setIcon(icon6)
        self.action_undo.setIconVisibleInMenu(False)
        self.action_undo.setObjectName(_fromUtf8("action_undo"))
        self.action_redo = QtGui.QAction(MainWindow)
        self.action_redo.setEnabled(False)
        icon7 = QtGui.QIcon()
        icon7.addPixmap(QtGui.QPixmap(_fromUtf8(":/icons/edit-redo.svg")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.action_redo.setIcon(icon7)
        self.action_redo.setIconVisibleInMenu(False)
        self.action_redo.setObjectName(_fromUtf8("action_redo"))
        self.action_saveSchematicAs = QtGui.QAction(MainWindow)
        self.action_saveSchematicAs.setObjectName(_fromUtf8("action_saveSchematicAs"))
        self.action_saveSymbolAs = QtGui.QAction(MainWindow)
        self.action_saveSymbolAs.setObjectName(_fromUtf8("action_saveSymbolAs"))
        self.action_modifySymbol = QtGui.QAction(MainWindow)
        self.action_modifySymbol.setObjectName(_fromUtf8("action_modifySymbol"))
        self.action_editShape = QtGui.QAction(MainWindow)
        self.action_editShape.setObjectName(_fromUtf8("action_editShape"))
        self.action_newSchematic = QtGui.QAction(MainWindow)
        self.action_newSchematic.setObjectName(_fromUtf8("action_newSchematic"))
        self.menu_File.addAction(self.action_newSchematic)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_saveSchematic)
        self.menu_File.addAction(self.action_saveSchematicAs)
        self.menu_File.addAction(self.action_saveSymbol)
        self.menu_File.addAction(self.action_saveSymbolAs)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_loadSchematic)
        self.menu_File.addAction(self.action_loadSymbol)
        self.menu_File.addAction(self.action_modifySymbol)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_exportFile)
        self.menu_File.addSeparator()
        self.menu_File.addAction(self.action_quit)
        self.menu_setPenWidth.addAction(self.action_setWidth2)
        self.menu_setPenWidth.addAction(self.action_setWidth4)
        self.menu_setPenWidth.addAction(self.action_setWidth6)
        self.menu_setPenWidth.addAction(self.action_setWidth8)
        self.menu_setPenWidth.addAction(self.action_setWidth10)
        self.menu_setPenColour.addAction(self.action_setPenColourBlack)
        self.menu_setPenColour.addAction(self.action_setPenColourRed)
        self.menu_setPenColour.addAction(self.action_setPenColourBlue)
        self.menu_setPenColour.addAction(self.action_setPenColourGreen)
        self.menu_setPenColour.addAction(self.action_setPenColourCyan)
        self.menu_setPenColour.addAction(self.action_setPenColourMagenta)
        self.menu_setPenColour.addAction(self.action_setPenColourYellow)
        self.menu_setPenStyle.addAction(self.action_setPenStyleSolid)
        self.menu_setPenStyle.addAction(self.action_setPenStyleDash)
        self.menu_setPenStyle.addAction(self.action_setPenStyleDot)
        self.menu_setPenStyle.addAction(self.action_setPenStyleDashDot)
        self.menu_setPenStyle.addAction(self.action_setPenStyleDashDotDot)
        self.menu_setFillColour.addAction(self.action_setBrushColourBlack)
        self.menu_setFillColour.addAction(self.action_setBrushColourRed)
        self.menu_setFillColour.addAction(self.action_setBrushColourBlue)
        self.menu_setFillColour.addAction(self.action_setBrushColourGreen)
        self.menu_setFillColour.addAction(self.action_setBrushColourCyan)
        self.menu_setFillColour.addAction(self.action_setBrushColourMagenta)
        self.menu_setFillColour.addAction(self.action_setBrushColourYellow)
        self.menu_setFillStyle.addAction(self.action_setBrushStyleNone)
        self.menu_setFillStyle.addAction(self.action_setBrushStyleSolid)
        self.menu_Edit.addAction(self.action_undo)
        self.menu_Edit.addAction(self.action_redo)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.action_delete)
        self.menu_Edit.addAction(self.action_move)
        self.menu_Edit.addAction(self.action_copy)
        self.menu_Edit.addAction(self.action_rotate)
        self.menu_Edit.addAction(self.action_mirror)
        self.menu_Edit.addSeparator()
        self.menu_Edit.addAction(self.menu_setPenWidth.menuAction())
        self.menu_Edit.addAction(self.menu_setPenColour.menuAction())
        self.menu_Edit.addAction(self.menu_setPenStyle.menuAction())
        self.menu_Edit.addAction(self.menu_setFillColour.menuAction())
        self.menu_Edit.addAction(self.menu_setFillStyle.menuAction())
        self.menu_N_type_MOSFET.addAction(self.action_addNMOSWithArrow)
        self.menu_N_type_MOSFET.addAction(self.action_addNMOSWithoutArrow)
        self.menu_P_type_MOSFET.addAction(self.action_addPMOSWithArrow)
        self.menu_P_type_MOSFET.addAction(self.action_addPMOSWithoutArrow)
        self.menu_Transistor.addAction(self.menu_N_type_MOSFET.menuAction())
        self.menu_Transistor.addAction(self.menu_P_type_MOSFET.menuAction())
        self.menu_Transistor.addAction(self.action_addNPNBJT)
        self.menu_Transistor.addAction(self.action_addPNPBJT)
        self.menu_DC.addAction(self.action_addDCVoltageSource)
        self.menu_DC.addAction(self.action_addDCCurrentSource)
        self.menu_Controlled.addAction(self.action_addVCVS)
        self.menu_Controlled.addAction(self.action_addVCCS)
        self.menu_Controlled.addAction(self.action_addCCVS)
        self.menu_Controlled.addAction(self.action_addCCCS)
        self.menuSources.addAction(self.menu_DC.menuAction())
        self.menuSources.addAction(self.action_addACSource)
        self.menuSources.addAction(self.menu_Controlled.menuAction())
        self.menu_AddSymbol.addAction(self.action_addWire)
        self.menu_AddSymbol.addAction(self.action_addResistor)
        self.menu_AddSymbol.addAction(self.action_addCapacitor)
        self.menu_AddSymbol.addAction(self.action_addGround)
        self.menu_AddSymbol.addAction(self.action_addDot)
        self.menu_AddSymbol.addAction(self.menu_Transistor.menuAction())
        self.menu_AddSymbol.addAction(self.menuSources.menuAction())
        self.menu_View.addAction(self.action_fitToView)
        self.menu_View.addAction(self.action_showGrid)
        self.menu_View.addAction(self.action_snapToGrid)
        self.menu_Arc.addAction(self.action_addArc3Point)
        self.menu_Arc.addAction(self.action_addArc4Point)
        self.menuSh_ape.addAction(self.action_addLine)
        self.menuSh_ape.addAction(self.menu_Arc.menuAction())
        self.menuSh_ape.addAction(self.action_addRectangle)
        self.menuSh_ape.addAction(self.action_addCircle)
        self.menuSh_ape.addAction(self.action_addEllipse)
        self.menuSh_ape.addAction(self.action_addTextBox)
        self.menuSh_ape.addAction(self.action_editShape)
        self.menubar.addAction(self.menu_File.menuAction())
        self.menubar.addAction(self.menu_Edit.menuAction())
        self.menubar.addAction(self.menu_View.menuAction())
        self.menubar.addAction(self.menuSh_ape.menuAction())
        self.menubar.addAction(self.menu_AddSymbol.menuAction())
        self.toolBar.addAction(self.action_undo)
        self.toolBar.addAction(self.action_redo)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.action_move)
        self.toolBar.addAction(self.action_delete)
        self.toolBar.addAction(self.action_copy)
        self.toolBar.addAction(self.action_rotate)
        self.toolBar.addAction(self.action_mirror)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "YCircuit", None))
        self.menu_File.setTitle(_translate("MainWindow", "&File", None))
        self.menu_Edit.setTitle(_translate("MainWindow", "&Edit", None))
        self.menu_setPenWidth.setTitle(_translate("MainWindow", "&Width", None))
        self.menu_setPenColour.setTitle(_translate("MainWindow", "&Colour", None))
        self.menu_setPenStyle.setTitle(_translate("MainWindow", "&Pen style", None))
        self.menu_setFillColour.setTitle(_translate("MainWindow", "Fill colour", None))
        self.menu_setFillStyle.setTitle(_translate("MainWindow", "Fill style", None))
        self.menu_AddSymbol.setTitle(_translate("MainWindow", "&Symbol", None))
        self.menu_Transistor.setTitle(_translate("MainWindow", "&Transistor", None))
        self.menu_N_type_MOSFET.setTitle(_translate("MainWindow", "&N-type MOSFET", None))
        self.menu_P_type_MOSFET.setTitle(_translate("MainWindow", "&P-type MOSFET", None))
        self.menuSources.setTitle(_translate("MainWindow", "&Sources", None))
        self.menu_DC.setTitle(_translate("MainWindow", "&DC", None))
        self.menu_Controlled.setTitle(_translate("MainWindow", "&Controlled", None))
        self.menu_View.setTitle(_translate("MainWindow", "&View", None))
        self.menuSh_ape.setTitle(_translate("MainWindow", "Sh&ape", None))
        self.menu_Arc.setTitle(_translate("MainWindow", "&Arc", None))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar", None))
        self.action_exportFile.setText(_translate("MainWindow", "Export file", None))
        self.action_exportFile.setToolTip(_translate("MainWindow", "Exports file as an image", None))
        self.action_exportFile.setShortcut(_translate("MainWindow", "Ctrl+E", None))
        self.action_quit.setText(_translate("MainWindow", "Quit", None))
        self.action_quit.setToolTip(_translate("MainWindow", "Quits the program", None))
        self.action_quit.setShortcut(_translate("MainWindow", "Ctrl+Q", None))
        self.action_move.setText(_translate("MainWindow", "Move", None))
        self.action_move.setToolTip(_translate("MainWindow", "Move selected items", None))
        self.action_move.setShortcut(_translate("MainWindow", "M", None))
        self.action_copy.setText(_translate("MainWindow", "Copy", None))
        self.action_copy.setToolTip(_translate("MainWindow", "Copy selected items", None))
        self.action_copy.setShortcut(_translate("MainWindow", "C", None))
        self.action_addWire.setText(_translate("MainWindow", "&Wire", None))
        self.action_addWire.setToolTip(_translate("MainWindow", "Draws a wire", None))
        self.action_addResistor.setText(_translate("MainWindow", "&Resistor", None))
        self.action_addResistor.setToolTip(_translate("MainWindow", "Draws a resistor", None))
        self.action_addDot.setText(_translate("MainWindow", "Connection &dot", None))
        self.action_addDot.setToolTip(_translate("MainWindow", "Draws a dot signifying connectivity", None))
        self.action_setWidth2.setText(_translate("MainWindow", "2", None))
        self.action_setWidth2.setToolTip(_translate("MainWindow", "Sets the width of currently selected items to 2", None))
        self.action_setWidth4.setText(_translate("MainWindow", "4", None))
        self.action_setWidth4.setToolTip(_translate("MainWindow", "Sets the width of currently selected items to 4", None))
        self.action_setWidth6.setText(_translate("MainWindow", "6", None))
        self.action_setWidth6.setToolTip(_translate("MainWindow", "Sets the width of currently selected items to 6", None))
        self.action_setWidth8.setText(_translate("MainWindow", "8", None))
        self.action_setWidth8.setToolTip(_translate("MainWindow", "Sets the width of currently selected items to 8", None))
        self.action_setWidth10.setText(_translate("MainWindow", "10", None))
        self.action_setWidth10.setToolTip(_translate("MainWindow", "Sets the width of currently selected items to 10", None))
        self.action_rotate.setText(_translate("MainWindow", "Rotate", None))
        self.action_rotate.setToolTip(_translate("MainWindow", "Rotate selected items", None))
        self.action_rotate.setShortcut(_translate("MainWindow", "R", None))
        self.action_mirror.setText(_translate("MainWindow", "Mirror", None))
        self.action_mirror.setToolTip(_translate("MainWindow", "Mirror selected items", None))
        self.action_mirror.setShortcut(_translate("MainWindow", "Shift+R", None))
        self.action_fitToView.setText(_translate("MainWindow", "Fit to view", None))
        self.action_fitToView.setShortcut(_translate("MainWindow", "F", None))
        self.action_showGrid.setText(_translate("MainWindow", "Show grid", None))
        self.action_showGrid.setToolTip(_translate("MainWindow", "Toggle grid visibility", None))
        self.action_showGrid.setShortcut(_translate("MainWindow", "G", None))
        self.action_delete.setText(_translate("MainWindow", "Delete", None))
        self.action_delete.setToolTip(_translate("MainWindow", "Delete selected items", None))
        self.action_delete.setShortcut(_translate("MainWindow", "D", None))
        self.action_setPenColourRed.setText(_translate("MainWindow", "&Red", None))
        self.action_setPenColourRed.setToolTip(_translate("MainWindow", "Set the colour of selected items to red", None))
        self.action_setPenColourBlue.setText(_translate("MainWindow", "&Blue", None))
        self.action_setPenColourBlue.setToolTip(_translate("MainWindow", "Set the colour of selected items to blue", None))
        self.action_setPenColourGreen.setText(_translate("MainWindow", "&Green", None))
        self.action_setPenColourGreen.setToolTip(_translate("MainWindow", "Set the colour of selected items to green", None))
        self.action_setPenColourBlack.setText(_translate("MainWindow", "Blac&k", None))
        self.action_setPenColourBlack.setToolTip(_translate("MainWindow", "Set the colour of selected items to black", None))
        self.action_setPenStyleSolid.setText(_translate("MainWindow", "&Solid", None))
        self.action_setPenStyleSolid.setToolTip(_translate("MainWindow", "Set pen style for selected items to solid", None))
        self.action_setPenStyleDash.setText(_translate("MainWindow", "&Dash", None))
        self.action_setPenStyleDash.setToolTip(_translate("MainWindow", "Set pen style for selected items to dash", None))
        self.action_setPenStyleDot.setText(_translate("MainWindow", "Do&t", None))
        self.action_setPenStyleDot.setToolTip(_translate("MainWindow", "Set pen style for selected items to dot", None))
        self.action_setPenStyleDashDot.setText(_translate("MainWindow", "D&ash-Dot", None))
        self.action_setPenStyleDashDot.setToolTip(_translate("MainWindow", "Set pen style for selected items to dash-dot", None))
        self.action_setPenStyleDashDotDot.setText(_translate("MainWindow", "Dash-dot-dot", None))
        self.action_setPenStyleDashDotDot.setToolTip(_translate("MainWindow", "Set pen style for selected items to dash-dot-dot", None))
        self.action_addCapacitor.setText(_translate("MainWindow", "&Capacitor", None))
        self.action_addCapacitor.setToolTip(_translate("MainWindow", "Draws a capacitor", None))
        self.action_addGround.setText(_translate("MainWindow", "&Ground", None))
        self.action_addGround.setToolTip(_translate("MainWindow", "Draws a ground symbol", None))
        self.action_setBrushColourBlack.setText(_translate("MainWindow", "Blac&k", None))
        self.action_setBrushColourBlack.setToolTip(_translate("MainWindow", "Sets the fill colour to black", None))
        self.action_setBrushColourRed.setText(_translate("MainWindow", "&Red", None))
        self.action_setBrushColourRed.setToolTip(_translate("MainWindow", "Set the fill colour to red", None))
        self.action_setBrushColourBlue.setText(_translate("MainWindow", "&Blue", None))
        self.action_setBrushColourBlue.setToolTip(_translate("MainWindow", "Set the fill colour to blue", None))
        self.action_setBrushColourGreen.setText(_translate("MainWindow", "&Green", None))
        self.action_setBrushColourGreen.setToolTip(_translate("MainWindow", "Set the brush colour to green", None))
        self.action_setBrushStyleNone.setText(_translate("MainWindow", "&No fill", None))
        self.action_setBrushStyleNone.setToolTip(_translate("MainWindow", "Remove any fill", None))
        self.action_setBrushStyleSolid.setText(_translate("MainWindow", "&Solid", None))
        self.action_setBrushStyleSolid.setToolTip(_translate("MainWindow", "Fill with a solid colour", None))
        self.action_addNPNBJT.setText(_translate("MainWindow", "NPN BJT", None))
        self.action_addNPNBJT.setToolTip(_translate("MainWindow", "Add NPN BJT", None))
        self.action_addPNPBJT.setText(_translate("MainWindow", "PNP BJT", None))
        self.action_addPNPBJT.setToolTip(_translate("MainWindow", "Add PNP BJT", None))
        self.action_addNMOSWithArrow.setText(_translate("MainWindow", "With &arrow", None))
        self.action_addNMOSWithArrow.setToolTip(_translate("MainWindow", "Add N-type MOSFET with arrow", None))
        self.action_addNMOSWithoutArrow.setText(_translate("MainWindow", "Without arrow", None))
        self.action_addNMOSWithoutArrow.setToolTip(_translate("MainWindow", "Add N-type MOSFET without arrow", None))
        self.action_addPMOSWithArrow.setText(_translate("MainWindow", "With &arrow", None))
        self.action_addPMOSWithArrow.setToolTip(_translate("MainWindow", "Add P-type MOSFET with arrow", None))
        self.action_addPMOSWithoutArrow.setText(_translate("MainWindow", "Without arrow", None))
        self.action_addPMOSWithoutArrow.setToolTip(_translate("MainWindow", "Add P-type MOSFET without arrow", None))
        self.action_saveSymbol.setText(_translate("MainWindow", "Save symbol", None))
        self.action_saveSymbol.setShortcut(_translate("MainWindow", "Ctrl+Shift+S", None))
        self.action_loadSymbol.setText(_translate("MainWindow", "Load symbol", None))
        self.action_loadSymbol.setShortcut(_translate("MainWindow", "Ctrl+Shift+L", None))
        self.action_saveSchematic.setText(_translate("MainWindow", "Save schematic", None))
        self.action_saveSchematic.setShortcut(_translate("MainWindow", "Ctrl+S", None))
        self.action_loadSchematic.setText(_translate("MainWindow", "Load schematic", None))
        self.action_loadSchematic.setShortcut(_translate("MainWindow", "Ctrl+L", None))
        self.action_addLine.setText(_translate("MainWindow", "&Line", None))
        self.action_addRectangle.setText(_translate("MainWindow", "&Rectangle", None))
        self.action_addCircle.setText(_translate("MainWindow", "&Circle", None))
        self.action_addEllipse.setText(_translate("MainWindow", "&Ellipse", None))
        self.action_snapToGrid.setText(_translate("MainWindow", "Sn&ap to grid", None))
        self.action_addTextBox.setText(_translate("MainWindow", "&Text box", None))
        self.action_setPenColourCyan.setText(_translate("MainWindow", "&Cyan", None))
        self.action_setPenColourMagenta.setText(_translate("MainWindow", "&Magenta", None))
        self.action_setPenColourYellow.setText(_translate("MainWindow", "&Yellow", None))
        self.action_setBrushColourCyan.setText(_translate("MainWindow", "&Cyan", None))
        self.action_setBrushColourMagenta.setText(_translate("MainWindow", "&Magenta", None))
        self.action_setBrushColourYellow.setText(_translate("MainWindow", "&Yellow", None))
        self.action_addDCVoltageSource.setText(_translate("MainWindow", "&Voltage", None))
        self.action_addDCVoltageSource.setToolTip(_translate("MainWindow", "Adds a DC voltage source", None))
        self.action_addDCCurrentSource.setText(_translate("MainWindow", "&Current", None))
        self.action_addDCCurrentSource.setToolTip(_translate("MainWindow", "Adds a DC current source", None))
        self.action_addVCVS.setText(_translate("MainWindow", "VCVS", None))
        self.action_addVCVS.setToolTip(_translate("MainWindow", "Adds a VCVS", None))
        self.action_addVCCS.setText(_translate("MainWindow", "VCCS", None))
        self.action_addVCCS.setToolTip(_translate("MainWindow", "Adds a VCCS", None))
        self.action_addCCVS.setText(_translate("MainWindow", "CCVS", None))
        self.action_addCCVS.setToolTip(_translate("MainWindow", "Adds a CCVS", None))
        self.action_addCCCS.setText(_translate("MainWindow", "CCCS", None))
        self.action_addCCCS.setToolTip(_translate("MainWindow", "Adds a CCCS", None))
        self.action_addACSource.setText(_translate("MainWindow", "&AC", None))
        self.action_addArc3Point.setText(_translate("MainWindow", "&3-point", None))
        self.action_addArc4Point.setText(_translate("MainWindow", "&4-point", None))
        self.action_undo.setText(_translate("MainWindow", "Undo", None))
        self.action_undo.setToolTip(_translate("MainWindow", "Undo the previous action", None))
        self.action_undo.setShortcut(_translate("MainWindow", "Ctrl+Z", None))
        self.action_redo.setText(_translate("MainWindow", "Redo", None))
        self.action_redo.setToolTip(_translate("MainWindow", "Redo the previously undid action", None))
        self.action_redo.setShortcut(_translate("MainWindow", "Ctrl+Y", None))
        self.action_saveSchematicAs.setText(_translate("MainWindow", "Save s&chematic as", None))
        self.action_saveSymbolAs.setText(_translate("MainWindow", "Save &symbol as", None))
        self.action_modifySymbol.setText(_translate("MainWindow", "&Modify symbol", None))
        self.action_editShape.setText(_translate("MainWindow", "Edit shape", None))
        self.action_editShape.setToolTip(_translate("MainWindow", "Edit selected shape", None))
        self.action_editShape.setShortcut(_translate("MainWindow", "E", None))
        self.action_newSchematic.setText(_translate("MainWindow", "New Schematic", None))
        self.action_newSchematic.setToolTip(_translate("MainWindow", "Create a new schematic", None))
        self.action_newSchematic.setShortcut(_translate("MainWindow", "Ctrl+N", None))

from src.drawingarea import DrawingArea
import icon_rc
