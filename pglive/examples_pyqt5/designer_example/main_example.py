import signal
from threading import Thread

from PyQt5.QtWidgets import QMainWindow

import pglive.examples_pyqt5 as examples
from pglive.examples_pyqt5.designer_example.win_template import Ui_MainWindow
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot


class MainWindow(QMainWindow, Ui_MainWindow):
    """Create main window from template"""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi(self)


win = MainWindow()
plot = LiveLinePlot()
data_connector = DataConnector(plot, max_points=600)
win.plot_widget.addItem(plot)

Thread(target=examples.sin_wave_generator, args=(data_connector,)).start()
signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
win.show()
examples.app.exec()
examples.stop()
