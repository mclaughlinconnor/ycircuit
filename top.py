import platform
if platform.system() == 'Windows':
    import ctypes
import sip
import sys
from PyQt5 import QtCore, QtWidgets
from src.mainwindow import myMainWindow


if __name__ == "__main__":
    if platform.system() == 'Windows':
        sip.setdestroyonexit(False)
        myappid = u'ycircuit.0.1'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    else:
        import os
        os.environ['QT_AUTO_SCREEN_SCALE_FACTOR'] = '1'
    QtCore.QCoreApplication.setOrganizationName('YCircuit')
    QtCore.QCoreApplication.setApplicationName('YCircuit')
    app = QtWidgets.QApplication(sys.argv)
    form = myMainWindow()
    form.showMaximized()
    form.ui.drawingArea.fitToViewRoutine()
    app.exec_()
