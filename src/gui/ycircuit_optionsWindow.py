# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/gui/ycircuit_optionsWindow.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Dialog.sizePolicy().hasHeightForWidth())
        Dialog.setSizePolicy(sizePolicy)
        Dialog.setMaximumSize(QtCore.QSize(800, 600))
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.tabWidget = QtWidgets.QTabWidget(Dialog)
        self.tabWidget.setObjectName("tabWidget")
        self.tab_printing = QtWidgets.QWidget()
        self.tab_printing.setObjectName("tab_printing")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.tab_printing)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.groupBox = QtWidgets.QGroupBox(self.tab_printing)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 2, 1, 1, 1)
        self.comboBox_penWidth = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_penWidth.setObjectName("comboBox_penWidth")
        self.comboBox_penWidth.addItem("")
        self.comboBox_penWidth.addItem("")
        self.comboBox_penWidth.addItem("")
        self.comboBox_penWidth.addItem("")
        self.comboBox_penWidth.addItem("")
        self.gridLayout.addWidget(self.comboBox_penWidth, 0, 2, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.comboBox_penStyle = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_penStyle.setObjectName("comboBox_penStyle")
        self.comboBox_penStyle.addItem("")
        self.comboBox_penStyle.addItem("")
        self.comboBox_penStyle.addItem("")
        self.comboBox_penStyle.addItem("")
        self.comboBox_penStyle.addItem("")
        self.gridLayout.addWidget(self.comboBox_penStyle, 2, 2, 1, 1)
        self.comboBox_penColour = QtWidgets.QComboBox(self.groupBox)
        self.comboBox_penColour.setObjectName("comboBox_penColour")
        self.comboBox_penColour.addItem("")
        self.comboBox_penColour.addItem("")
        self.comboBox_penColour.addItem("")
        self.comboBox_penColour.addItem("")
        self.comboBox_penColour.addItem("")
        self.comboBox_penColour.addItem("")
        self.comboBox_penColour.addItem("")
        self.gridLayout.addWidget(self.comboBox_penColour, 1, 2, 1, 1)
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem2, 1, 1, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.verticalLayout_4.addWidget(self.groupBox)
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_printing)
        self.groupBox_2.setObjectName("groupBox_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.groupBox_2)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.gridLayout_3 = QtWidgets.QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_9 = QtWidgets.QLabel(self.groupBox_2)
        self.label_9.setObjectName("label_9")
        self.gridLayout_3.addWidget(self.label_9, 0, 0, 1, 1)
        spacerItem3 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem3, 0, 1, 1, 1)
        self.comboBox_brushColour = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_brushColour.setMinimumSize(QtCore.QSize(0, 0))
        self.comboBox_brushColour.setObjectName("comboBox_brushColour")
        self.comboBox_brushColour.addItem("")
        self.comboBox_brushColour.addItem("")
        self.comboBox_brushColour.addItem("")
        self.comboBox_brushColour.addItem("")
        self.comboBox_brushColour.addItem("")
        self.comboBox_brushColour.addItem("")
        self.comboBox_brushColour.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_brushColour, 0, 2, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.groupBox_2)
        self.label_10.setObjectName("label_10")
        self.gridLayout_3.addWidget(self.label_10, 1, 0, 1, 1)
        spacerItem4 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_3.addItem(spacerItem4, 1, 1, 1, 1)
        self.comboBox_brushStyle = QtWidgets.QComboBox(self.groupBox_2)
        self.comboBox_brushStyle.setMinimumSize(QtCore.QSize(0, 0))
        self.comboBox_brushStyle.setObjectName("comboBox_brushStyle")
        self.comboBox_brushStyle.addItem("")
        self.comboBox_brushStyle.addItem("")
        self.gridLayout_3.addWidget(self.comboBox_brushStyle, 1, 2, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout_3)
        self.verticalLayout_4.addWidget(self.groupBox_2)
        spacerItem5 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_4.addItem(spacerItem5)
        self.tabWidget.addTab(self.tab_printing, "")
        self.tab_grid = QtWidgets.QWidget()
        self.tab_grid.setObjectName("tab_grid")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.tab_grid)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_11 = QtWidgets.QLabel(self.tab_grid)
        self.label_11.setObjectName("label_11")
        self.horizontalLayout_5.addWidget(self.label_11)
        spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem6)
        self.checkBox_gridVisibility = QtWidgets.QCheckBox(self.tab_grid)
        self.checkBox_gridVisibility.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_gridVisibility.setText("")
        self.checkBox_gridVisibility.setObjectName("checkBox_gridVisibility")
        self.horizontalLayout_5.addWidget(self.checkBox_gridVisibility)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_grid)
        self.groupBox_3.setObjectName("groupBox_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label_14 = QtWidgets.QLabel(self.groupBox_3)
        self.label_14.setObjectName("label_14")
        self.gridLayout_2.addWidget(self.label_14, 0, 0, 1, 1)
        spacerItem7 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem7, 0, 1, 1, 1)
        self.checkBox_gridSnapToGrid = QtWidgets.QCheckBox(self.groupBox_3)
        self.checkBox_gridSnapToGrid.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_gridSnapToGrid.setText("")
        self.checkBox_gridSnapToGrid.setObjectName("checkBox_gridSnapToGrid")
        self.gridLayout_2.addWidget(self.checkBox_gridSnapToGrid, 0, 2, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.groupBox_3)
        self.label_7.setObjectName("label_7")
        self.gridLayout_2.addWidget(self.label_7, 1, 0, 1, 1)
        spacerItem8 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem8, 1, 1, 1, 1)
        self.comboBox_gridSnapToGridSpacing = QtWidgets.QComboBox(self.groupBox_3)
        self.comboBox_gridSnapToGridSpacing.setObjectName("comboBox_gridSnapToGridSpacing")
        self.comboBox_gridSnapToGridSpacing.addItem("")
        self.comboBox_gridSnapToGridSpacing.addItem("")
        self.comboBox_gridSnapToGridSpacing.addItem("")
        self.comboBox_gridSnapToGridSpacing.addItem("")
        self.comboBox_gridSnapToGridSpacing.addItem("")
        self.comboBox_gridSnapToGridSpacing.addItem("")
        self.comboBox_gridSnapToGridSpacing.addItem("")
        self.gridLayout_2.addWidget(self.comboBox_gridSnapToGridSpacing, 1, 2, 1, 1)
        self.horizontalLayout_2.addLayout(self.gridLayout_2)
        self.verticalLayout.addWidget(self.groupBox_3)
        self.groupBox_4 = QtWidgets.QGroupBox(self.tab_grid)
        self.groupBox_4.setObjectName("groupBox_4")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox_4)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.gridLayout_4 = QtWidgets.QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.label_12 = QtWidgets.QLabel(self.groupBox_4)
        self.label_12.setObjectName("label_12")
        self.gridLayout_4.addWidget(self.label_12, 0, 0, 1, 1)
        spacerItem9 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem9, 0, 1, 1, 1)
        self.checkBox_gridShowMajorGridPoints = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_gridShowMajorGridPoints.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_gridShowMajorGridPoints.setText("")
        self.checkBox_gridShowMajorGridPoints.setObjectName("checkBox_gridShowMajorGridPoints")
        self.gridLayout_4.addWidget(self.checkBox_gridShowMajorGridPoints, 0, 2, 1, 1)
        self.label_13 = QtWidgets.QLabel(self.groupBox_4)
        self.label_13.setObjectName("label_13")
        self.gridLayout_4.addWidget(self.label_13, 1, 0, 1, 1)
        spacerItem10 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem10, 1, 1, 1, 1)
        self.comboBox_gridMajorGridPointSpacing = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_gridMajorGridPointSpacing.setObjectName("comboBox_gridMajorGridPointSpacing")
        self.comboBox_gridMajorGridPointSpacing.addItem("")
        self.comboBox_gridMajorGridPointSpacing.addItem("")
        self.comboBox_gridMajorGridPointSpacing.addItem("")
        self.comboBox_gridMajorGridPointSpacing.addItem("")
        self.gridLayout_4.addWidget(self.comboBox_gridMajorGridPointSpacing, 1, 2, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.groupBox_4)
        self.label_6.setObjectName("label_6")
        self.gridLayout_4.addWidget(self.label_6, 2, 0, 1, 1)
        spacerItem11 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem11, 2, 1, 1, 1)
        self.checkBox_gridShowMinorGridPoints = QtWidgets.QCheckBox(self.groupBox_4)
        self.checkBox_gridShowMinorGridPoints.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_gridShowMinorGridPoints.setText("")
        self.checkBox_gridShowMinorGridPoints.setObjectName("checkBox_gridShowMinorGridPoints")
        self.gridLayout_4.addWidget(self.checkBox_gridShowMinorGridPoints, 2, 2, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setObjectName("label_5")
        self.gridLayout_4.addWidget(self.label_5, 3, 0, 1, 1)
        spacerItem12 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_4.addItem(spacerItem12, 3, 1, 1, 1)
        self.comboBox_gridMinorGridPointSpacing = QtWidgets.QComboBox(self.groupBox_4)
        self.comboBox_gridMinorGridPointSpacing.setObjectName("comboBox_gridMinorGridPointSpacing")
        self.comboBox_gridMinorGridPointSpacing.addItem("")
        self.comboBox_gridMinorGridPointSpacing.addItem("")
        self.comboBox_gridMinorGridPointSpacing.addItem("")
        self.comboBox_gridMinorGridPointSpacing.addItem("")
        self.comboBox_gridMinorGridPointSpacing.addItem("")
        self.comboBox_gridMinorGridPointSpacing.addItem("")
        self.comboBox_gridMinorGridPointSpacing.addItem("")
        self.gridLayout_4.addWidget(self.comboBox_gridMinorGridPointSpacing, 3, 2, 1, 1)
        self.horizontalLayout_4.addLayout(self.gridLayout_4)
        self.verticalLayout.addWidget(self.groupBox_4)
        spacerItem13 = QtWidgets.QSpacerItem(20, 184, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem13)
        self.groupBox_3.raise_()
        self.groupBox_4.raise_()
        self.tabWidget.addTab(self.tab_grid, "")
        self.tab_saveExport = QtWidgets.QWidget()
        self.tab_saveExport.setObjectName("tab_saveExport")
        self.verticalLayout_5 = QtWidgets.QVBoxLayout(self.tab_saveExport)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.groupBox_5 = QtWidgets.QGroupBox(self.tab_saveExport)
        self.groupBox_5.setObjectName("groupBox_5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_8 = QtWidgets.QLabel(self.groupBox_5)
        self.label_8.setObjectName("label_8")
        self.horizontalLayout_6.addWidget(self.label_8)
        spacerItem14 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem14)
        self.checkBox_showSchematicPreview = QtWidgets.QCheckBox(self.groupBox_5)
        self.checkBox_showSchematicPreview.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_showSchematicPreview.setText("")
        self.checkBox_showSchematicPreview.setChecked(True)
        self.checkBox_showSchematicPreview.setObjectName("checkBox_showSchematicPreview")
        self.horizontalLayout_6.addWidget(self.checkBox_showSchematicPreview)
        self.verticalLayout_3.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_7 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.label_15 = QtWidgets.QLabel(self.groupBox_5)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_7.addWidget(self.label_15)
        spacerItem15 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_7.addItem(spacerItem15)
        self.lineEdit_defaultSchematicSaveFolder = QtWidgets.QLineEdit(self.groupBox_5)
        self.lineEdit_defaultSchematicSaveFolder.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_defaultSchematicSaveFolder.setReadOnly(True)
        self.lineEdit_defaultSchematicSaveFolder.setObjectName("lineEdit_defaultSchematicSaveFolder")
        self.horizontalLayout_7.addWidget(self.lineEdit_defaultSchematicSaveFolder)
        self.pushButton_defaultSchematicSaveFolder = QtWidgets.QPushButton(self.groupBox_5)
        self.pushButton_defaultSchematicSaveFolder.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_defaultSchematicSaveFolder.setObjectName("pushButton_defaultSchematicSaveFolder")
        self.horizontalLayout_7.addWidget(self.pushButton_defaultSchematicSaveFolder)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.verticalLayout_5.addWidget(self.groupBox_5)
        self.groupBox_6 = QtWidgets.QGroupBox(self.tab_saveExport)
        self.groupBox_6.setObjectName("groupBox_6")
        self.verticalLayout_6 = QtWidgets.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.horizontalLayout_8 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.label_16 = QtWidgets.QLabel(self.groupBox_6)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_8.addWidget(self.label_16)
        spacerItem16 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem16)
        self.checkBox_showSymbolPreview = QtWidgets.QCheckBox(self.groupBox_6)
        self.checkBox_showSymbolPreview.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.checkBox_showSymbolPreview.setText("")
        self.checkBox_showSymbolPreview.setChecked(True)
        self.checkBox_showSymbolPreview.setObjectName("checkBox_showSymbolPreview")
        self.horizontalLayout_8.addWidget(self.checkBox_showSymbolPreview)
        self.verticalLayout_6.addLayout(self.horizontalLayout_8)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_17 = QtWidgets.QLabel(self.groupBox_6)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_9.addWidget(self.label_17)
        spacerItem17 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem17)
        self.lineEdit_defaultSymbolSaveFolder = QtWidgets.QLineEdit(self.groupBox_6)
        self.lineEdit_defaultSymbolSaveFolder.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_defaultSymbolSaveFolder.setReadOnly(True)
        self.lineEdit_defaultSymbolSaveFolder.setObjectName("lineEdit_defaultSymbolSaveFolder")
        self.horizontalLayout_9.addWidget(self.lineEdit_defaultSymbolSaveFolder)
        self.pushButton_defaultSymbolSaveFolder = QtWidgets.QPushButton(self.groupBox_6)
        self.pushButton_defaultSymbolSaveFolder.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_defaultSymbolSaveFolder.setObjectName("pushButton_defaultSymbolSaveFolder")
        self.horizontalLayout_9.addWidget(self.pushButton_defaultSymbolSaveFolder)
        self.verticalLayout_6.addLayout(self.horizontalLayout_9)
        self.verticalLayout_5.addWidget(self.groupBox_6)
        self.groupBox_7 = QtWidgets.QGroupBox(self.tab_saveExport)
        self.groupBox_7.setObjectName("groupBox_7")
        self.verticalLayout_7 = QtWidgets.QVBoxLayout(self.groupBox_7)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_18 = QtWidgets.QLabel(self.groupBox_7)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_10.addWidget(self.label_18)
        spacerItem18 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem18)
        self.comboBox_defaultExportFormat = QtWidgets.QComboBox(self.groupBox_7)
        self.comboBox_defaultExportFormat.setObjectName("comboBox_defaultExportFormat")
        self.comboBox_defaultExportFormat.addItem("")
        self.comboBox_defaultExportFormat.addItem("")
        self.comboBox_defaultExportFormat.addItem("")
        self.comboBox_defaultExportFormat.addItem("")
        self.comboBox_defaultExportFormat.addItem("")
        self.comboBox_defaultExportFormat.addItem("")
        self.horizontalLayout_10.addWidget(self.comboBox_defaultExportFormat)
        self.verticalLayout_7.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_19 = QtWidgets.QLabel(self.groupBox_7)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_11.addWidget(self.label_19)
        spacerItem19 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_11.addItem(spacerItem19)
        self.lineEdit_defaultExportFolder = QtWidgets.QLineEdit(self.groupBox_7)
        self.lineEdit_defaultExportFolder.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.lineEdit_defaultExportFolder.setReadOnly(True)
        self.lineEdit_defaultExportFolder.setObjectName("lineEdit_defaultExportFolder")
        self.horizontalLayout_11.addWidget(self.lineEdit_defaultExportFolder)
        self.pushButton_defaultExportFolder = QtWidgets.QPushButton(self.groupBox_7)
        self.pushButton_defaultExportFolder.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_defaultExportFolder.setObjectName("pushButton_defaultExportFolder")
        self.horizontalLayout_11.addWidget(self.pushButton_defaultExportFolder)
        self.verticalLayout_7.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_20 = QtWidgets.QLabel(self.groupBox_7)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_12.addWidget(self.label_20)
        spacerItem20 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem20)
        self.doubleSpinBox_exportImageWhitespacePadding = QtWidgets.QDoubleSpinBox(self.groupBox_7)
        self.doubleSpinBox_exportImageWhitespacePadding.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_exportImageWhitespacePadding.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.doubleSpinBox_exportImageWhitespacePadding.setDecimals(1)
        self.doubleSpinBox_exportImageWhitespacePadding.setMinimum(1.0)
        self.doubleSpinBox_exportImageWhitespacePadding.setMaximum(4.0)
        self.doubleSpinBox_exportImageWhitespacePadding.setSingleStep(0.1)
        self.doubleSpinBox_exportImageWhitespacePadding.setProperty("value", 1.1)
        self.doubleSpinBox_exportImageWhitespacePadding.setObjectName("doubleSpinBox_exportImageWhitespacePadding")
        self.horizontalLayout_12.addWidget(self.doubleSpinBox_exportImageWhitespacePadding)
        self.verticalLayout_7.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_21 = QtWidgets.QLabel(self.groupBox_7)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_13.addWidget(self.label_21)
        spacerItem21 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem21)
        self.doubleSpinBox_exportImageScaleFactor = QtWidgets.QDoubleSpinBox(self.groupBox_7)
        self.doubleSpinBox_exportImageScaleFactor.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.doubleSpinBox_exportImageScaleFactor.setCorrectionMode(QtWidgets.QAbstractSpinBox.CorrectToNearestValue)
        self.doubleSpinBox_exportImageScaleFactor.setDecimals(1)
        self.doubleSpinBox_exportImageScaleFactor.setMinimum(1.0)
        self.doubleSpinBox_exportImageScaleFactor.setMaximum(4.0)
        self.doubleSpinBox_exportImageScaleFactor.setSingleStep(0.1)
        self.doubleSpinBox_exportImageScaleFactor.setProperty("value", 2.0)
        self.doubleSpinBox_exportImageScaleFactor.setObjectName("doubleSpinBox_exportImageScaleFactor")
        self.horizontalLayout_13.addWidget(self.doubleSpinBox_exportImageScaleFactor)
        self.verticalLayout_7.addLayout(self.horizontalLayout_13)
        self.verticalLayout_5.addWidget(self.groupBox_7)
        spacerItem22 = QtWidgets.QSpacerItem(20, 27, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_5.addItem(spacerItem22)
        self.tabWidget.addTab(self.tab_saveExport, "")
        self.verticalLayout_8.addWidget(self.tabWidget)
        self.label_4 = QtWidgets.QLabel(Dialog)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setWordWrap(True)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_8.addWidget(self.label_4)
        spacerItem23 = QtWidgets.QSpacerItem(20, 307, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem23)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem24 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem24)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Apply|QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setCenterButtons(False)
        self.buttonBox.setObjectName("buttonBox")
        self.horizontalLayout_3.addWidget(self.buttonBox)
        self.verticalLayout_8.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        self.comboBox_penWidth.setCurrentIndex(1)
        self.comboBox_penStyle.setCurrentIndex(0)
        self.comboBox_penColour.setCurrentIndex(0)
        self.comboBox_brushColour.setCurrentIndex(0)
        self.comboBox_brushStyle.setCurrentIndex(0)
        self.comboBox_gridSnapToGridSpacing.setCurrentIndex(3)
        self.comboBox_gridMinorGridPointSpacing.setCurrentIndex(4)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Options"))
        self.groupBox.setTitle(_translate("Dialog", "Pen"))
        self.label_2.setText(_translate("Dialog", "Default colour"))
        self.comboBox_penWidth.setItemText(0, _translate("Dialog", "2"))
        self.comboBox_penWidth.setItemText(1, _translate("Dialog", "4"))
        self.comboBox_penWidth.setItemText(2, _translate("Dialog", "6"))
        self.comboBox_penWidth.setItemText(3, _translate("Dialog", "8"))
        self.comboBox_penWidth.setItemText(4, _translate("Dialog", "10"))
        self.label_3.setText(_translate("Dialog", "Default style"))
        self.comboBox_penStyle.setItemText(0, _translate("Dialog", "Solid"))
        self.comboBox_penStyle.setItemText(1, _translate("Dialog", "Dash"))
        self.comboBox_penStyle.setItemText(2, _translate("Dialog", "Dot"))
        self.comboBox_penStyle.setItemText(3, _translate("Dialog", "Dash-dot"))
        self.comboBox_penStyle.setItemText(4, _translate("Dialog", "Dash-dot-dot"))
        self.comboBox_penColour.setItemText(0, _translate("Dialog", "Black"))
        self.comboBox_penColour.setItemText(1, _translate("Dialog", "Red"))
        self.comboBox_penColour.setItemText(2, _translate("Dialog", "Blue"))
        self.comboBox_penColour.setItemText(3, _translate("Dialog", "Green"))
        self.comboBox_penColour.setItemText(4, _translate("Dialog", "Cyan"))
        self.comboBox_penColour.setItemText(5, _translate("Dialog", "Magenta"))
        self.comboBox_penColour.setItemText(6, _translate("Dialog", "Yellow"))
        self.label.setText(_translate("Dialog", "Default width"))
        self.groupBox_2.setTitle(_translate("Dialog", "Brush"))
        self.label_9.setText(_translate("Dialog", "Default colour"))
        self.comboBox_brushColour.setItemText(0, _translate("Dialog", "Black"))
        self.comboBox_brushColour.setItemText(1, _translate("Dialog", "Red"))
        self.comboBox_brushColour.setItemText(2, _translate("Dialog", "Blue"))
        self.comboBox_brushColour.setItemText(3, _translate("Dialog", "Green"))
        self.comboBox_brushColour.setItemText(4, _translate("Dialog", "Cyan"))
        self.comboBox_brushColour.setItemText(5, _translate("Dialog", "Magenta"))
        self.comboBox_brushColour.setItemText(6, _translate("Dialog", "Yellow"))
        self.label_10.setText(_translate("Dialog", "Default style"))
        self.comboBox_brushStyle.setItemText(0, _translate("Dialog", "No fill"))
        self.comboBox_brushStyle.setItemText(1, _translate("Dialog", "Solid"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_printing), _translate("Dialog", "Painting"))
        self.label_11.setText(_translate("Dialog", "Visibility"))
        self.groupBox_3.setTitle(_translate("Dialog", "Snapping"))
        self.label_14.setText(_translate("Dialog", "Snap to grid"))
        self.label_7.setText(_translate("Dialog", "Snap to grid spacing"))
        self.comboBox_gridSnapToGridSpacing.setItemText(0, _translate("Dialog", "1"))
        self.comboBox_gridSnapToGridSpacing.setItemText(1, _translate("Dialog", "2"))
        self.comboBox_gridSnapToGridSpacing.setItemText(2, _translate("Dialog", "5"))
        self.comboBox_gridSnapToGridSpacing.setItemText(3, _translate("Dialog", "10"))
        self.comboBox_gridSnapToGridSpacing.setItemText(4, _translate("Dialog", "20"))
        self.comboBox_gridSnapToGridSpacing.setItemText(5, _translate("Dialog", "30"))
        self.comboBox_gridSnapToGridSpacing.setItemText(6, _translate("Dialog", "40"))
        self.groupBox_4.setTitle(_translate("Dialog", "Major and minor points"))
        self.label_12.setText(_translate("Dialog", "Show major grid points"))
        self.label_13.setText(_translate("Dialog", "Major grid point spacing"))
        self.comboBox_gridMajorGridPointSpacing.setItemText(0, _translate("Dialog", "100"))
        self.comboBox_gridMajorGridPointSpacing.setItemText(1, _translate("Dialog", "200"))
        self.comboBox_gridMajorGridPointSpacing.setItemText(2, _translate("Dialog", "300"))
        self.comboBox_gridMajorGridPointSpacing.setItemText(3, _translate("Dialog", "400"))
        self.label_6.setText(_translate("Dialog", "Show minor grid points"))
        self.label_5.setText(_translate("Dialog", "Minor grid point spacing"))
        self.comboBox_gridMinorGridPointSpacing.setItemText(0, _translate("Dialog", "1"))
        self.comboBox_gridMinorGridPointSpacing.setItemText(1, _translate("Dialog", "2"))
        self.comboBox_gridMinorGridPointSpacing.setItemText(2, _translate("Dialog", "5"))
        self.comboBox_gridMinorGridPointSpacing.setItemText(3, _translate("Dialog", "10"))
        self.comboBox_gridMinorGridPointSpacing.setItemText(4, _translate("Dialog", "20"))
        self.comboBox_gridMinorGridPointSpacing.setItemText(5, _translate("Dialog", "30"))
        self.comboBox_gridMinorGridPointSpacing.setItemText(6, _translate("Dialog", "40"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_grid), _translate("Dialog", "Grid"))
        self.groupBox_5.setTitle(_translate("Dialog", "Schematic"))
        self.label_8.setText(_translate("Dialog", "Show previews in save/load dialogs"))
        self.checkBox_showSchematicPreview.setToolTip(_translate("Dialog", "Disable this if there are folders with many schematics which might be significantly slowed down in the load/save dialogs"))
        self.label_15.setText(_translate("Dialog", "Default save folder"))
        self.lineEdit_defaultSchematicSaveFolder.setText(_translate("Dialog", "./"))
        self.pushButton_defaultSchematicSaveFolder.setText(_translate("Dialog", "..."))
        self.groupBox_6.setTitle(_translate("Dialog", "Symbol"))
        self.label_16.setText(_translate("Dialog", "Show previews in save/load dialogs"))
        self.checkBox_showSymbolPreview.setToolTip(_translate("Dialog", "Disable this if there are folders with many symbols which might be significantly slowed down in the load/save dialogs"))
        self.label_17.setText(_translate("Dialog", "Default save folder"))
        self.lineEdit_defaultSymbolSaveFolder.setText(_translate("Dialog", "Resources/Symbols/Custom"))
        self.pushButton_defaultSymbolSaveFolder.setText(_translate("Dialog", "..."))
        self.groupBox_7.setTitle(_translate("Dialog", "Export"))
        self.label_18.setText(_translate("Dialog", "Default format"))
        self.comboBox_defaultExportFormat.setItemText(0, _translate("Dialog", "PDF"))
        self.comboBox_defaultExportFormat.setItemText(1, _translate("Dialog", "SVG"))
        self.comboBox_defaultExportFormat.setItemText(2, _translate("Dialog", "PNG"))
        self.comboBox_defaultExportFormat.setItemText(3, _translate("Dialog", "JPG"))
        self.comboBox_defaultExportFormat.setItemText(4, _translate("Dialog", "BMP"))
        self.comboBox_defaultExportFormat.setItemText(5, _translate("Dialog", "TIFF"))
        self.label_19.setText(_translate("Dialog", "Default folder"))
        self.lineEdit_defaultExportFolder.setText(_translate("Dialog", "./"))
        self.pushButton_defaultExportFolder.setText(_translate("Dialog", "..."))
        self.label_20.setText(_translate("Dialog", "Whitespace padding"))
        self.doubleSpinBox_exportImageWhitespacePadding.setToolTip(_translate("Dialog", "Sets the scaling factor of the overall exported image to the tight bounding box of elements within the scene. The difference between the two sizes is effectively the whitespace near the edges of the image."))
        self.label_21.setText(_translate("Dialog", "Scale factor (only for raster formats)"))
        self.doubleSpinBox_exportImageScaleFactor.setToolTip(_translate("Dialog", "Sets the scaling factor of the exported image. You can tune this value to tradeoff speed of export with the resolution of the resultant images."))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_saveExport), _translate("Dialog", "Save/Export"))
        self.label_4.setText(_translate("Dialog", "Note: These values are defaults that will be used when the program restarts. To change these values for just the current session, please use the Edit menu."))

