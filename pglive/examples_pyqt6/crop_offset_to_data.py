import signal
from threading import Thread

import pglive.examples_pyqt6 as examples
import pyqtgraph as pg
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_axis_range import LiveAxisRange
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
In this example live axis range crop offset to data is displayed.
"""
layout = pg.LayoutWidget()
layout.layout.setSpacing(0)

'''
We want to display view 30 seconds long and pan right every 1 second. 
'''
widget = LivePlotWidget(title="Roll plot view every 1 sec, offset 30 sec, crop left = False",
                        x_range_controller=LiveAxisRange(roll_on_tick=100, offset_left=30),
                        y_range_controller=LiveAxisRange(fixed_range=[-1, 1]))
plot = LiveLinePlot(pen="red")
widget.addItem(plot)
layout.addWidget(widget, row=0, col=0)
data_connector = DataConnector(plot, max_points=6000)

'''
Move view to the right on every 300 ticks (data update).
Y range is fixed to -1 and 1.
'''
widget2 = LivePlotWidget(title="Roll plot view every 1 sec, offset 30 sec, crop left = True",
                         x_range_controller=LiveAxisRange(roll_on_tick=100, offset_left=30),
                         y_range_controller=LiveAxisRange(fixed_range=[-1, 1]))
widget2.x_range_controller.crop_left_offset_to_data = True
plot2 = LiveLinePlot(pen="red")
widget2.addItem(plot2)
layout.addWidget(widget2, row=1, col=0)
data_connector2 = DataConnector(plot2, max_points=6000)

'''
Move view to the right on every 300 ticks (data update).
Y range is fixed to -1 and 1.
'''
widget3 = LivePlotWidget(title="Roll plot view every 1 sec, offset 30 sec, crop bottom = False",
                         y_range_controller=LiveAxisRange(roll_on_tick=100, offset_bottom=30),
                         x_range_controller=LiveAxisRange(fixed_range=[-1, 1]))
plot3 = LiveLinePlot(pen="yellow")
widget3.addItem(plot3)
layout.addWidget(widget3, row=0, col=1)
data_connector3 = DataConnector(plot3, max_points=6000)

'''
Move view to the right on every 300 ticks (data update).
Y range is fixed to -1 and 1.
'''
widget4 = LivePlotWidget(title="Roll plot view every 1 sec, offset 30 sec, crop bottom = True",
                         y_range_controller=LiveAxisRange(roll_on_tick=100, offset_bottom=30),
                         x_range_controller=LiveAxisRange(fixed_range=[-1, 1]))
widget4.y_range_controller.crop_bottom_offset_to_data = True
plot4 = LiveLinePlot(pen="yellow")
widget4.addItem(plot4)
layout.addWidget(widget4, row=1, col=1)
data_connector4 = DataConnector(plot4, max_points=6000)

layout.show()

Thread(target=examples.sin_wave_generator, args=(data_connector, data_connector2)).start()
Thread(target=examples.sin_wave_generator, args=(data_connector3, data_connector4), kwargs={"flip": True}).start()
signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
examples.app.exec()
examples.stop()
