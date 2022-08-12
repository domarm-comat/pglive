import pglive.examples_pyqt5 as examples
from threading import Thread

import pyqtgraph as pg

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveHBarPlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
In this example, different plot rate is demonstrated.
Display four plots, each slower by 1/4 of previous plot rate.
Plot rate is set in Hz unit.
"""
layout = pg.LayoutWidget()
args = []
# Initial rate of 100Hz
plot_rate = 100
max_len = 600
# Initial delta Y is 1
bar_height = 1
for index in range(4):
    widget = LivePlotWidget(title=f"Horizontal Bar Plot @ {plot_rate}Hz")
    plot = LiveHBarPlot(bar_height=bar_height, brush="green", pen="green")
    widget.addItem(plot)
    layout.addWidget(widget)
    args.append(DataConnector(plot, max_points=max_len, plot_rate=plot_rate))
    plot_rate /= 4

layout.show()

Thread(target=examples.sin_wave_generator, args=args).start()
examples.app.exec()
examples.stop()
