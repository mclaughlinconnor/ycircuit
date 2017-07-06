# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/gui/textEditor_gui.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(539, 399)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_bold = QtWidgets.QPushButton(Dialog)
        self.pushButton_bold.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton_bold.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_bold.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_bold.setStyleSheet("QPushButton {\n"
"    font-size: 18px;\n"
"    font-weight: bold;\n"
"}")
        self.pushButton_bold.setCheckable(True)
        self.pushButton_bold.setChecked(False)
        self.pushButton_bold.setAutoDefault(False)
        self.pushButton_bold.setFlat(True)
        self.pushButton_bold.setObjectName("pushButton_bold")
        self.horizontalLayout.addWidget(self.pushButton_bold)
        self.pushButton_italic = QtWidgets.QPushButton(Dialog)
        self.pushButton_italic.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton_italic.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_italic.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_italic.setStyleSheet("QPushButton {\n"
"    font-size: 18px;\n"
"    font-style: italic;\n"
"}")
        self.pushButton_italic.setCheckable(True)
        self.pushButton_italic.setAutoDefault(False)
        self.pushButton_italic.setFlat(True)
        self.pushButton_italic.setObjectName("pushButton_italic")
        self.horizontalLayout.addWidget(self.pushButton_italic)
        self.pushButton_underline = QtWidgets.QPushButton(Dialog)
        self.pushButton_underline.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton_underline.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_underline.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_underline.setStyleSheet("QPushButton {\n"
"    font-size: 18px;\n"
"    text-decoration: underline;\n"
"}")
        self.pushButton_underline.setCheckable(True)
        self.pushButton_underline.setAutoDefault(False)
        self.pushButton_underline.setFlat(True)
        self.pushButton_underline.setObjectName("pushButton_underline")
        self.horizontalLayout.addWidget(self.pushButton_underline)
        self.pushButton_overline = QtWidgets.QPushButton(Dialog)
        self.pushButton_overline.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton_overline.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_overline.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_overline.setStyleSheet("QPushButton {\n"
"    font-size: 18px;\n"
"    text-decoration: overline;\n"
"}")
        self.pushButton_overline.setCheckable(True)
        self.pushButton_overline.setAutoDefault(False)
        self.pushButton_overline.setFlat(True)
        self.pushButton_overline.setObjectName("pushButton_overline")
        self.horizontalLayout.addWidget(self.pushButton_overline)
        self.pushButton_subscript = QtWidgets.QPushButton(Dialog)
        self.pushButton_subscript.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton_subscript.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_subscript.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_subscript.setStyleSheet("QPushButton {\n"
"    font-size: 15px;\n"
"}")
        self.pushButton_subscript.setCheckable(True)
        self.pushButton_subscript.setAutoDefault(False)
        self.pushButton_subscript.setFlat(True)
        self.pushButton_subscript.setObjectName("pushButton_subscript")
        self.horizontalLayout.addWidget(self.pushButton_subscript)
        self.pushButton_superscript = QtWidgets.QPushButton(Dialog)
        self.pushButton_superscript.setMinimumSize(QtCore.QSize(20, 0))
        self.pushButton_superscript.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_superscript.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_superscript.setStyleSheet("QPushButton {\n"
"    font-size: 15px;\n"
"}")
        self.pushButton_superscript.setCheckable(True)
        self.pushButton_superscript.setAutoDefault(False)
        self.pushButton_superscript.setFlat(True)
        self.pushButton_superscript.setObjectName("pushButton_superscript")
        self.horizontalLayout.addWidget(self.pushButton_superscript)
        self.pushButton_symbol = QtWidgets.QPushButton(Dialog)
        self.pushButton_symbol.setMinimumSize(QtCore.QSize(40, 0))
        self.pushButton_symbol.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_symbol.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_symbol.setStyleSheet("font: 11pt \"Symbol\";")
        self.pushButton_symbol.setCheckable(True)
        self.pushButton_symbol.setAutoDefault(False)
        self.pushButton_symbol.setFlat(True)
        self.pushButton_symbol.setObjectName("pushButton_symbol")
        self.horizontalLayout.addWidget(self.pushButton_symbol)
        self.pushButton_latex = QtWidgets.QPushButton(Dialog)
        self.pushButton_latex.setMinimumSize(QtCore.QSize(50, 0))
        self.pushButton_latex.setMaximumSize(QtCore.QSize(30, 16777215))
        self.pushButton_latex.setFocusPolicy(QtCore.Qt.NoFocus)
        self.pushButton_latex.setStyleSheet("QPushButton {\n"
"    font-size: 15px;\n"
"}")
        self.pushButton_latex.setCheckable(True)
        self.pushButton_latex.setAutoDefault(False)
        self.pushButton_latex.setFlat(True)
        self.pushButton_latex.setObjectName("pushButton_latex")
        self.horizontalLayout.addWidget(self.pushButton_latex)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.horizontalLayout.setStretch(8, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.textEdit = QtWidgets.QTextEdit(Dialog)
        self.textEdit.setObjectName("textEdit")
        self.verticalLayout.addWidget(self.textEdit)
        self.buttonBox = QtWidgets.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.verticalLayout.addWidget(self.buttonBox)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        self.buttonBox.accepted.connect(Dialog.accept)
        self.buttonBox.rejected.connect(Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Edit text"))
        self.pushButton_bold.setText(_translate("Dialog", "B"))
        self.pushButton_bold.setShortcut(_translate("Dialog", "Ctrl+B"))
        self.pushButton_italic.setText(_translate("Dialog", "I"))
        self.pushButton_italic.setShortcut(_translate("Dialog", "Ctrl+I"))
        self.pushButton_underline.setText(_translate("Dialog", "U"))
        self.pushButton_underline.setShortcut(_translate("Dialog", "Ctrl+U"))
        self.pushButton_overline.setText(_translate("Dialog", "O"))
        self.pushButton_overline.setShortcut(_translate("Dialog", "Ctrl+O"))
        self.pushButton_subscript.setText(_translate("Dialog", "Sub"))
        self.pushButton_subscript.setShortcut(_translate("Dialog", "Ctrl+-"))
        self.pushButton_superscript.setText(_translate("Dialog", "Sup"))
        self.pushButton_superscript.setShortcut(_translate("Dialog", "Ctrl+="))
        self.pushButton_symbol.setText(_translate("Dialog", "abc"))
        self.pushButton_symbol.setShortcut(_translate("Dialog", "Ctrl+S"))
        self.pushButton_latex.setText(_translate("Dialog", "LaTeX"))
        self.pushButton_latex.setShortcut(_translate("Dialog", "Ctrl+L"))

