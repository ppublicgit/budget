##=========================================================================
##
## UNCLASSIFIED
##
##=========================================================================

from PyQt5 import QtWidgets, QtCore
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

class MplCanvas(Canvas):
    """Class to represent the Canvas widget"""
    def __init__(self):
        # setup Matplotlib Figure and Axis
        self.fig = Figure()
        self.ax1 = self.fig.add_subplot(111)
        # initialization of the canvas
        Canvas.__init__(self, self.fig)
        # we define the widget as expandable
        Canvas.setSizePolicy(self, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # notify the system of updated policy
        Canvas.updateGeometry(self)
        self.fig.tight_layout()

class MplWidget(QtWidgets.QWidget):
    """Widget defined in Qt Designer"""
    def __init__(self, parent=None):
        # initialization of Qt MainWindow widget
        QtWidgets.QWidget.__init__(self, parent)
        # set the canvas to the Matplotlib widget
        self.canvas = MplCanvas()
        # these 2 lines for capturing focus
        self.canvas.setFocusPolicy(QtCore.Qt.ClickFocus)
        self.canvas.setFocus()
        # create a vertical box layout
        self.vbl = QtWidgets.QVBoxLayout()
        # add navigation toolbar
        self.nav_toolbar = NavigationToolbar(self.canvas, self)
        self.vbl.addWidget(self.nav_toolbar)
        # add mpl widget to the vertical box
        self.vbl.addWidget(self.canvas)
        # set the layout to the vertical box
        self.setLayout(self.vbl)