from PyQt5 import QtCore, QtGui, QtWidgets
from .gui.ycircuit_optionsWindow import Ui_Dialog
import os


class MyOptionsWindow(QtWidgets.QDialog):
    """This class takes care of the options in YCircuit."""

    applied = QtCore.pyqtSignal()

    def __init__(self, parent=None, settingsFileName=None):
        """Initializes the object and various parameters to default values"""
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        if settingsFileName is not None:
            self.fileName = settingsFileName
        else:
            self.fileName = '.config'
        self.settings = QtCore.QSettings(self.fileName, QtCore.QSettings.IniFormat)
        self.readValues()

        self.ui.buttonBox.accepted.connect(self.accept)
        self.ui.buttonBox.rejected.connect(self.reject)
        self.ui.buttonBox.button(self.ui.buttonBox.Apply).clicked.connect(self.writeValues)
        self.ui.buttonBox.button(self.ui.buttonBox.Apply).clicked.connect(lambda: self.applied.emit())

        self.ui.pushButton_defaultSchematicSaveFolder.clicked.connect(self.changeDefaultSchematicSaveFolder)
        self.ui.pushButton_defaultSymbolSaveFolder.clicked.connect(self.changeDefaultSymbolSaveFolder)
        self.ui.pushButton_defaultSymbolPreviewFolder.clicked.connect(self.changeDefaultSymbolPreviewFolder)
        self.ui.pushButton_defaultExportFolder.clicked.connect(self.changeDefaultExportFolder)

    def accept(self):
        self.writeValues()
        super().accept()

    def reject(self):
        super().reject()

    def readValues(self):
        if not os.path.isfile(self.fileName):
            self.createSettingsFile()
        # Read from the newly created settings file
        # Font settings
        self.ui.fontComboBox_fontFamily.setCurrentText(self.settings.value('Painting/Font/Family'))
        self.ui.comboBox_fontPointSize.setCurrentText(self.settings.value('Painting/Font/Point size'))
        # Painting pen settings
        self.ui.comboBox_penWidth.setCurrentText(self.settings.value('Painting/Pen/Width'))
        self.ui.comboBox_penColour.setCurrentText(self.settings.value('Painting/Pen/Colour'))
        self.ui.comboBox_penStyle.setCurrentText(self.settings.value('Painting/Pen/Style'))
        # Painting brush settings
        self.ui.comboBox_brushColour.setCurrentText(self.settings.value('Painting/Brush/Colour'))
        self.ui.comboBox_brushStyle.setCurrentText(self.settings.value('Painting/Brush/Style'))
        # Rotation settings
        self.ui.comboBox_rotationDirection.setCurrentText(self.settings.value('Painting/Rotation/Direction'))
        self.ui.spinBox_rotationAngle.setValue(self.settings.value('Painting/Rotation/Angle', type=int))

        # Grid settings
        self.ui.checkBox_gridVisibility.setChecked(self.settings.value('Grid/Visibility', type=bool))
        # Snap settings
        self.ui.checkBox_gridSnapToGrid.setChecked(self.settings.value('Grid/Snapping/Snap to grid', type=bool))
        self.ui.comboBox_gridSnapToGridSpacing.setCurrentText(self.settings.value('Grid/Snapping/Snap to grid spacing', type=str))
        # Major grid point settings
        self.ui.checkBox_gridShowMajorGridPoints.setChecked(self.settings.value('Grid/Major and minor grid points/Major grid points visibility', type=bool))
        self.ui.comboBox_gridMajorGridPointSpacing.setCurrentText(self.settings.value('Grid/Major and minor grid points/Major grid points spacing'))
        # Minor grid point settings
        self.ui.checkBox_gridShowMinorGridPoints.setChecked(self.settings.value('Grid/Major and minor grid points/Minor grid points visibility', type=bool))
        self.ui.comboBox_gridMinorGridPointSpacing.setCurrentText(self.settings.value('Grid/Major and minor grid points/Minor grid points spacing'))

        # Save/export settings
        self.ui.checkBox_autobackupEnable.setChecked(self.settings.value('SaveExport/Autobackup/Enable', type=bool))
        self.ui.spinBox_autobackupTimerInterval.setValue(self.settings.value('SaveExport/Autobackup/Timer interval', type=int))
        self.ui.checkBox_showSchematicPreview.setChecked(self.settings.value('SaveExport/Schematic/Show preview', type=bool))
        self.ui.lineEdit_defaultSchematicSaveFolder.setText(self.settings.value('SaveExport/Schematic/Default save folder'))
        self.ui.checkBox_showSymbolPreview.setChecked(self.settings.value('SaveExport/Symbol/Show preview', type=bool))
        self.ui.lineEdit_defaultSymbolSaveFolder.setText(self.settings.value('SaveExport/Symbol/Default save folder'))
        self.ui.lineEdit_defaultSymbolPreviewFolder.setText(self.settings.value('SaveExport/Symbol/Default preview folder'))
        self.ui.comboBox_defaultExportFormat.setCurrentText(self.settings.value('SaveExport/Export/Default format'))
        self.ui.lineEdit_defaultExportFolder.setText(self.settings.value('SaveExport/Export/Default folder'))
        self.ui.doubleSpinBox_exportImageWhitespacePadding.setValue(self.settings.value('SaveExport/Export/Whitespace padding', type=float))
        self.ui.doubleSpinBox_exportImageScaleFactor.setValue(self.settings.value('SaveExport/Export/Image scale factor', type=float))

    def writeValues(self):
        # Font settings
        self.settings.setValue('Painting/Font/Family', self.ui.fontComboBox_fontFamily.currentText())
        self.settings.setValue('Painting/Font/Point size', self.ui.comboBox_fontPointSize.currentText())
        # Painting pen settings
        self.settings.setValue('Painting/Pen/Width', self.ui.comboBox_penWidth.currentText())
        self.settings.setValue('Painting/Pen/Colour', self.ui.comboBox_penColour.currentText())
        self.settings.setValue('Painting/Pen/Style', self.ui.comboBox_penStyle.currentText())
        # Painting brush settings
        self.settings.setValue('Painting/Brush/Colour', self.ui.comboBox_brushColour.currentText())
        self.settings.setValue('Painting/Brush/Style', self.ui.comboBox_brushStyle.currentText())
        # Rotation settings
        self.settings.setValue('Painting/Rotation/Direction', self.ui.comboBox_rotationDirection.currentText())
        self.settings.setValue('Painting/Rotation/Angle', self.ui.spinBox_rotationAngle.value())

        # Grid settings
        self.settings.setValue('Grid/Visibility', self.ui.checkBox_gridVisibility.isChecked())
        # Snapping settings
        self.settings.setValue('Grid/Snapping/Snap to grid', self.ui.checkBox_gridSnapToGrid.isChecked())
        self.settings.setValue('Grid/Snapping/Snap to grid spacing', self.ui.comboBox_gridSnapToGridSpacing.currentText())
        # Major grid point settings
        self.settings.setValue('Grid/Major and minor grid points/Major grid points visibility', self.ui.checkBox_gridShowMajorGridPoints.isChecked())
        self.settings.setValue('Grid/Major and minor grid points/Major grid points spacing', self.ui.comboBox_gridMajorGridPointSpacing.currentText())
        # Minor grid point settings
        self.settings.setValue('Grid/Major and minor grid points/Minor grid points visibility', self.ui.checkBox_gridShowMinorGridPoints.isChecked())
        self.settings.setValue('Grid/Major and minor grid points/Minor grid points spacing', self.ui.comboBox_gridMinorGridPointSpacing.currentText())

        # Save/export settings
        self.settings.setValue('SaveExport/Autobackup/Enable', self.ui.checkBox_autobackupEnable.isChecked())
        self.settings.setValue('SaveExport/Autobackup/Timer interval', self.ui.spinBox_autobackupTimerInterval.value())
        self.settings.setValue('SaveExport/Schematic/Show preview', self.ui.checkBox_showSchematicPreview.isChecked())
        self.settings.setValue('SaveExport/Schematic/Default save folder', self.ui.lineEdit_defaultSchematicSaveFolder.text())
        self.settings.setValue('SaveExport/Symbol/Show preview', self.ui.checkBox_showSymbolPreview.isChecked())
        self.settings.setValue('SaveExport/Symbol/Default save folder', self.ui.lineEdit_defaultSymbolSaveFolder.text())
        self.settings.setValue('SaveExport/Symbol/Default preview folder', self.ui.lineEdit_defaultSymbolPreviewFolder.text())
        self.settings.setValue('SaveExport/Export/Default format', self.ui.comboBox_defaultExportFormat.currentText())
        self.settings.setValue('SaveExport/Export/Default folder', self.ui.lineEdit_defaultExportFolder.text())
        self.settings.setValue('SaveExport/Export/Whitespace padding', self.ui.doubleSpinBox_exportImageWhitespacePadding.text())
        self.settings.setValue('SaveExport/Export/Image scale factor', self.ui.doubleSpinBox_exportImageScaleFactor.text())

        # Sync changes to disk
        self.settings.sync()

    def createSettingsFile(self):
        # Painting settings
        self.settings.beginGroup('Painting')
        # Font settings
        self.settings.beginGroup('Font')
        self.settings.setValue('Family', 'Arial')
        self.settings.setValue('Point size', '10')
        self.settings.endGroup()
        # Painting pen settings
        self.settings.beginGroup('Pen')
        self.settings.setValue('Width', '4')
        self.settings.setValue('Colour', 'Black')
        self.settings.setValue('Style', 'Solid')
        self.settings.endGroup()
        # Painting brush settings
        self.settings.beginGroup('Brush')
        self.settings.setValue('Colour', 'Black')
        self.settings.setValue('Style', 'No fill')
        self.settings.endGroup()
        self.settings.beginGroup('Rotation')
        self.settings.setValue('Direction', 'Clockwise')
        self.settings.setValue('Angle', '45')
        self.settings.endGroup()
        self.settings.endGroup()

        # Grid settings
        self.settings.beginGroup('Grid')
        self.settings.setValue('Visibility', True)
        # Snapping settings
        self.settings.beginGroup('Snapping')
        self.settings.setValue('Snap to grid', True)
        self.settings.setValue('Snap to grid spacing', '10')
        self.settings.endGroup()
        # Major grid point settings
        self.settings.beginGroup('Major and minor grid points')
        self.settings.setValue('Major grid points visibility', True)
        self.settings.setValue('Major grid points spacing', '100')
        # Minor grid point settings
        self.settings.setValue('Minor grid points visibility', True)
        self.settings.setValue('Minor grid points spacing', '20')
        self.settings.endGroup()
        self.settings.endGroup()

        # Save/export settings
        self.settings.beginGroup('SaveExport')
        self.settings.beginGroup('Autobackup')
        self.settings.setValue('Enable', True)
        self.settings.setValue('Timer interval', '10')
        self.settings.endGroup()
        self.settings.beginGroup('Schematic')
        self.settings.setValue('Show preview', True)
        self.settings.setValue('Default save folder', './')
        self.settings.endGroup()
        self.settings.beginGroup('Symbol')
        self.settings.setValue('Show preview', True)
        self.settings.setValue('Default save folder', 'Resources/Symbols/Custom/')
        self.settings.setValue('Default preview folder', 'Resources/Symbols/Standard/')
        self.settings.endGroup()
        self.settings.beginGroup('Export')
        self.settings.setValue('Default format', 'pdf')
        self.settings.setValue('Default folder', './')
        self.settings.setValue('Whitespace padding', '1.1')
        self.settings.setValue('Image scale factor', '2.0')
        self.settings.endGroup()
        self.settings.endGroup()

        # Write data to disk
        self.settings.sync()

    def changeDefaultSchematicSaveFolder(self):
        fileDialog = QtWidgets.QFileDialog()
        defaultFolder = self.ui.lineEdit_defaultSchematicSaveFolder.text()
        defaultFolder = fileDialog.getExistingDirectory(self, 'Choose default schematic save folder', defaultFolder)
        dir_ = QtCore.QDir('./')
        if defaultFolder != '':
            self.ui.lineEdit_defaultSchematicSaveFolder.setText(dir_.relativeFilePath(defaultFolder))

    def changeDefaultSymbolSaveFolder(self):
        fileDialog = QtWidgets.QFileDialog()
        defaultFolder = self.ui.lineEdit_defaultSymbolSaveFolder.text()
        defaultFolder = fileDialog.getExistingDirectory(self, 'Choose default symbol save folder', defaultFolder)
        dir_ = QtCore.QDir('./')
        if defaultFolder != '':
            self.ui.lineEdit_defaultSymbolSaveFolder.setText(dir_.relativeFilePath(defaultFolder))

    def changeDefaultSymbolPreviewFolder(self):
        fileDialog = QtWidgets.QFileDialog()
        defaultFolder = self.ui.lineEdit_defaultSymbolPreviewFolder.text()
        defaultFolder = fileDialog.getExistingDirectory(self, 'Choose default symbol preview folder', defaultFolder)
        dir_ = QtCore.QDir('./')
        if defaultFolder != '':
            self.ui.lineEdit_defaultSymbolPreviewFolder.setText(dir_.relativeFilePath(defaultFolder))

    def changeDefaultExportFolder(self):
        fileDialog = QtWidgets.QFileDialog()
        defaultFolder = self.ui.lineEdit_defaultExportFolder.text()
        defaultFolder = fileDialog.getExistingDirectory(self, 'Choose default export folder', defaultFolder)
        dir_ = QtCore.QDir('./')
        if defaultFolder != '':
            self.ui.lineEdit_defaultExportFolder.setText(dir_.relativeFilePath(defaultFolder))
