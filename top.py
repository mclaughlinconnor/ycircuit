import os, sys

if getattr(sys, "frozen", False):
    dname = os.path.dirname(sys.executable)
else:
    abspath = os.path.abspath(__file__)
    dname = os.path.dirname(abspath)
os.chdir(dname)
import platform

if platform.system() == "Windows":
    import ctypes
import sip
from PyQt5 import QtCore, QtWidgets, QtGui
from src.mainwindow import myMainWindow
import logging, logging.handlers


logger = logging.getLogger("YCircuit")
logger.setLevel(logging.INFO)

fh = logging.handlers.RotatingFileHandler("YCircuit.log", maxBytes=1000000, backupCount=1)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
fh.setFormatter(formatter)

logger.addHandler(fh)


def logException(excType, value, traceback):
    logger.critical("Uncaught exception", exc_info=(excType, value, traceback))


if __name__ == "__main__":
    logger.info("YCircuit started on " + sys.platform)
    logger.info("Setting directory to " + dname)
    if platform.system() == "Windows":
        sip.setdestroyonexit(False)
        myappid = u"ycircuit.0.2"
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
    if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    else:
        import os

        os.environ["QT_AUTO_SCREEN_SCALE_FACTOR"] = "1"
    QtCore.QCoreApplication.setOrganizationName("YCircuit")
    QtCore.QCoreApplication.setApplicationName("YCircuit")
    app = QtWidgets.QApplication(sys.argv)
    # Show the splash screen
    # splashPicture = QtGui.QPixmap(':/splash/splash.png')
    # app.splash = QtWidgets.QSplashScreen(app.desktop(), splashPicture, QtCore.Qt.WindowStaysOnTopHint)
    # app.splash.setMask(splashPicture.mask())
    # Code below from https://stackoverflow.com/a/50680020
    # currentScreen = app.desktop().screenNumber(QtGui.QCursor().pos())
    # currentScreenCenter = app.desktop().availableGeometry(currentScreen).center()
    # app.splash.move(currentScreenCenter - app.splash.rect().center())
    # app.splash.show()

    form = myMainWindow(clipboard=app.clipboard())
    form.showMaximized()
    form.ui.drawingArea.fitToViewRoutine()

    # Hide splash screen
    # app.splash.finish(form)
    sys.excepthook = logException
    app.exec_()
    logger.info("YCircuit closed normally\n")
