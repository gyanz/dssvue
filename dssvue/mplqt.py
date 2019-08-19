from PyQt5 import  uic

from PyQt5 import QtGui
from PyQt5.QtGui import (QColor,QIcon,QTextCursor)

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import (QApplication,QMainWindow,QDialog,QCheckBox,QComboBox,
                            QWidgetAction,QLabel,QFileDialog,
                            QAbstractItemView,QAction,QActionGroup,
                            QSizePolicy,QVBoxLayout,QHBoxLayout,
                            QTableWidget,QTableWidgetItem,QWidget,
                            QTableView,
                            QHeaderView,
                            QDialogButtonBox,QButtonGroup,QRadioButton, QToolBar)

from PyQt5 import QtCore
from PyQt5.QtCore import (QThread,QMutex,QReadWriteLock,QMutexLocker,QSettings,
                          pyqtSignal,Qt,QSortFilterProxyModel)

'''
import matplotlib as mpl
mpl.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
'''
import pyqtgraph as pg
from pyqtgraph.imageview.ImageView import ImageView
from pyqtgraph.widgets.MatplotlibWidget import MatplotlibWidget

QAPP = None
def mkQApp():
    global QAPP    
    QAPP = QtGui.QApplication.instance()
    if QAPP is None:
        QAPP = QtGui.QApplication([])
    return QAPP

