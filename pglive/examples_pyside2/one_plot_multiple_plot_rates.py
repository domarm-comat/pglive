import signal
from threading import Thread

import pglive.examples_pyside2 as examples
import pyqtgraph as pg

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_axis_range import LiveAxisRange
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
In this example we are plotting two signals in one plot with different plot_rate.
Since LiveAxisRange is calculating range from plot_rate, it might result in unwanted results.
You can use ignore_auto_range flag for DataConnector.
If it's set to True, this DataConnector is not causing change of range.
You can in fact use it to all LiveAxisRanges and implement your own custom Range calculation.
"""
layout = pg.LayoutWidget()
layout.layout.setSpacing(0)

'''
We want to display two signals in different frequencies.
Pglive is calculating view in respect to all plots. This might lead to unwanted results with multiple plots in one view.
So to makes things looks nice, we use only 100Hz plot for view calculation and ignore slow 1Hz plot.
Like that we can even save some resources and speed up overall plotting performance. 
'''
widget = LivePlotWidget(title="Two signals plotting at different rates.",
                        x_range_controller=LiveAxisRange(roll_on_tick=100, offset_left=30),
                        y_range_controller=LiveAxisRange(fixed_range=[-1, 1]))
widget.x_range_controller.crop_left_offset_to_data = True
plot = LiveLinePlot(pen="red")
widget.addItem(plot)
plot2 = LiveLinePlot(pen="yellow")
widget.addItem(plot2)
layout.addWidget(widget, row=0, col=0)
data_connector = DataConnector(plot, max_points=6000, plot_rate=100)
data_connector2 = DataConnector(plot2, max_points=6000, plot_rate=1, ignore_auto_range=True)
layout.show()

Thread(target=examples.sin_wave_generator, args=(data_connector,)).start()
Thread(target=examples.cos_wave_generator, args=(data_connector2,)).start()
signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
examples.app.exec_()
examples.stop()
