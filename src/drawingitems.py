from PyQt5 import QtCore, QtGui, QtWidgets
from src.gui.textEditor_gui import Ui_Dialog
import numpy
import pickle
import sympy
from io import BytesIO


class Grid(QtCore.QObject):
    """temp docstring for the Gridclass"""
    def __init__(self, parent=None, view=None, spacing=10):
        super(Grid, self).__init__()
        self.parent = parent
        self.view = view
        self.spacing = spacing
        self.displaySpacing = spacing*10
        self.xLength = 200
        self.yLength = 200
        self.xPoints = numpy.arange(0, self.xLength + self.spacing, self.spacing)
        self.yPoints = numpy.arange(0, self.yLength + self.spacing, self.spacing)

    def createGrid(self, **kwargs):
        if 'spacing' in kwargs:
            self.spacing = kwargs['spacing']
        # displaySpacing has information about how far apart are the major grid points
        self.displaySpacing = 100
        self.xDisplayPoints = self.xPoints[::2]
        self.yDisplayPoints = self.yPoints[::2]
        self.gridPolygonRegular = QtGui.QPolygon()
        for x in self.xDisplayPoints:
            for y in self.yDisplayPoints:
                self.gridPolygonRegular.append(QtCore.QPoint(x, y))
        self.gridPolygonLarge = QtGui.QPolygon()
        # Larger pixels for points on the coarse grid
        for x in self.xDisplayPoints[self.xDisplayPoints % self.displaySpacing == 0]:
            for y in self.yDisplayPoints[self.yDisplayPoints % self.displaySpacing == 0]:
                self.gridPolygonLarge.append(QtCore.QPoint(x, y))

        pix = QtGui.QPixmap(QtCore.QSize(self.xLength, self.yLength))
        # Set background to white
        pix.fill(QtGui.QColor('white'))
        painter = QtGui.QPainter(pix)
        pen = QtGui.QPen()
        pen.setWidth(1.5)
        painter.setPen(pen)
        painter.drawPoints(self.gridPolygonRegular)
        pen.setWidth(3)
        painter.setPen(pen)
        painter.drawPoints(self.gridPolygonLarge)
        painter.end()
        self.view.setBackgroundBrush(QtGui.QBrush(pix))


    def removeGrid(self):
        self.view.setBackgroundBrush(QtGui.QBrush())

    def snapTo(self, point, spacing=None):
        if spacing is None:
            newX = numpy.round(point.x()/self.spacing)*self.spacing
            newY = numpy.round(point.y()/self.spacing)*self.spacing
        else:
            newX = numpy.round(point.x()/spacing)*spacing
            newY = numpy.round(point.y()/spacing)*spacing
        return QtCore.QPointF(newX, newY)


class TextEditor(QtWidgets.QDialog):
    def __init__(self, textBox=None):
        super(TextEditor, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.textBox = textBox

        self.ui.textEdit.setFocus(True)
        if self.textBox is not None:
            font = self.textBox.font()
            self.ui.textEdit.setFont(font)
            self.ui.textEdit.setTextColor(QtGui.QColor(self.textBox.localPenColour))
            if self.textBox.latexExpression is None:
                self.ui.textEdit.setHtml(self.textBox.toHtml())
            else:
                plainText = '$' + self.textBox.latexExpression + '$'
                self.ui.textEdit.setPlainText(plainText)
                self.ui.pushButton_latex.setChecked(True)
                cursor = self.ui.textEdit.textCursor()
                cursor.setPosition(1)
                self.ui.textEdit.setTextCursor(cursor)
                if hasattr(self.textBox, 'latexImageBinary'):
                    if not hasattr(self.textBox, 'data64'):
                        img = QtGui.QImage()
                        img.loadFromData(self.textBox.latexImageBinary.getvalue(), format='png')
                        data = QtCore.QByteArray()
                        buf = QtCore.QBuffer(data)
                        img.save(buf, format='png')
                        self.textBox.data64 = str(data.toBase64())
                else:
                    self.textBox.latexImageBinary, self.base64 = self.mathTexToQImage(plainText, self.font().pointSize(), self.textBox.localPenColour)
                htmlString = '<img src="data:image/png;base64, ' + self.textBox.data64 + '">'
                self.textBox.latexImageHtml = htmlString
                self.textBox.setHtml(htmlString)

        self.ui.textEdit.cursorPositionChanged.connect(self.modifyPushButtons)
        self.ui.textEdit.textChanged.connect(self.latexDollarDecorators)

        QtWidgets.QShortcut('Ctrl+Return', self).activated.connect(self.accept)

        self.ui.pushButton_bold.clicked.connect(self.modifyText)
        self.ui.pushButton_italic.clicked.connect(self.modifyText)
        self.ui.pushButton_underline.clicked.connect(self.modifyText)
        self.ui.pushButton_overline.clicked.connect(self.modifyText)
        self.ui.pushButton_subscript.clicked.connect(self.modifyText)
        self.ui.pushButton_superscript.clicked.connect(self.modifyText)
        self.ui.pushButton_symbol.clicked.connect(self.modifyText)
        self.ui.pushButton_latex.clicked.connect(self.modifyText)

    def accept(self):
        plainText = self.ui.textEdit.toPlainText()
        if self.ui.pushButton_latex.isChecked():
            self.textBox.latexImageBinary, self.textBox.data64 = self.mathTexToQImage(plainText, self.font().pointSize(), self.textBox.localPenColour)
            htmlString = '<img src="data:image/png;base64, ' + self.textBox.data64 + '">'
            self.textBox.latexImageHtml = htmlString
            self.textBox.latexExpression = plainText[1:-1]  # Skip $'s
            self.textBox.setHtml(htmlString)
        else:
            self.textBox.setHtml(self.ui.textEdit.toHtml())
            self.textBox.latexImageHtml = None
            self.textBox.latexExpression= None
        super(TextEditor, self).accept()

    def modifyPushButtons(self):
        cursor = self.ui.textEdit.textCursor()
        format = cursor.charFormat()
        bold, italic, underline, overline = True, True, True, True
        subscript, superscript, symbol = True, True, True
        latex = self.ui.pushButton_latex.isChecked()
        if latex is not True:
            if cursor.hasSelection() is True:
                start, end = cursor.selectionStart(), cursor.selectionEnd()
            else:
                start, end = cursor.position() - 1, cursor.position()
            for i in range(start + 1, end + 1):
                cursor.setPosition(i)
                format = cursor.charFormat()
                if format.fontWeight() != 75:
                    bold = False
                if format.fontItalic() is False:
                    italic = False
                if format.fontUnderline() is False:
                    underline = False
                if format.fontOverline() is False:
                    overline = False
                if format.verticalAlignment() != format.AlignSubScript:
                    subscript = False
                if format.verticalAlignment() != format.AlignSuperScript:
                    superscript = False
                if str(format.fontFamily()) != 'Symbol':
                    symbol = False
            self.ui.pushButton_bold.setChecked(bold)
            self.ui.pushButton_italic.setChecked(italic)
            self.ui.pushButton_underline.setChecked(underline)
            self.ui.pushButton_overline.setChecked(overline)
            self.ui.pushButton_subscript.setChecked(subscript)
            self.ui.pushButton_superscript.setChecked(superscript)
            self.ui.pushButton_symbol.setChecked(symbol)

    def latexDollarDecorators(self):
        latex = self.ui.pushButton_latex.isChecked()
        if latex is True:
            plainText = self.ui.textEdit.toPlainText()
            cursor = self.ui.textEdit.textCursor()
            if plainText[0] != '$':
                plainText.insert(0, '$')
                self.ui.textEdit.setPlainText(plainText)
                cursor.setPosition(1)
            if plainText[-1] != '$':
                plainText.append('$')
                self.ui.textEdit.setPlainText(plainText)
                cursor.setPosition(len(plainText)-1)
            if len(plainText) < 2:
                self.ui.textEdit.setPlainText('$$')
                cursor.setPosition(1)
            self.ui.textEdit.setTextCursor(cursor)

    def modifyText(self):
        bold = self.ui.pushButton_bold.isChecked()
        italic = self.ui.pushButton_italic.isChecked()
        underline = self.ui.pushButton_underline.isChecked()
        overline = self.ui.pushButton_overline.isChecked()
        subscript = self.ui.pushButton_subscript.isChecked()
        superscript = self.ui.pushButton_superscript.isChecked()
        symbol = self.ui.pushButton_symbol.isChecked()
        latex = self.ui.pushButton_latex.isChecked()
        cursor = self.ui.textEdit.textCursor()
        format = cursor.charFormat()
        if latex is not True:
            if len(self.ui.textEdit.toPlainText()) > 0:
                if self.ui.textEdit.toPlainText()[0] == '$':
                    self.ui.textEdit.setHtml('')
            if bold is True:
                # 75 is bold weight
                format.setFontWeight(75)
            else:
                # 50 is normal weight
                format.setFontWeight(50)
            if italic is True:
                format.setFontItalic(True)
            else:
                format.setFontItalic(False)
            if underline is True:
                format.setFontUnderline(True)
            else:
                format.setFontUnderline(False)
            if overline is True:
                format.setFontOverline(True)
            else:
                format.setFontOverline(False)
            if subscript is True:
                format.setVerticalAlignment(format.AlignSubScript)
            elif superscript is True:
                format.setVerticalAlignment(format.AlignSuperScript)
            else:
                format.setVerticalAlignment(format.AlignNormal)
            if symbol is True:
                format.setFontFamily('Symbol')
            else:
                format.setFontFamily(self.textBox.font().family())
            cursor.mergeCharFormat(format)
            self.ui.textEdit.setTextCursor(cursor)
        else:
            self.ui.pushButton_bold.setChecked(False)
            self.ui.pushButton_italic.setChecked(False)
            self.ui.pushButton_underline.setChecked(False)
            self.ui.pushButton_overline.setChecked(False)
            self.ui.pushButton_subscript.setChecked(False)
            self.ui.pushButton_superscript.setChecked(False)
            self.ui.pushButton_symbol.setChecked(False)
            format.setFontWeight(50)
            format.setFontItalic(False)
            format.setFontUnderline(False)
            format.setFontOverline(False)
            format.setVerticalAlignment(format.AlignNormal)
            cursor.mergeCharFormat(format)
            self.ui.textEdit.setTextCursor(cursor)
            self.ui.textEdit.setPlainText('$$')
            cursor.setPosition(1)
            self.ui.textEdit.setTextCursor(cursor)

    def mathTexToQImage(self, mathTex, fs, fc):
        """Use SymPy to generate the latex expression as a binary object, and save it to a file as an image.
        This saves the generated image within the object itself (which gets saved into a higher level
        schematic/symbol). As a result, the file size of the saved schematic/symbol is larger, but we
        benefit from greatly improved loading times."""
        dpi = self.textBox.latexImageDpi * self.textBox.latexImageDpiScale
        obj = BytesIO()

        color = QtGui.QColor(fc)
        rgba = color.getRgbF()
        r, g, b = rgba[0], rgba[1], rgba[2]
        fg = 'rgb ' + str(r) + ' ' + str(g) + ' ' + str(b)
        sympy.preview(mathTex, output='png', viewer='BytesIO', outputbuffer=obj, dvioptions=['-D', str(dpi), '-T', 'tight', '-fg', fg, '-bg', 'Transparent'])

        img = QtGui.QImage()
        img.loadFromData(obj.getvalue(), format='png')

        data = QtCore.QByteArray()
        buf = QtCore.QBuffer(data)
        img.save(buf, format='png')
        data64 = str(data.toBase64())

        return obj, data64


class myFileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        super(myFileDialog, self).__init__(*args)
        self.setOption(self.DontUseNativeDialog)
        # Find the list view responsible for showing the files and change its flow
        listViews = self.findChildren(QtWidgets.QListView)
        listView = listViews[0]
        listView.setFlow(listView.LeftToRight)
        self.iconProvider_ = myIconProvider()
        self.setIconProvider(self.iconProvider_)
        if 'mode' in kwargs:
            self.mode = kwargs['mode']
        else:
            self.mode = 'load'
        if self.mode == 'load':
            self.setFileMode(self.ExistingFile)
            self.setAcceptMode(self.AcceptOpen)
        elif self.mode == 'save':
            self.setFileMode(self.AnyFile)
            self.setAcceptMode(self.AcceptSave)
        if 'filt' in kwargs:
            self.setNameFilter(kwargs['filt'])
        self.setViewMode(self.List)
        self.resize(1280, 960)

    def setViewMode(self, viewMode):
        if viewMode == self.Detail:
            self.setItemDelegate(QtWidgets.QStyledItemDelegate())
        else:
            self.setItemDelegate(myStyledItemDelegate())
        super(myFileDialog, self).setViewMode(viewMode)


class myIconProvider(QtWidgets.QFileIconProvider):
    def __init__(self, parent=None):
        """Create a custom icon provider for the file picker"""
        super(myIconProvider, self).__init__()

    def icon(self, fileInfo):
        if type(fileInfo) == QtCore.QFileInfo:
            if str(fileInfo.filePath())[-3:] in ['sch', 'sym']:
                with open(str(fileInfo.filePath()), 'rb') as file:
                    loadItem = pickle.load(file)
                scene = QtWidgets.QGraphicsScene()
                # Load the file
                loadItem.__init__(None, QtCore.QPointF(0, 0), loadItem.listOfItems, mode='symbol')
                scene.addItem(loadItem)
                rect = loadItem.boundingRect()
                # Set the maximum icon dimension
                maxDim = 320
                maxSize = QtCore.QSizeF(maxDim, maxDim)
                pixRect = QtCore.QRectF(QtCore.QPointF(), maxSize)
                # Create a pixmap and fill it with a white background
                pix = QtGui.QPixmap(pixRect.toRect().size())
                pix.fill()

                # Find out the painter's starting position to have the icon drawn in the
                # center of the pixmap
                actualSize = rect.size()
                actualSize.scale(maxSize, QtCore.Qt.KeepAspectRatio)
                width, height = actualSize.width(), actualSize.height()
                startX, startY = (maxDim - width)/2, (maxDim - height)/2

                painter = QtGui.QPainter(pix)
                pen = QtGui.QPen()
                pen.setWidth(2)
                painter.setPen(pen)
                painter.translate(startX, startY)
                scene.render(painter, pixRect, rect)
                painter.end()

                icon = QtGui.QIcon()
                icon.addPixmap(pix)
                return icon
            else:
                return super(myIconProvider, self).icon(fileInfo)
        else:
            return super(myIconProvider, self).icon(fileInfo)


class myStyledItemDelegate(QtWidgets.QStyledItemDelegate):
    def __init__(self, *args):
        super(myStyledItemDelegate, self).__init__(*args)
        self.iconWidth, self.iconHeight = 200, 200

    def paint(self, painter, option, index):
        option.decorationPosition = option.Top
        option.decorationSize = QtCore.QSize(self.iconWidth*0.9, self.iconHeight*0.9)
        option.decorationAlignment = QtCore.Qt.AlignCenter
        option.displayAlignment = QtCore.Qt.AlignCenter
        super(myStyledItemDelegate, self).paint(painter, option, index)

    def sizeHint(self, option, index):
        return QtCore.QSize(self.iconWidth, self.iconHeight+30)
