from PyQt5 import QtCore, QtGui, QtWidgets
from .components import myGraphicsItemGroup
# from .drawingitems import myFileDialog
# import os

class DrawingAreaPreview(QtWidgets.QGraphicsView):
    """The drawing area preview is subclassed from QGraphicsView to provide
    additional functionality such as highlighting the currently viewed area
    etc."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.visibleRect = QtCore.QRectF()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QtGui.QPainter(self.viewport())
        pen = QtGui.QPen()
        pen.setColor(QtGui.QColor('black'))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(self.visibleRect)
        self.drawForeground(painter, self.visibleRect)

    def fitToViewRoutine(self):
        """Resizes viewport so that all items drawn are visible"""
        if len(self.scene().items()) == 1:
            # Fit to (0, 0, 800, 800) if nothing is present
            rect = QtCore.QRectF(0, 0, 800, 800)
            self.fitInView(rect, QtCore.Qt.KeepAspectRatio)
        else:
            self.fitInView(self.scene().itemsBoundingRect(), QtCore.Qt.KeepAspectRatio)

    def updateVisibleRect(self):
        self.visibleRect = self.drawingArea.mapToScene(self.drawingArea.viewport().geometry()).boundingRect()
        self.visibleRect = QtCore.QRectF(self.mapFromScene(self.visibleRect).boundingRect())
        self.fitToViewRoutine()

    def hidePins(self, hide=True):
        """Toggles visibility of pins on symbols"""
        show = not hide
        for item in self.scene().items():
            if isinstance(item, myGraphicsItemGroup):
                item.pinVisibility(show)


class ExportWindow(QtWidgets.QDialog):
    """This dialog implements the export preview."""

    def __init__(self, parent=None, scene=None, **kwargs):
        """Initializes the object and various parameters to default values"""
        from .gui.ycircuit_exportWindow import Ui_Dialog
        super().__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.parentView = parent
        self.ui.graphicsView_exportPreview.setScene(scene)
        self.dimensions = {
            'width': 400,
            'height': 400
        }
        self.ui.label_exportDimensions.units = 'in'

        self.ui.comboBox_exportFormat.activated.connect(
            self.comboBox_exportFormat_currentIndexChanged)
        self.ui.doubleSpinBox_exportImageWhitespacePadding.valueChanged.connect(
            self.updatePreview)
        self.ui.doubleSpinBox_exportImageScaleFactor.valueChanged.connect(
            self.updatePreview)
        self.ui.comboBox_exportQuality.currentIndexChanged.connect(
            self.comboBox_exportQuality_currentIndexChanged)
        self.ui.checkBox_hidePins.clicked.connect(
            self.ui.graphicsView_exportPreview.hidePins)
        self.ui.graphicsView_exportPreview.scene().changed.connect(
            self.updatePreview)
        self.ui.buttonGroup_exportArea.buttonClicked.connect(
            self.buttonGroup_exportArea_buttonClicked)
        if self.parentView._selectedItems == []:
            self.ui.radioButton_exportAreaSelected.setEnabled(False)

        if 'exportFormat' in kwargs:
            self.exportFormat = kwargs['exportFormat']
            self.ui.comboBox_exportFormat.setCurrentText(self.exportFormat.upper())
        if 'exportArea' in kwargs:
            self.exportArea = kwargs['exportArea']
            if self.exportArea == 'full':
                self.ui.radioButton_exportAreaFull.setChecked(True)
            elif self.exportArea == 'selected':
                self.ui.radioButton_exportAreaSelected.setChecked(True)
            else:
                self.ui.radioButton_exportAreaVisible.setChecked(True)
        if 'whitespacePadding' in kwargs:
            self.whitespacePadding = kwargs['whitespacePadding']
            self.ui.doubleSpinBox_exportImageWhitespacePadding.setValue(
                self.whitespacePadding)
        if 'scaleFactor' in kwargs:
            self.scaleFactor = kwargs['scaleFactor']
            self.ui.doubleSpinBox_exportImageScaleFactor.setValue(
                self.scaleFactor)
        if 'quality' in kwargs:
            self.quality = kwargs['quality']
            if self.quality is None:
                self.quality = 50
            self.ui.comboBox_exportQuality.setCurrentText(str(self.quality) + '%')
        if 'hidePins' in kwargs:
            self.hidePins = kwargs['hidePins']
            self.ui.checkBox_hidePins.setChecked(self.hidePins)
        if 'transparentBackground' in kwargs:
            self.transparentBackground = kwargs['transparentBackground']
            self.ui.checkBox_transparentBackground.setChecked(self.transparentBackground)
        self.comboBox_exportFormat_currentIndexChanged()
        self.comboBox_exportQuality_currentIndexChanged()
        self.ui.graphicsView_exportPreview.hidePins(self.ui.checkBox_hidePins.isChecked())
        self.updatePreview()

    def accept(self):
        self.exportFormat = self.ui.comboBox_exportFormat.currentText().lower()
        self.whitespacePadding = self.ui.doubleSpinBox_exportImageWhitespacePadding.value()
        self.scaleFactor = self.ui.doubleSpinBox_exportImageScaleFactor.value()
        self.quality = int(self.ui.comboBox_exportQuality.currentText()[:-1])
        self.hidePins = self.ui.checkBox_hidePins.isChecked()
        self.transparentBackground = self.ui.checkBox_transparentBackground.isChecked()
        if self.ui.radioButton_exportAreaFull.isChecked() is True:
            self.exportArea = 'full'
        elif self.ui.radioButton_exportAreaVisible.isChecked() is True:
            self.exportArea = 'visible'
        elif self.ui.radioButton_exportAreaSelected.isChecked() is True:
            self.exportArea = 'selected'
        super().accept()

    def reject(self):
        self.exportFormat = self.ui.comboBox_exportFormat.currentText().lower()
        self.whitespacePadding = self.ui.doubleSpinBox_exportImageWhitespacePadding.value()
        self.scaleFactor = self.ui.doubleSpinBox_exportImageScaleFactor.value()
        self.quality = int(self.ui.comboBox_exportQuality.currentText()[:-1])
        self.hidePins = self.ui.checkBox_hidePins.isChecked()
        self.transparentBackground = self.ui.checkBox_transparentBackground.isChecked()
        if self.ui.radioButton_exportAreaFull.isChecked() is True:
            self.exportArea = 'full'
        elif self.ui.radioButton_exportAreaVisible.isChecked() is True:
            self.exportArea = 'visible'
        elif self.ui.radioButton_exportAreaSelected.isChecked() is True:
            self.exportArea = 'selected'
        super().reject()

    def comboBox_exportFormat_currentIndexChanged(self):
        _format = self.ui.comboBox_exportFormat.currentText().lower()
        if _format in ['pdf', 'svg']:
            self.ui.doubleSpinBox_exportImageScaleFactor.setEnabled(False)
            self.ui.comboBox_exportQuality.setEnabled(False)
            self.ui.doubleSpinBox_exportImageWhitespacePadding.setEnabled(True)
        elif _format in ['bmp', 'tiff']:
            self.ui.doubleSpinBox_exportImageScaleFactor.setEnabled(True)
            self.ui.comboBox_exportQuality.setEnabled(False)
            self.ui.doubleSpinBox_exportImageWhitespacePadding.setEnabled(True)
        elif _format == 'tex':
            self.ui.doubleSpinBox_exportImageScaleFactor.setEnabled(True)
            self.ui.comboBox_exportQuality.setEnabled(False)
            self.ui.doubleSpinBox_exportImageWhitespacePadding.setEnabled(False)
        else:
            self.ui.doubleSpinBox_exportImageScaleFactor.setEnabled(True)
            self.ui.comboBox_exportQuality.setEnabled(True)
            self.ui.doubleSpinBox_exportImageWhitespacePadding.setEnabled(True)
        if _format in ['png', 'tiff']:
            self.ui.checkBox_transparentBackground.setEnabled(True)
        else:
            self.ui.checkBox_transparentBackground.setEnabled(False)
            self.ui.checkBox_transparentBackground.setChecked(False)
        if _format in ['pdf', 'svg']:
            self.ui.label_exportDimensions.units = 'in'
        elif _format == 'tex':
            self.ui.label_exportDimensions.units = 'cm'
        else:
            self.ui.label_exportDimensions.units = 'px'
        self.exportFormat = _format
        self.buttonGroup_exportArea_buttonClicked()

    def buttonGroup_exportArea_buttonClicked(self):
        if self.ui.radioButton_exportAreaFull.isChecked() is True:
            self.exportArea = 'full'
        elif self.ui.radioButton_exportAreaVisible.isChecked() is True:
            self.exportArea = 'visible'
        elif self.ui.radioButton_exportAreaSelected.isChecked() is True:
            self.exportArea = 'selected'
        if self.exportArea in ['visible', 'selected']:
            self.ui.doubleSpinBox_exportImageWhitespacePadding.setEnabled(False)
            self.ui.doubleSpinBox_exportImageWhitespacePadding.setValue(1)
        else:
            self.ui.doubleSpinBox_exportImageWhitespacePadding.setEnabled(True)
        if self.exportFormat == 'tex':
            self.ui.doubleSpinBox_exportImageWhitespacePadding.setEnabled(False)
        self.updatePreview()

    def comboBox_exportQuality_currentIndexChanged(self):
        self.quality = int(self.ui.comboBox_exportQuality.currentText()[:-1])

    def updatePreview(self):
        self.whitespacePadding = self.ui.doubleSpinBox_exportImageWhitespacePadding.value()
        if self.exportArea == 'full':
            sourceRect = self.ui.graphicsView_exportPreview.scene().itemsBoundingRect()
        elif self.exportArea == 'visible':
            self.whitespacePadding = 1
            sourceRect = self.parentView.mapToScene(self.parentView.viewport().geometry()).boundingRect()
        elif self.exportArea == 'selected':
            self.whitespacePadding = 1
            sourceRect = self.parentView._selectedItems[0].sceneBoundingRect()
            for item in self.parentView._selectedItems:
                sourceRect = sourceRect.united(item.sceneBoundingRect())
        sourceRect.setWidth(int(self.whitespacePadding * sourceRect.width()))
        sourceRect.setHeight(int(self.whitespacePadding * sourceRect.height()))
        width, height = sourceRect.width(), sourceRect.height()
        size = QtCore.QSize(width, height)
        size.scale(275, 275, QtCore.Qt.KeepAspectRatio)
        if width > height:
            size.setWidth(size.height()*width/height)
        else:
            size.setHeight(size.width()*height/width)
        self.ui.graphicsView_exportPreview.setFixedSize(size)
        self.ui.graphicsView_exportPreview.viewport().setFixedSize(size)
        if self.whitespacePadding > 1:
            sourceRect.translate(-width * (self.whitespacePadding - 1) / (self.whitespacePadding * 2.),
                                 -height * (self.whitespacePadding - 1) / (self.whitespacePadding * 2.))
        self.ui.graphicsView_exportPreview.fitInView(sourceRect)
        self.sourceRect = sourceRect
        self.dimensions['width'] = int(width)
        self.dimensions['height'] = int(height)
        self.updateDimensions()

    def updateDimensions(self):
        self.scaleFactor = self.ui.doubleSpinBox_exportImageScaleFactor.value()
        # Convert pixels to inches for PDF and SVG
        if self.exportFormat == 'pdf':
            # 1200 because we use QtPrintSupport.QPrinter.HighResolution
            self.dimensions['width'] = round(self.dimensions['width']/1200, 2)
            self.dimensions['height'] = round(self.dimensions['height']/1200, 2)
        elif self.exportFormat == 'svg':
            # 96 because that is the value set in the export routine
            self.dimensions['width'] = round(self.dimensions['width']/96, 2)
            self.dimensions['height'] = round(self.dimensions['height']/96, 2)
        elif self.exportFormat == 'tex':
            self.dimensions['width'] = round(self.dimensions['width']/100*self.scaleFactor, 2)
            self.dimensions['height'] = round(self.dimensions['height']/100*self.scaleFactor, 2)
        else:
            self.dimensions['width'] = int(self.dimensions['width']*self.scaleFactor)
            self.dimensions['height'] = int(self.dimensions['height']*self.scaleFactor)
        text = str(self.dimensions['width']) + self.ui.label_exportDimensions.units \
            + ' x ' + str(self.dimensions['height']) \
            + self.ui.label_exportDimensions.units
        self.ui.label_exportDimensions.setText(text)
