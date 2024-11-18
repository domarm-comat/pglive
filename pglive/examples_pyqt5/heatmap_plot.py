import signal
import time
from threading import Thread
import pglive.examples_pyqt5 as examples
import numpy.random
import pyqtgraph as pg
from PyQt5.QtWidgets import QWidget, QGridLayout


from pglive.kwargs import Axis
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_HeatMap import LiveHeatMap
from pglive.sources.live_axis import LiveAxis
from pglive.sources.live_plot_widget import LivePlotWidget

"""
HeatMap is displayed in this example.
"""
# Get color map
cmap = pg.colormap.get("CET-D1")
# Create Heat map plot item
# grid_pen is used to draw a grid, remove if you don't want any grid
# counts_pen is used to draw point counts, remove if you don't want any grid
plot = LiveHeatMap(colormap=cmap, grid_pen=pg.mkPen("red"), counts_pen=pg.mkPen("white"))

resolution = 10  # 10 x 10 pixels
left_labels = [f"Y{i}" for i in range(resolution)]
bottom_labels = [f"X{i}" for i in range(resolution)]

# Set Axis.SHOW_ALL_CATEGORIES: True if you want to always show all category ticks
left_axis = LiveAxis("left", tick_angle=0,
                     **{Axis.TICK_FORMAT: Axis.CATEGORY, Axis.CATEGORIES: left_labels, Axis.SHOW_ALL_CATEGORIES: True})
right_axis = LiveAxis("right", tick_angle=0,
                      **{Axis.TICK_FORMAT: Axis.CATEGORY, Axis.CATEGORIES: left_labels,
                         Axis.SHOW_ALL_CATEGORIES: False})
top_axis = LiveAxis("top", tick_angle=0, **{Axis.TICK_FORMAT: Axis.CATEGORY, Axis.CATEGORIES: bottom_labels,
                                            Axis.SHOW_ALL_CATEGORIES: True})
bottom_axis = LiveAxis("bottom", tick_angle=0, **{Axis.TICK_FORMAT: Axis.CATEGORY, Axis.CATEGORIES: bottom_labels,
                                                  Axis.SHOW_ALL_CATEGORIES: False})

view_1 = LivePlotWidget(title="Heat map plot with counts and grid @ 1Hz",
                        axisItems={'top': top_axis, 'bottom': bottom_axis, 'left': left_axis, 'right': right_axis})
view_1.addItem(plot)

# Get color map
cmap_2 = pg.colormap.get("plasma")
# Create Heat map plot item
plot_2 = LiveHeatMap(colormap=cmap_2)

resolution_2 = 20  # 20 x 20 pixels
left_labels_2 = [f"Y{i}" for i in range(resolution_2)]
bottom_labels_2 = [f"X{i}" for i in range(resolution_2)]

# Set Axis.SHOW_ALL_CATEGORIES: True if you want to always show all category ticks
left_axis_2 = LiveAxis("left", tick_angle=0,
                       **{Axis.TICK_FORMAT: Axis.CATEGORY, Axis.CATEGORIES: left_labels_2,
                          Axis.SHOW_ALL_CATEGORIES: True})
right_axis_2 = LiveAxis("right", tick_angle=0,
                        **{Axis.TICK_FORMAT: Axis.CATEGORY, Axis.CATEGORIES: left_labels_2,
                           Axis.SHOW_ALL_CATEGORIES: False})
top_axis_2 = LiveAxis("top", tick_angle=0, **{Axis.TICK_FORMAT: Axis.CATEGORY, Axis.CATEGORIES: bottom_labels_2,
                                              Axis.SHOW_ALL_CATEGORIES: True})
bottom_axis_2 = LiveAxis("bottom", tick_angle=0, **{Axis.TICK_FORMAT: Axis.CATEGORY, Axis.CATEGORIES: bottom_labels_2,
                                                    Axis.SHOW_ALL_CATEGORIES: False})

view_2 = LivePlotWidget(title="Heat map plot @ 10Hz",
                        axisItems={'top': top_axis_2, 'bottom': bottom_axis_2, 'left': left_axis_2,
                                   'right': right_axis_2})
view_2.addItem(plot_2)

# Setup layout to display all plots and histograms
plots_view = QWidget()
plots_view.setContentsMargins(0, 0, 0, 0)
plots_view.setLayout(QGridLayout())
plots_view.layout().setSpacing(0)
plots_view.layout().addWidget(view_1, 0, 0)
plots_view.layout().addWidget(plot.histogram, 0, 1)
plots_view.layout().addWidget(view_2, 1, 0)
plots_view.layout().addWidget(plot_2.histogram, 1, 1)
plots_view.show()
data_connector = DataConnector(plot)
data_connector_2 = DataConnector(plot_2)


def heatmap_generator(data_connector, resolution, bottom_labels, left_labels, timeout=1):
    while examples.running:
        heatmap = []
        for i in range(resolution):
            heatmap.append(numpy.random.randint(0, 1000, resolution))
        data_connector.cb_set_data(bottom_labels, left_labels, heatmap=heatmap)
        time.sleep(timeout)


Thread(target=heatmap_generator, args=(data_connector, resolution, bottom_labels, left_labels)).start()
Thread(target=heatmap_generator, args=(data_connector_2, resolution_2, bottom_labels_2, left_labels_2, 0.1)).start()
signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
examples.app.exec()
examples.stop()
