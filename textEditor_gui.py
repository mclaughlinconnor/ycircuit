# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\textEditor_gui.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(539, 399)
        self.horizontalLayout_2 = QtGui.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.pushButton_bold = QtGui.QPushButton(Dialog)
        self.pushButton_bold.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton_bold.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_bold.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_bold.setStyleSheet(_fromUtf8("QPushButton {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"}"))
        self.pushButton_bold.setCheckable(True)
        self.pushButton_bold.setChecked(False)
        self.pushButton_bold.setAutoDefault(False)
        self.pushButton_bold.setFlat(True)
        self.pushButton_bold.setObjectName(_fromUtf8("pushButton_bold"))
        self.horizontalLayout.addWidget(self.pushButton_bold)
        self.pushButton_italic = QtGui.QPushButton(Dialog)
        self.pushButton_italic.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton_italic.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_italic.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_italic.setStyleSheet(_fromUtf8("QPushButton {\n"
"    font-size: 18px;\n"
"    font-style: italic;\n"
"}"))
        self.pushButton_italic.setCheckable(True)
        self.pushButton_italic.setAutoDefault(False)
        self.pushButton_italic.setFlat(True)
        self.pushButton_italic.setObjectName(_fromUtf8("pushButton_italic"))
        self.horizontalLayout.addWidget(self.pushButton_italic)
        self.pushButton_underline = QtGui.QPushButton(Dialog)
        self.pushButton_underline.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton_underline.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_underline.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_underline.setStyleSheet(_fromUtf8("QPushButton {\n"
"    font-size: 18px;\n"
"    text-decoration: underline;\n"
"}"))
        self.pushButton_underline.setCheckable(True)
        self.pushButton_underline.setAutoDefault(False)
        self.pushButton_underline.setFlat(True)
        self.pushButton_underline.setObjectName(_fromUtf8("pushButton_underline"))
        self.horizontalLayout.addWidget(self.pushButton_underline)
        self.pushButton_subscript = QtGui.QPushButton(Dialog)
        self.pushButton_subscript.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton_subscript.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_subscript.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_subscript.setStyleSheet(_fromUtf8(""))
        self.pushButton_subscript.setCheckable(True)
        self.pushButton_subscript.setAutoDefault(False)
        self.pushButton_subscript.setFlat(True)
        self.pushButton_subscript.setObjectName(_fromUtf8("pushButton_subscript"))
        self.horizontalLayout.addWidget(self.pushButton_subscript)
        self.pushButton_superscript = QtGui.QPushButton(Dialog)
        self.pushButton_superscript.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton_superscript.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_superscript.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_superscript.setStyleSheet(_fromUtf8(""))
        self.pushButton_superscript.setCheckable(True)
        self.pushButton_superscript.setAutoDefault(False)
        self.pushButton_superscript.setFlat(True)
        self.pushButton_superscript.setObjectName(_fromUtf8("pushButton_superscript"))
        self.horizontalLayout.addWidget(self.pushButton_superscript)
        self.pushButton_latex = QtGui.QPushButton(Dialog)
        self.pushButton_latex.setMinimumSize(QtCore.QSize(40, 0))
        self.pushButton_latex.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_latex.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_latex.setStyleSheet(_fromUtf8(""))
        self.pushButton_latex.setCheckable(True)
        self.pushButton_latex.setAutoDefault(False)
        self.pushButton_latex.setFlat(True)
        self.pushButton_latex.setObjectName(_fromUtf8("pushButton_latex"))
        self.horizontalLayout.addWidget(self.pushButton_latex)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout.setStretch(6, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEdit = QtGui.QTextEdit(Dialog)
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.verticalLayout.addWidget(self.textEdit)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Edit text", None))
        self.pushButton_bold.setText(_translate("Dialog", "B", None))
        self.pushButton_bold.setShortcut(_translate("Dialog", "Ctrl+B", None))
        self.pushButton_italic.setText(_translate("Dialog", "I", None))
        self.pushButton_italic.setShortcut(_translate("Dialog", "Ctrl+I", None))
        self.pushButton_underline.setText(_translate("Dialog", "U", None))
        self.pushButton_underline.setShortcut(_translate("Dialog", "Ctrl+U", None))
        self.pushButton_subscript.setText(_translate("Dialog", "Sub", None))
        self.pushButton_subscript.setShortcut(_translate("Dialog", "Ctrl+U", None))
        self.pushButton_superscript.setText(_translate("Dialog", "Sup", None))
        self.pushButton_superscript.setShortcut(_translate("Dialog", "Ctrl+U", None))
        self.pushButton_latex.setText(_translate("Dialog", "LaTeX", None))
        self.pushButton_latex.setShortcut(_translate("Dialog", "Ctrl+U", None))

