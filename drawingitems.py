from PyQt4 import QtCore, QtGui
from textEditor_gui import Ui_Dialog
import numpy
import uuid
import platform
import matplotlib as mpl
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib import rc
rc('font',**{'family':'sans-serif','sans-serif':['helvetica']})
## for Palatino and other serif fonts use:
#rc('font',**{'family':'serif','serif':['Palatino']})
rc('text', usetex=True)


class Grid(QtGui.QGraphicsItem):
    """temp docstring for the Gridclass"""
    def __init__(self, parent=None, view=None, spacing=10):
        super(Grid, self).__init__()
        self.parent = parent
        self.view = view
        self.spacing = spacing
        self.displaySpacing = spacing
        self.xLength = 10000
        self.yLength = 10000
        self.xPoints = numpy.arange(-self.xLength, self.xLength, self.spacing)
        self.yPoints = numpy.arange(-self.yLength, self.yLength, self.spacing)

    def boundingRect(self):
        return self.scene().sceneRect()

    def paint(self, painter, *args):
        pen = QtGui.QPen()
        # pen.setWidth(0.75*self.displaySpacing/self.spacing)
        pen.setWidth(max(1,0.75*numpy.log10(self.displaySpacing)))
        painter.setPen(pen)
        painter.drawPoints(self.gridPolygonRegular)
        # pen.setWidth(1.25*self.displaySpacing/self.spacing)
        pen.setWidth(max(2,1.5*numpy.log10(self.displaySpacing)))
        painter.setPen(pen)
        painter.drawPoints(self.gridPolygonLarge)

    def createGrid(self, **kwargs):
        if 'spacing' in kwargs:
            self.spacing = kwargs['spacing']
        # xL = int(topLeft.x()/self.displaySpacing)*self.displaySpacing
        # xL = numpy.minimum(xL, 0)
        # xH = int(bottomRight.x()/self.displaySpacing)*self.displaySpacing
        # xH = numpy.maximum(xH, int(self.scene().sceneRect().width()))
        # yL = int(topLeft.y()/self.displaySpacing)*self.displaySpacing
        # yL = numpy.minimum(yL, 0)
        # yH = int(bottomRight.y()/self.displaySpacing)*self.displaySpacing
        # yH = numpy.maximum(yH, int(self.scene().sceneRect().height()))
        # self.displaySpacing = self.spacing*(xH - xL)/1000
        # self.xDisplayPoints = numpy.arange(xL, xH, self.displaySpacing)
        # self.yDisplayPoints = numpy.arange(yL, yH, self.displaySpacing)
        topLeft = self.snapTo(self.mapToScene(QtCore.QPointF(self.view.rect().topLeft())))
        bottomRight = self.snapTo(self.mapToScene(QtCore.QPointF(self.view.rect().bottomRight())))
        if (bottomRight - topLeft).x() > (bottomRight - topLeft).y():
            self.extent = (bottomRight - topLeft).toPoint().x()
        else:
            self.extent = (bottomRight - topLeft).toPoint().y()
        self.displaySpacing = 10**(numpy.floor(numpy.log10(self.extent)))
        if self.extent/self.displaySpacing < 3:
            self.displaySpacing /= 10
        if self.displaySpacing <= self.spacing:
            self.displaySpacing = self.spacing*10
        topLeft = self.snapTo(topLeft, self.displaySpacing)
        bottomRight = self.snapTo(bottomRight, self.displaySpacing)
        padding = 2*self.displaySpacing
        self.xDisplayPoints = numpy.arange(topLeft.x()-padding, bottomRight.x()+padding, self.displaySpacing/5)
        self.yDisplayPoints = numpy.arange(topLeft.y()-padding, bottomRight.y()+padding, self.displaySpacing/5)
        self.gridPolygonRegular = QtGui.QPolygon()
        for x in self.xDisplayPoints:
            for y in self.yDisplayPoints:
                self.gridPolygonRegular.append(QtCore.QPoint(x, y))
        self.gridPolygonLarge = QtGui.QPolygon()
        for x in self.xDisplayPoints[self.xDisplayPoints % self.displaySpacing*10 == 0]:
            for y in self.yDisplayPoints[self.yDisplayPoints % self.displaySpacing*10 == 0]:
                self.gridPolygonLarge.append(QtCore.QPoint(x, y))

    def snapTo(self, point, spacing=None):
        if spacing is None:
            newX = numpy.round(point.x()/self.spacing)*self.spacing
            newY = numpy.round(point.y()/self.spacing)*self.spacing
        else:
            newX = numpy.round(point.x()/spacing)*spacing
            newY = numpy.round(point.y()/spacing)*spacing
        return QtCore.QPointF(newX, newY)


class TextEditor(QtGui.QDialog):
    def __init__(self, textBox=None):
        super(TextEditor, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.textBox = textBox

        self.ui.textEdit.setFocus(True)
        if self.textBox is not None:
            if self.textBox.latexExpression is None:
                self.ui.textEdit.setHtml(self.textBox.toHtml())
            else:
                self.ui.textEdit.setPlainText('$' + self.textBox.latexExpression + '$')
                self.ui.pushButton_latex.setChecked(True)
                cursor = self.ui.textEdit.textCursor()
                cursor.setPosition(1)
                self.ui.textEdit.setTextCursor(cursor)
            font = self.textBox.font()
            self.ui.textEdit.setFont(font)
            self.ui.textEdit.setTextColor(QtGui.QColor(self.textBox.localPenColour))

        self.ui.textEdit.cursorPositionChanged.connect(self.modifyPushButtons)
        self.ui.textEdit.textChanged.connect(self.latexDollarDecorators)

        QtGui.QShortcut('Ctrl+Return', self).activated.connect(self.accept)

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
            image = self.mathTexToQImage(plainText, self.font().pointSize(), self.textBox.localPenColour)
            if self.textBox.latexImageHtml is None:
                saveFile = str(uuid.uuid4()) + '.png'
                image.save(saveFile, quality=80)
                htmlString = '<img src="' + saveFile + '">'
            elif self.textBox.latexExpression != plainText[1:-1]:
                htmlString = self.textBox.latexImageHtml
                saveFile = htmlString[10:-2]
                image.save(saveFile, quality=80)
            else:
                htmlString = self.textBox.latexImageHtml
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
        # This function is adapted from http://stackoverflow.com/questions/32035251/displaying-latex-in-pyqt-pyside-qtablewidget
        # This will likely be moved to a separate thread later because it is slow at startup

        #---- set up a mpl figure instance ----

        fig = mpl.figure.Figure()
        fig.patch.set_facecolor('none')
        fig.set_canvas(FigureCanvasAgg(fig))
        fig.dpi = 640
        renderer = fig.canvas.get_renderer()

        #---- plot the mathTex expression ----

        ax = fig.add_axes([0, 0, 1, 1])
        ax.axis('off')
        ax.patch.set_facecolor('none')
        t = ax.text(0, 0, mathTex, ha='left', va='bottom', color=fc, fontsize=fs)

        #---- fit figure size to text artist ----

        fwidth, fheight = fig.get_size_inches()
        fig_bbox = fig.get_window_extent(renderer)
        text_bbox = t.get_window_extent(renderer, fig.dpi)

        tight_fwidth = text_bbox.width * fwidth / fig_bbox.width
        tight_fheight = text_bbox.height * fheight / fig_bbox.height

        # Added some extra padding because fractions were getting clipped
        fig.set_size_inches(tight_fwidth, tight_fheight + 0.05)

        #---- convert mpl figure to QPixmap ----

        buf, size = fig.canvas.print_to_buffer()
        qimage = QtGui.QImage.rgbSwapped(QtGui.QImage(buf, size[0], size[1], QtGui.QImage.Format_ARGB32))
        return qimage
