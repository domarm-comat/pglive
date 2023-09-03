import signal
import time
from threading import Thread

import numpy as np
import numpy.random
import pyqtgraph as pg

import pglive.examples_pyqt6 as examples
from pglive.kwargs import Axis
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_HeatMap import LiveHeatMap
from pglive.sources.live_axis import LiveAxis
from pglive.sources.live_plot_widget import LivePlotWidget

"""
Line plot is displayed in this example.
"""
global running
# color map
cmap = pg.colormap.get('CET-D1')
plot = LiveHeatMap(colormap=cmap, grid_pen=pg.mkPen("red", width=1), draw_counts=False)

resolution = 25
left_labels = [f"Y{i}" for i in range(resolution)]
bottom_labels = [f"X{i}" for i in range(resolution)]
# imv.setData(bottom_labels, left_labels, heatmap=np.array(heatmap))

# Set Axis.SHOW_ALL_CATEGORIES: True if you want to always show all category ticks
left_axis = LiveAxis("left", tick_angle=0,
                     **{Axis.TICK_FORMAT: Axis.CATEGORY, Axis.CATEGORIES: left_labels, Axis.SHOW_ALL_CATEGORIES: True})
right_axis = LiveAxis("right", tick_angle=0,
                     **{Axis.TICK_FORMAT: Axis.CATEGORY, Axis.CATEGORIES: left_labels, Axis.SHOW_ALL_CATEGORIES: False})
top_axis = LiveAxis("top", tick_angle=0, **{Axis.TICK_FORMAT: Axis.CATEGORY, Axis.CATEGORIES: bottom_labels,
                                    Axis.SHOW_ALL_CATEGORIES: False})
bottom_axis = LiveAxis("bottom", tick_angle=0, **{Axis.TICK_FORMAT: Axis.CATEGORY, Axis.CATEGORIES: bottom_labels,
                                    Axis.SHOW_ALL_CATEGORIES: True})

win = LivePlotWidget(title="Line Plot @ 100Hz", axisItems={'top': top_axis, 'bottom': bottom_axis, 'left': left_axis, 'right': right_axis})
win.addItem(plot)
win.show()

data_connector = DataConnector(plot)

def heatmap_generator(data_connector):
    while True:
        heatmap = []
        for i in range(resolution):
            heatmap.append(numpy.random.randint(0, 1024, resolution))
        data_connector.cb_set_data(bottom_labels, left_labels, heatmap=np.array(heatmap))
        time.sleep(1)

Thread(target=heatmap_generator, args=(data_connector,)).start()
signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
examples.app.exec()
examples.stop()
