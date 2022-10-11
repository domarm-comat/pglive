import signal
from threading import Thread

import pglive.examples_pyside6 as examples
from pglive.kwargs import Axis
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_axis import LiveAxis
from pglive.sources.live_categorized_bar_plot import LiveCategorizedBarPlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
In this example Categorized Bar plot is displayed.
"""
categories = ["On", "Off", "Idle", "Warning", "Failure"]
plot = LiveCategorizedBarPlot(categories,
                              category_color={"Failure": "r", "Warning": "orange", "Off": "silver", "Idle": "blue"})
# Make sure to give plot.categories to Axis.CATEGORIES param (it's dynamic list)
# If you're using static categories and your data won't yield not listed category you can use static categories list
left_axis = LiveAxis("left", **{Axis.TICK_FORMAT: Axis.CATEGORY, Axis.CATEGORIES: plot.categories})
bottom_axis = LiveAxis("bottom", **{Axis.TICK_FORMAT: Axis.DURATION})
win = LivePlotWidget(title="Categorized Bar Plot @ 5Hz", axisItems={'bottom': bottom_axis, 'left': left_axis})
win.addItem(plot)
data_connector = DataConnector(plot, max_points=50, update_rate=5)
win.show()

Thread(target=examples.category_generator, args=(data_connector,), kwargs={"categories": categories}).start()
signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
examples.app.exec()
examples.stop()
