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

    def accept(self):
        self.writeValues()
        super().accept()

    def reject(self):
        super().reject()

    def readValues(self):
        if not os.path.isfile(self.fileName):
            self.createSettingsFile()
        # Read from the newly created settings file
        # Painting pen settings
        self.ui.comboBox_penWidth.setCurrentText(self.settings.value('Painting/Pen/Width'))
        self.ui.comboBox_penColour.setCurrentText(self.settings.value('Painting/Pen/Colour'))
        self.ui.comboBox_penStyle.setCurrentText(self.settings.value('Painting/Pen/Style'))
        # Painting brush settings
        self.ui.comboBox_brushColour.setCurrentText(self.settings.value('Painting/Brush/Colour'))
        self.ui.comboBox_brushStyle.setCurrentText(self.settings.value('Painting/Brush/Style'))

        # Grid settings
        self.ui.checkBox_gridVisibility.setChecked(self.settings.value('Grid/Visibility', type=bool))
        # Snap settings
        self.ui.checkBox_gridSnapToGrid.setChecked(self.settings.value('Grid/Snapping/Snap to grid', type=bool))
        self.ui.comboBox_gridSnapToGridSpacing.setCurrentText(str(self.settings.value('Grid/Snapping/Snap to grid spacing')))
        # Major grid point settings
        self.ui.checkBox_gridShowMajorGridPoints.setChecked(self.settings.value('Grid/Major and minor grid points/Major grid points visibility', type=bool))
        self.ui.comboBox_gridMajorGridPointSpacing.setCurrentText(str(self.settings.value('Grid/Major and minor grid points/Major grid points spacing')))
        # Minor grid point settings
        self.ui.checkBox_gridShowMinorGridPoints.setChecked(self.settings.value('Grid/Major and minor grid points/Minor grid points visibility', type=bool))
        self.ui.comboBox_gridMinorGridPointSpacing.setCurrentText(str(self.settings.value('Grid/Major and minor grid points/Minor grid points spacing')))

        # Save/export settings
        self.ui.checkBox_showSchematicPreview.setChecked(self.settings.value('SaveExport/Schematic/Show schematic preview', type=bool))
        self.ui.lineEdit_defaultSchematicSaveFolder.setText(self.settings.value('SaveExport/Schematic/Default schematic save folder'))
        self.ui.checkBox_showSymbolPreview.setChecked(self.settings.value('SaveExport/Symbol/Show symbol preview', type=bool))
        self.ui.lineEdit_defaultSymbolSaveFolder.setText(self.settings.value('SaveExport/Symbol/Default symbol save folder'))

    def writeValues(self):
        # Painting pen settings
        self.settings.setValue('Painting/Pen/Width', str(self.ui.comboBox_penWidth.currentText()))
        self.settings.setValue('Painting/Pen/Colour', str(self.ui.comboBox_penColour.currentText()))
        self.settings.setValue('Painting/Pen/Style', str(self.ui.comboBox_penStyle.currentText()))
        # Painting brush settings
        self.settings.setValue('Painting/Brush/Colour', str(self.ui.comboBox_brushColour.currentText()))
        self.settings.setValue('Painting/Brush/Style', str(self.ui.comboBox_brushStyle.currentText()))

        # Grid settings
        self.settings.setValue('Grid/Visibility', self.ui.checkBox_gridVisibility.isChecked())
        # Snapping settings
        self.settings.setValue('Grid/Snapping/Snap to grid', self.ui.checkBox_gridSnapToGrid.isChecked())
        self.settings.setValue('Grid/Snapping/Snap to grid spacing', int(self.ui.comboBox_gridSnapToGridSpacing.currentText()))
        # Major grid point settings
        self.settings.setValue('Grid/Major and minor grid points/Major grid points visibility', self.ui.checkBox_gridShowMajorGridPoints.isChecked())
        self.settings.setValue('Grid/Major and minor grid points/Major grid points spacing', int(self.ui.comboBox_gridMajorGridPointSpacing.currentText()))
        # Minor grid point settings
        self.settings.setValue('Grid/Major and minor grid points/Minor grid points visibility', self.ui.checkBox_gridShowMinorGridPoints.isChecked())
        self.settings.setValue('Grid/Major and minor grid points/Minor grid points spacing', int(self.ui.comboBox_gridMinorGridPointSpacing.currentText()))

        # Save/export settings
        self.settings.setValue('SaveExport/Schematic/Show schematic preview', self.ui.checkBox_showSchematicPreview.isChecked())
        self.settings.setValue('SaveExport/Schematic/Default schematic save folder', str(self.ui.lineEdit_defaultSchematicSaveFolder.text()))
        self.settings.setValue('SaveExport/Symbol/Show symbol preview', self.ui.checkBox_showSymbolPreview.isChecked())
        self.settings.setValue('SaveExport/Symbol/Default symbol save folder', str(self.ui.lineEdit_defaultSymbolSaveFolder.text()))

        # Sync changes to disk
        self.settings.sync()

    def createSettingsFile(self):
        # Painting settings
        self.settings.beginGroup('Painting')
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
        self.settings.endGroup()

        # Grid settings
        self.settings.beginGroup('Grid')
        self.settings.setValue('Visibility', True)
        # Snapping settings
        self.settings.beginGroup('Snapping')
        self.settings.setValue('Snap to grid', True)
        self.settings.setValue('Snap to grid spacing', 10)
        self.settings.endGroup()
        # Major grid point settings
        self.settings.beginGroup('Major and minor grid points')
        self.settings.setValue('Major grid points visibility', True)
        self.settings.setValue('Major grid points spacing', 100)
        # Minor grid point settings
        self.settings.setValue('Minor grid points visibility', True)
        self.settings.setValue('Minor grid points spacing', 20)
        self.settings.endGroup()
        self.settings.endGroup()

        # Save/export settings
        self.settings.beginGroup('SaveExport')
        self.settings.beginGroup('Schematic')
        self.settings.setValue('Show schematic preview', True)
        self.settings.setValue('Default schematic save folder', './')
        self.settings.endGroup()
        self.settings.beginGroup('Symbol')
        self.settings.setValue('Show symbol preview', True)
        self.settings.setValue('Default symbol save folder', 'Resources/Symbols/Custom/')
        self.settings.endGroup()
        self.settings.endGroup()

        # Write data to disk
        self.settings.sync()

    def changeDefaultSchematicSaveFolder(self):
        fileDialog = QtWidgets.QFileDialog()
        defaultFolder = fileDialog.getExistingDirectory(self, 'Choose default schematic save folder', './')
        dir_ = QtCore.QDir('./')
        if defaultFolder != '':
            self.ui.lineEdit_defaultSchematicSaveFolder.setText(dir_.relativeFilePath(defaultFolder))

    def changeDefaultSymbolSaveFolder(self):
        fileDialog = QtWidgets.QFileDialog()
        defaultFolder = fileDialog.getExistingDirectory(self, 'Choose default symbol save folder', 'Resources/Symbols/Custom/')
        dir_ = QtCore.QDir('./')
        if defaultFolder != '':
            self.ui.lineEdit_defaultSymbolSaveFolder.setText(dir_.relativeFilePath(defaultFolder))
