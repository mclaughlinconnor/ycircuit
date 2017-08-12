import platform
if platform.system() == 'Windows':
    import ctypes
import sip
import sys
from PyQt5 import QtCore, QtWidgets
from src.mainwindow import myMainWindow
import logging, logging.handlers


logger = logging.getLogger('YCircuit')
logger.setLevel(logging.INFO)

fh = logging.handlers.RotatingFileHandler('YCircuit.log', maxBytes=1000000, backupCount=1)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)

logger.addHandler(fh)

def logException(excType, value, traceback):
    logger.critical('Uncaught exception', exc_info=(excType, value, traceback))

if __name__ == "__main__":
    logger.info('YCircuit started on ' + sys.platform)
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
    sys.excepthook = logException
    app.exec_()
    logger.info('YCircuit closed normally\n')
