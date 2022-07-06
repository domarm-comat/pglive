import pglive.examples_pyside6 as examples
import signal
from math import sin
from threading import Thread
from time import sleep

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveVBarPlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
In this example Vertical Bar plot is displayed.
Every update bar color is changed as well.
"""
win = LivePlotWidget(title="Coloured Vertical Bar Plot @ 100Hz")
plot = LiveVBarPlot(bar_width=1)
win.addItem(plot)

data_connector = DataConnector(plot, max_points=600)


def sin_wave_generator(*data_connectors):
    """Sin function generator, cycling colors of bar with each data point append"""
    x = 0
    while examples.running:
        x += 1
        for coloured_data_connector in data_connectors:
            color = next(examples.colors)
            coloured_data_connector.cb_append_data_point(sin(x * 0.01), x, pen=color, brush=color)
        sleep(0.01)


win.show()

Thread(target=sin_wave_generator, args=(data_connector,)).start()
signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
examples.app.exec()
examples.stop()
