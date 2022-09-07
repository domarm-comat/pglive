import pglive.examples_pyqt6 as examples
import signal
from threading import Thread

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
In this example Line plot is displayed.
"""
def ar(args, kwargs):
    print(args)

win = LivePlotWidget(title="Line Plot @ 100Hz")
win.autoRange = ar
plot = LiveLinePlot()
plot.autoRange = ar
win.addItem(plot)

data_connector = DataConnector(plot, max_points=600)

win.show()

Thread(target=examples.sin_wave_generator, args=(data_connector,)).start()
signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
examples.app.exec()
examples.stop()
