import pglive.examples_pyside2 as examples
from math import ceil
from threading import Thread

import pyqtgraph as pg

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveHBarPlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
In this example, different update rate is demonstrated.
Display four plots, each slower by 1/4 of previous update rate.
Update rate is set in Hz unit.
"""
layout = pg.LayoutWidget()
args = []
# Initial rate of 100Hz
update_rate = 100
max_len = 600
# Initial delta Y is 1
bar_height = 1
for index in range(4):
    widget = LivePlotWidget(title=f"Horizontal Bar Plot @ {update_rate}Hz")
    plot = LiveHBarPlot(bar_height=bar_height, brush="green", pen="green")
    widget.addItem(plot)
    layout.addWidget(widget)
    args.append(DataConnector(plot, max_points=ceil(max_len), update_rate=update_rate))
    # divide all important parameters by 4
    update_rate /= 4
    max_len /= 4
    # bar height depends on Y distance, that's why we should multiply it by 4
    # if we leave it at 1, we get smaller bars
    bar_height *= 4

layout.show()

Thread(target=examples.sin_wave_generator, args=args).start()
examples.app.exec_()
examples.stop()
