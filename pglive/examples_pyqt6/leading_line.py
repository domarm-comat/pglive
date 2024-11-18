import pglive.examples_pyqt6 as examples
from pyqtgraph import mkPen  # type: ignore

from threading import Thread

import pyqtgraph as pg  # type: ignore

from pglive.kwargs import LeadingLine, Orientation
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot, LiveScatterPlot, LiveHBarPlot, LiveVBarPlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
Leading line is displayed in this example.
Pglive can plot Vertical or Horizontal leading line.
User can choose orientation and which value is displayed by using text_axis parameter.
Please note, that X might be swapped with Y, when plotting horizontally or vertically.
Color of leading line is set with pen parameter.
"""

layout = pg.LayoutWidget()
# Line plot displaying Vertical Leading line and using Y axis value
plot_widget_1 = LivePlotWidget(title="Line Plot @ 50Hz, Leading with Y")
plot = LiveLinePlot()
plot.set_leading_line(LeadingLine.VERTICAL, pen=mkPen("red"), text_axis=LeadingLine.AXIS_Y, text_color="white",
                      text_orientation=Orientation.HORIZONTAL)
plot_widget_1.addItem(plot)
data_connector = DataConnector(plot, max_points=300, update_rate=50)
layout.addWidget(plot_widget_1)

# Line plot displaying Horizontal Leading line and using Y axis value
# Note that in this case text_axis default is X, but we have flipped x and y values.
plot_widget_2 = LivePlotWidget(title="Line Plot @ 50Hz, Leading with Y")
plot = LiveScatterPlot()
plot.set_leading_line(LeadingLine.HORIZONTAL, pen=mkPen("yellow"))
plot_widget_2.addItem(plot)
data_connector2 = DataConnector(plot, max_points=300, update_rate=50)
layout.addWidget(plot_widget_2)

plot_widget_3 = LivePlotWidget(title="Line Plot @ 50Hz, Leading with X")
plot = LiveHBarPlot()
plot.set_leading_line(LeadingLine.HORIZONTAL, pen=mkPen("yellow"), text_axis=LeadingLine.AXIS_Y, text_color="blue",
                      text_orientation=Orientation.VERTICAL)
plot_widget_3.addItem(plot)
data_connector3 = DataConnector(plot, max_points=300, update_rate=50)
layout.addWidget(plot_widget_3)

plot_widget_4 = LivePlotWidget(title="Line Plot @ 50Hz, Leading with Y")
plot = LiveVBarPlot()
plot.set_leading_line(LeadingLine.HORIZONTAL, pen=mkPen("red"), text_axis=LeadingLine.AXIS_Y)
plot_widget_4.addItem(plot)
data_connector4 = DataConnector(plot, max_points=300, update_rate=50)
layout.addWidget(plot_widget_4)

layout.show()

Thread(target=examples.sin_wave_generator, args=(data_connector, data_connector3, data_connector4)).start()
Thread(target=examples.sin_wave_generator, args=(data_connector2, ), kwargs={"flip": True}).start()
examples.app.exec()
examples.stop()
