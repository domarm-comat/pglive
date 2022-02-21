import pglive.examples_pyqt5 as examples
from threading import Thread

import pyqtgraph as pg

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveHBarPlot, LiveVBarPlot, LiveLinePlot, LiveScatterPlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
In this example all plot types are displayed.
"""

layout = pg.LayoutWidget()
args = []
plots = [
    ["Horizontal Bar Plot", LiveHBarPlot(bar_height=2, brush="blue", pen="blue")],
    ["Vertical Bar Plot", LiveVBarPlot(bar_width=2, brush="green", pen="green")],
    ["Line Plot", LiveLinePlot(pen="red")],
    ["Scatter Plot", LiveScatterPlot(brush="yellow", pen="yellow")],
]

for title, plot in plots:
    widget = LivePlotWidget(title=f"{title} @ 50Hz")
    widget.addItem(plot)
    layout.addWidget(widget)
    args.append(DataConnector(plot, max_points=300, update_rate=50))

layout.show()

Thread(target=examples.sin_wave_generator, args=args).start()
examples.app.exec()
examples.stop()
