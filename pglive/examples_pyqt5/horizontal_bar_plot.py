import pglive.examples_pyqt5 as examples
from threading import Thread

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveHBarPlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
Horizontal Bar plot is displayed in this example.
"""
win = LivePlotWidget(title="Horizontal Bar Plot @ 100Hz")
plot = LiveHBarPlot(bar_height=1, brush="green", pen="green")
win.addItem(plot)

data_connector = DataConnector(plot, max_points=600)
win.show()

Thread(target=examples.sin_wave_generator, args=(data_connector,)).start()
examples.app.exec()
examples.stop()
