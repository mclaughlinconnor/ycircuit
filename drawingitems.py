from PyQt4 import QtCore, QtGui
from textEditor_gui import Ui_Dialog
import numpy


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
        pen.setWidth(0.75*self.displaySpacing/self.spacing)
        painter.setPen(pen)
        for i in self.xDisplayPoints:
            for j in self.yDisplayPoints:
                self.point = QtCore.QPoint(i, j)
                painter.drawPoint(self.point)
        pen.setWidth(1.25*self.displaySpacing/self.spacing)
        painter.setPen(pen)
        for i in self.xDisplayPoints[self.xDisplayPoints % 100 == 0]:
            for j in self.yDisplayPoints[self.yDisplayPoints % 100 == 0]:
                self.point = QtCore.QPoint(i, j)
                painter.drawPoint(self.point)

    def createGrid(self, **kwargs):
        if 'spacing' in kwargs:
            self.spacing = kwargs['spacing']
        topLeft = self.view.mapToScene(self.view.rect().topLeft())
        bottomRight = self.view.mapToScene(self.view.rect().bottomRight())
        xL = int(topLeft.x()/self.displaySpacing)*self.displaySpacing
        xL = numpy.minimum(xL, 0)
        xH = int(bottomRight.x()/self.displaySpacing)*self.displaySpacing
        xH = numpy.maximum(xH, int(self.scene().sceneRect().width()))
        yL = int(topLeft.y()/self.displaySpacing)*self.displaySpacing
        yL = numpy.minimum(yL, 0)
        yH = int(bottomRight.y()/self.displaySpacing)*self.displaySpacing
        yH = numpy.maximum(yH, int(self.scene().sceneRect().height()))
        self.displaySpacing = self.spacing*(xH - xL)/1000
        if self.displaySpacing < self.spacing:
            self.displaySpacing = self.spacing
        self.xDisplayPoints = numpy.arange(xL, xH, self.displaySpacing)
        self.yDisplayPoints = numpy.arange(yL, yH, self.displaySpacing)

    def snapTo(self, point):
        newX = numpy.round(point.x()/self.spacing)*self.spacing
        newY = numpy.round(point.y()/self.spacing)*self.spacing
        return QtCore.QPointF(newX, newY)


class TextEditor(QtGui.QDialog):
    def __init__(self, textBox=None):
        super(TextEditor, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.ui.textEdit.setFocus(True)
        if textBox is not None:
            self.ui.textEdit.setHtml(textBox.toHtml())
            font = textBox.font()
            self.ui.textEdit.setFont(font)

        self.ui.textEdit.cursorPositionChanged.connect(self.modifyPushButtons)

        QtGui.QShortcut('Ctrl+Return', self).activated.connect(self.accept)

        self.ui.pushButton_bold.clicked.connect(self.modifyText)
        self.ui.pushButton_italic.clicked.connect(self.modifyText)
        self.ui.pushButton_underline.clicked.connect(self.modifyText)
        self.ui.pushButton_subscript.clicked.connect(self.modifyText)
        self.ui.pushButton_superscript.clicked.connect(self.modifyText)

    def modifyPushButtons(self):
        cursor = self.ui.textEdit.textCursor()
        format = cursor.charFormat()
        bold, italic, underline, subscript, superscript = True, True, True, True, True
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
            if format.verticalAlignment() != format.AlignSubScript:
                subscript = False
            if format.verticalAlignment() != format.AlignSuperScript:
                superscript = False
        self.ui.pushButton_bold.setChecked(bold)
        self.ui.pushButton_italic.setChecked(italic)
        self.ui.pushButton_underline.setChecked(underline)
        self.ui.pushButton_subscript.setChecked(subscript)
        self.ui.pushButton_superscript.setChecked(superscript)
        # else:
        #     self.ui.pushButton_bold.setChecked(format.fontWeight() == 75)
        #     self.ui.pushButton_italic.setChecked(format.fontItalic())
        #     self.ui.pushButton_underline.setChecked(format.fontUnderline())

    def modifyText(self):
        bold = self.ui.pushButton_bold.isChecked()
        italic = self.ui.pushButton_italic.isChecked()
        underline = self.ui.pushButton_underline.isChecked()
        subscript = self.ui.pushButton_subscript.isChecked()
        superscript = self.ui.pushButton_superscript.isChecked()
        cursor = self.ui.textEdit.textCursor()
        format = cursor.charFormat()
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
        if subscript is True:
            format.setVerticalAlignment(format.AlignSubScript)
        elif superscript is True:
            format.setVerticalAlignment(format.AlignSuperScript)
        else:
            format.setVerticalAlignment(format.AlignNormal)
        cursor.mergeCharFormat(format)
        self.ui.textEdit.setTextCursor(cursor)
