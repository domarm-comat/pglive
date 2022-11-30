import time
from random import randint
from time import sleep

import pyqtgraph as pg
from threading import Thread
import numpy as np
from PyQt6.QtWidgets import QApplication
import sys

from pglive import examples_pyqt6
from pglive.kwargs import Axis
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_axis import LiveAxis
from pglive.sources.live_axis_range import LiveAxisRange
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

if __name__ == "__main__":
    app = QApplication(sys.argv)
    PV1_Watts_Layout = pg.LayoutWidget()
    PV1watts_plot = LiveLinePlot(pen='orange', name='PV-1', fillLevel=0, brush=(213, 129, 44, 100))
    PV2watts_plot = LiveLinePlot(pen='cyan', name='PV-2', fillLevel=0, brush=(102, 102, 255, 100))
    PV3watts_plot = LiveLinePlot(pen='red', name='PV-2', fillLevel=0, brush=(102, 102, 255, 100))

    # Data connectors for each plot with dequeue of max_points
    PV1watts_connector = DataConnector(PV1watts_plot, max_points=48000)
    PV2watts_connector = DataConnector(PV2watts_plot, max_points=48000)
    PV3watts_connector = DataConnector(PV3watts_plot, max_points=48000)

    # Setup bottom axis with TIME tick format
    # use Axis.DATETIME to show date
    pv1_watts_bottom_axis = LiveAxis("bottom", **{Axis.TICK_FORMAT: Axis.TIME})

    # Create plot
    PV1_graph_Widget = LivePlotWidget(title="Charger 1 & 2 Watts 1 Hour of 24",
                                           axisItems={'bottom': pv1_watts_bottom_axis},
                                           x_range_controller=LiveAxisRange(roll_on_tick=1800, offset_left=1))

    PV1_graph_Widget.x_range_controller.crop_left_offset_to_data = True

    # Show grid
    PV1_graph_Widget.showGrid(x=True, y=True, alpha=0.3)

    # Set labels
    PV1_graph_Widget.setLabel('bottom')
    PV1_graph_Widget.setLabel('left', 'Watts')

    PV1_graph_Widget.addLegend()  # If plot is named, auto add name to legend

    # Add Line
    PV1_graph_Widget.addItem(PV1watts_plot)
    PV1_graph_Widget.addItem(PV2watts_plot)
    PV1_graph_Widget.addItem(PV3watts_plot)

    # Add chart to Layout in Qt Designer
    PV1_Watts_Layout.addWidget(PV1_graph_Widget)
    PV1_Watts_Layout.show()

    Thread(target=examples_pyqt6.sin_wave_generator, args=(PV1watts_connector,)).start()
    Thread(target=examples_pyqt6.sin_wave_generator, args=(PV2watts_connector,)).start()

    def tt():
        while True:
            PV3watts_connector.cb_set_data([randint(0,10),randint(0,10),randint(0,10),randint(0,10)], [10,20,30,40])
            sleep(3)


    Thread(target=tt).start()


    app.exec()
    examples_pyqt6.running = False