import sys
from math import sin
from threading import Thread
from time import sleep

from PyQt6.QtWidgets import QApplication
from pglive.sources.live_plot import LiveLinePlot

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot_widget import LivePlotWidget

"""
In this example Line plot is displayed.
"""
app = QApplication(sys.argv)
running = True

plot_widget = LivePlotWidget(title="Line Plot @ 100Hz")
plot_curve = LiveLinePlot()
plot_widget.addItem(plot_curve)
# DataConnector holding 600 points and plots @ 100Hz
data_connector = DataConnector(plot_curve, max_points=600, update_rate=100)


def sin_wave_generator(connector):
    """Sinus wave generator"""
    x = 0
    while running:
        x += 1
        data_point = sin(x * 0.01)
        # Callback to plot new data point
        connector.cb_append_data_point(data_point, x)

        sleep(0.01)


plot_widget.show()
Thread(target=sin_wave_generator, args=(data_connector,)).start()
app.exec()
running = False