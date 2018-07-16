from PyQt5 import QtCore, QtGui, QtWidgets
from src.gui.textEditor_gui import Ui_Dialog
import pickle
import sympy
from io import BytesIO
from distutils.spawn import find_executable
import logging

logger = logging.getLogger('YCircuit.drawingitems')


class Grid(QtCore.QObject):
    """temp docstring for the Gridclass"""
    def __init__(self,
                 parent=None,
                 view=None,
                 minorSpacing=20,
                 majorSpacing=100):
        super().__init__()
        self.parent = parent
        self.view = view
        self.enableGrid = True
        self.snapToGrid = True
        self.snapNetToPin = True
        self.minorSpacing = minorSpacing
        self.majorSpacing = majorSpacing
        self.minorSpacingVisibility = True
        self.majorSpacingVisibility = True
        self.snapToGridSpacing = self.minorSpacing / 2
        # Set it to 1200 because it is the LCM of 100, 200, 300 and 400 which are
        # the available major grid point spacings
        self.xLength = 1200
        self.yLength = 1200
        self.xMinorPoints = list(range(0, self.xLength + self.minorSpacing, self.minorSpacing))
        self.yMinorPoints = list(range(0, self.yLength + self.minorSpacing, self.minorSpacing))
        self.xMajorPoints = list(range(0, self.xLength + self.majorSpacing, self.majorSpacing))
        self.yMajorPoints = list(range(0, self.yLength + self.majorSpacing, self.majorSpacing))
        self.pinsPos = []

    def createGrid(self):
        self.xMinorPoints = list(range(0, self.xLength + self.minorSpacing, self.minorSpacing))
        self.yMinorPoints = list(range(0, self.yLength + self.minorSpacing, self.minorSpacing))
        self.xMajorPoints = list(range(0, self.xLength + self.majorSpacing, self.majorSpacing))
        self.yMajorPoints = list(range(0, self.yLength + self.majorSpacing, self.majorSpacing))
        self.gridPolygonRegular = QtGui.QPolygon()
        if self.minorSpacingVisibility is True:
            for x in self.xMinorPoints:
                for y in self.yMinorPoints:
                    self.gridPolygonRegular.append(QtCore.QPoint(x, y))
        self.gridPolygonLarge = QtGui.QPolygon()
        # Larger pixels for points on the coarse grid
        if self.majorSpacingVisibility is True:
            for x in self.xMajorPoints:
                for y in self.yMajorPoints:
                    self.gridPolygonLarge.append(QtCore.QPoint(x, y))

        pix = QtGui.QPixmap(QtCore.QSize(self.xLength, self.yLength))
        # Set background to white
        pix.fill(QtGui.QColor('white'))
        painter = QtGui.QPainter(pix)
        pen = QtGui.QPen()
        pen.setWidth(1)
        painter.setPen(pen)
        painter.drawPoints(self.gridPolygonRegular)
        pen.setWidth(4)
        painter.setPen(pen)
        painter.drawPoints(self.gridPolygonLarge)
        painter.end()
        self.view.setBackgroundBrush(QtGui.QBrush(pix))

    def removeGrid(self):
        self.view.setBackgroundBrush(QtGui.QBrush())

    def snapTo(self, point, snapToGridSpacing=None, pin=False):
        if snapToGridSpacing is None:
            newX = round(point.x()/self.snapToGridSpacing)*self.snapToGridSpacing
            newY = round(point.y()/self.snapToGridSpacing)*self.snapToGridSpacing
        else:
            newX = round(point.x()/snapToGridSpacing)*snapToGridSpacing
            newY = round(point.y()/snapToGridSpacing)*snapToGridSpacing
        if pin is True:
            if self.pinsPos == []:
                return QtCore.QPointF(newX, newY)
            if self.snapNetToPin is False:
                return QtCore.QPointF(newX, newY)
            pinsPos = [pos-QtCore.QPointF(newX, newY) for pos in self.pinsPos]
            dist = [pin.x()**2 + pin.y()**2 for pin in pinsPos]
            if min(dist) < 25*self.snapToGridSpacing**2:
                closestPin = dist.index(min(dist))
                newX, newY = self.pinsPos[closestPin].x(), self.pinsPos[closestPin].y()
        return QtCore.QPointF(newX, newY)


class TextEditor(QtWidgets.QDialog):
    def __init__(self, textBox=None, **kwargs):
        super().__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.textBox = textBox

        self.ui.textEdit.setFocus(True)
        if self.textBox is not None:
            font = self.textBox.font()
            font.setPointSize(font.pointSize() * self.textBox.textScale)
            self.ui.textEdit.setCurrentFont(font)
            self.font_ = font
            self.ui.textEdit.setTextColor(QtGui.QColor(self.textBox.localPenColour))
            if self.textBox.latexExpression is None:
                self.ui.textEdit.setHtml(self.textBox.toHtml())
            else:
                plainText = '$' + self.textBox.latexExpression + '$'
                self.ui.textEdit.setPlainText(plainText)
                self.ui.toolButton_latex.setChecked(True)
                cursor = self.ui.textEdit.textCursor()
                cursor.setPosition(1)
                self.ui.textEdit.setTextCursor(cursor)
                if hasattr(self.textBox, 'latexImageBinary'):
                    img = QtGui.QImage()
                    img.loadFromData(self.textBox.latexImageBinary.getvalue(), format='png')
                else:
                    self.textBox.latexImageBinary = self.mathTexToQImage(plainText, self.font().pointSize(), self.textBox.localPenColour)
                htmlString = ''
                self.textBox.latexImageHtml = htmlString
                self.textBox.setHtml(htmlString)

        self.ui.textEdit.cursorPositionChanged.connect(self.modifyPushButtons)
        self.ui.textEdit.cursorPositionChanged.connect(self.latexDollarDecorators)

        QtWidgets.QShortcut('Ctrl+Return', self).activated.connect(self.accept)

        self.ui.pushButton_bold.clicked.connect(self.modifyText)
        self.ui.pushButton_italic.clicked.connect(self.modifyText)
        self.ui.pushButton_underline.clicked.connect(self.modifyText)
        self.ui.pushButton_overline.clicked.connect(self.modifyText)
        self.ui.pushButton_subscript.clicked.connect(self.modifyText)
        self.ui.pushButton_superscript.clicked.connect(self.modifyText)
        self.ui.pushButton_symbol.clicked.connect(self.modifyText)
        if not find_executable('latex'):
            self.ui.toolButton_latex.setEnabled(False)
        self.ui.toolButton_latex.clicked.connect(self.modifyText)
        self.ui.latexMenu = QtWidgets.QMenu()
        self.ui.action_useEulerFont = QtWidgets.QAction('Use Euler font', self)
        self.ui.action_useEulerFont.setCheckable(True)
        if 'eulerFont' in kwargs:
            self.ui.action_useEulerFont.setChecked(kwargs['eulerFont'])
        self.ui.latexMenu.addAction(self.ui.action_useEulerFont)
        self.ui.toolButton_latex.setMenu(self.ui.latexMenu)
        katexHtmlFile = QtCore.QFileInfo('./src/katex.html')
        # On the built version, the file is at /lib/src
        if not katexHtmlFile.exists():
            katexHtmlFile = QtCore.QFileInfo('./lib/src/katex.html')
        self.ui.webEngineView.setUrl(QtCore.QUrl.fromLocalFile(katexHtmlFile.absoluteFilePath()))
        self.ui.webEngineView.hide()
        if self.textBox is not None:
            if self.textBox.latexExpression is not None:
                processedText = self.processTextForKatex(plainText)
                self.ui.webEngineView.show()
                self.ui.webEngineView.loadFinished.connect(
                    lambda: self.ui.webEngineView.page().runJavaScript(
                        'try {try_render("' +
                        processedText +
                        '")} catch(err) {}'
                    )
                )

    def accept(self):
        plainText = self.ui.textEdit.toPlainText()
        if self.ui.toolButton_latex.isChecked():
            self.textBox.latexImageBinary = self.mathTexToQImage(plainText, self.font().pointSize(), self.textBox.localPenColour)
            # This will not be None if latex is installed
            if self.textBox.latexImageBinary is not None:
                htmlString = ''
                self.textBox.latexImageHtml = htmlString
                self.textBox.latexExpression = plainText[1:-1]  # Skip $'s
                self.textBox.setHtml(htmlString)
                self.textBox.useEulerFont = self.ui.action_useEulerFont.isChecked()
                logger.info('Set latex expression for %s to %s', self.textBox, self.textBox.latexExpression)
            else:
                self.textBox.setHtml(self.ui.textEdit.toHtml())
                logger.info('Set HTML for %s to %s', self.textBox, self.textBox.toHtml())
        else:
            self.textBox.setHtml(self.ui.textEdit.toHtml())
            logger.info('Set HTML for %s to %s', self.textBox, self.textBox.toHtml())
            self.textBox.latexImageHtml = None
            self.textBox.latexExpression = None
            self.textBox.latexImageBinary = None
        super().accept()

    def modifyPushButtons(self):
        # Forcibly set the right font family and point size
        if self.ui.textEdit.fontFamily() != 'Symbol':
            self.ui.textEdit.setFontFamily(self.font_.family())
        self.ui.textEdit.setFontPointSize(self.font_.pointSize())
        cursor = self.ui.textEdit.textCursor()
        format = cursor.charFormat()
        bold, italic, underline, overline = True, True, True, True
        subscript, superscript, symbol = True, True, True
        latex = self.ui.toolButton_latex.isChecked()
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
        latex = self.ui.toolButton_latex.isChecked()
        if latex is True:
            plainText = self.ui.textEdit.toPlainText()
            cursor = self.ui.textEdit.textCursor()
            if plainText[0] != '$':
                plainText = '$' + plainText
                self.ui.textEdit.setPlainText(plainText)
                cursor.setPosition(1)
            if plainText[-1] != '$':
                plainText += '$'
                self.ui.textEdit.setPlainText(plainText)
                cursor.setPosition(len(plainText) - 1)
            if len(plainText) < 2:
                self.ui.textEdit.setPlainText('$$')
                cursor.setPosition(1)
            if cursor.position() == 0:
                cursor.setPosition(1)
            elif cursor.position() == len(plainText):
                cursor.setPosition(len(plainText) - 1)
            self.ui.textEdit.setTextCursor(cursor)
            processedText = self.processTextForKatex(plainText)
            self.ui.webEngineView.page().runJavaScript('try_render("' + processedText + '")')

    def processTextForKatex(self, plainText=''):
        # Remove $ signs
        text = plainText[1:-1]
        text = text.replace('\\', '\\\\')
        text = '\\\\begin{aligned}' + text + '\\\\end{aligned}'
        return text

    def modifyText(self):
        bold = self.ui.pushButton_bold.isChecked()
        italic = self.ui.pushButton_italic.isChecked()
        underline = self.ui.pushButton_underline.isChecked()
        overline = self.ui.pushButton_overline.isChecked()
        subscript = self.ui.pushButton_subscript.isChecked()
        superscript = self.ui.pushButton_superscript.isChecked()
        symbol = self.ui.pushButton_symbol.isChecked()
        latex = self.ui.toolButton_latex.isChecked()
        cursor = self.ui.textEdit.textCursor()
        format = cursor.charFormat()
        if latex is not True:
            self.ui.webEngineView.hide()
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
            self.ui.webEngineView.show()
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
        try:
            sympy.preview(mathTex, output='png', viewer='BytesIO', euler=self.ui.action_useEulerFont.isChecked(), outputbuffer=obj, dvioptions=['-D', str(dpi), '-T', 'tight', '-fg', fg, '-bg', 'Transparent'])
            logger.info('Generating latex expression %s', mathTex)
        except RuntimeError:
            self.ui.toolButton_latex.setChecked(False)
            logger.info('Latex installation not detected (Sympy raised RuntimeError)')
            return None, None

        img = QtGui.QImage()
        img.loadFromData(obj.getvalue(), format='png')
        self.textBox.latexImageColour = fc

        return obj


class myFileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        super().__init__(*args)
        self.setOption(self.DontUseNativeDialog)
        # Find the list view responsible for showing the files and change its flow
        listViews = self.findChildren(QtWidgets.QListView)
        listView = listViews[0]
        listView.setFlow(listView.LeftToRight)
        listView.setViewMode(listView.IconMode)
        listView.setUniformItemSizes(True)
        listView.setSpacing(10)
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
            if '*.sym' in kwargs['filt']:
                listView.setIconSize(QtCore.QSize(100, 100))
            elif '*.sch' in kwargs['filt']:
                listView.setIconSize(QtCore.QSize(150, 150))
        if 'showSchematicPreview' in kwargs:
            self.iconProvider_.showSchematicPreview = kwargs['showSchematicPreview']
        if 'showSymbolPreview' in kwargs:
            self.iconProvider_.showSymbolPreview = kwargs['showSymbolPreview']
        screenSize = QtWidgets.QDesktopWidget().screenGeometry(QtWidgets.QDesktopWidget().screenNumber()).size()
        self.resize(screenSize*0.8)


class myIconProvider(QtWidgets.QFileIconProvider):
    def __init__(self, parent=None):
        """Create a custom icon provider for the file picker"""
        super().__init__()
        self.showSchematicPreview = True
        self.showSymbolPreview = True

    def icon(self, fileInfo):
        if type(fileInfo) == QtCore.QFileInfo:
            if str(fileInfo.filePath())[-3:] == 'sch':
                if self.showSchematicPreview is False:
                    return super().icon(fileInfo)
            if str(fileInfo.filePath())[-3:] == 'sym':
                if self.showSymbolPreview is False:
                    return super().icon(fileInfo)
            if str(fileInfo.filePath())[-3:] in ['sch', 'sym']:
                with open(str(fileInfo.filePath()), 'rb') as f:
                    try:
                        loadItem = pickle.load(f)
                    except:
                        return super().icon(fileInfo)

                if not hasattr(loadItem, 'icon'):
                    pix = self.createIconPixmap(loadItem)
                else:
                    pix = QtGui.QPixmap()
                    pix.loadFromData(loadItem.icon, 'png')
                icon = QtGui.QIcon()
                icon.addPixmap(pix)
                return icon
            else:
                return super().icon(fileInfo)
        else:
            return super().icon(fileInfo)

    def createIconPixmap(self, loadItem, scene=None):
        if scene is None:
            scene = QtWidgets.QGraphicsScene()
            # Load the file
            loadItem.__init__(
                None,
                QtCore.QPointF(0, 0),
                loadItem.listOfItems,
                mode='symbol')
            scene.addItem(loadItem)
        rect = loadItem.sceneBoundingRect()
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
        startX, startY = (maxDim - width) / 2, (maxDim - height) / 2

        painter = QtGui.QPainter(pix)
        pen = QtGui.QPen()
        pen.setWidth(2)
        painter.setPen(pen)
        painter.translate(startX, startY)
        scene.render(painter, pixRect, rect)
        painter.end()

        return pix
