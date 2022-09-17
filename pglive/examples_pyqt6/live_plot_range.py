import pglive.examples_pyqt6 as examples
import signal
from threading import Thread
import pyqtgraph as pg

from pglive.kwargs import Axis
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_axis import LiveAxis
from pglive.sources.live_axis_range import LiveAxisRange
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
In this example live plot range is used to increase plotting performance.
"""

layout = pg.LayoutWidget()
layout.layout.setSpacing(0)
args = []
args2 = []

'''
Move view to the right on every 300 ticks (data update).
Y range is automatically adjudicating every tick.
'''
widget = LivePlotWidget(title=f"Rolling X view range, auto Y range @ 100Hz",
                        x_range_controller=LiveAxisRange(roll_on_tick=300))
plot = LiveLinePlot(pen="green")
widget.addItem(plot)
layout.addWidget(widget)
args.append(DataConnector(plot, max_points=300, update_rate=100))

'''
Move view to the right on every 300 ticks (data update).
Y range is fixed to -1 and 1.
'''

widget = LivePlotWidget(title=f"Rolling X view range, fixed Y range @ 100Hz",
                        x_range_controller=LiveAxisRange(roll_on_tick=300),
                        y_range_controller=LiveAxisRange(fixed_range=[-1, 1]))
plot = LiveLinePlot(pen="green")
widget.addItem(plot)
layout.addWidget(widget)
args.append(DataConnector(plot, max_points=300, update_rate=100))

'''
Move view to the right on every 150 ticks (data update).
Y range is fixed to -1 and 1.
In this case we have max. of 300 points in the buffer, but view is fixed to the last 150.
'''

widget = LivePlotWidget(title=f"Rolling X at half of max points, fixed Y range @ 100Hz",
                        x_range_controller=LiveAxisRange(roll_on_tick=150),
                        y_range_controller=LiveAxisRange(fixed_range=[-1, 1]))
plot = LiveLinePlot(pen="green")
widget.addItem(plot)
layout.addWidget(widget, row=1, col=0)
args.append(DataConnector(plot, max_points=300, update_rate=100))

'''
Move view to the right on every 150 ticks (data update).
Y range is fixed to -1 and 1.
In this case we set offset_left to 0.5 (50% of last 150 points in the DataConnector's buffer).
Like this we can always display fixed first 150 ticks on every roll (not starting with blank view).
Of course we need to set max_points to value 2 * roll_on_ticks.
'''

widget = LivePlotWidget(title=f"Rolling X at half of max points with 50% left offset, fixed Y range @ 100Hz",
                        x_range_controller=LiveAxisRange(roll_on_tick=150, offset_left=0.5),
                        y_range_controller=LiveAxisRange(fixed_range=[-1, 1]))
plot = LiveLinePlot(pen="green")
widget.addItem(plot)
layout.addWidget(widget, row=1, col=1)
args.append(DataConnector(plot, max_points=300, update_rate=100))

'''
Move view to the top on every 300 ticks (data update).
X range is fixed to -1 and 1.
'''

widget = LivePlotWidget(title=f"Rolling X at half of max points with 50% left offset, fixed Y range @ 100Hz",
                        x_range_controller=LiveAxisRange(fixed_range=[-1, 1]),
                        y_range_controller=LiveAxisRange(roll_on_tick=300))
plot = LiveLinePlot(pen="white")
widget.addItem(plot)
layout.addWidget(widget, row=0, col=2)
args2.append(DataConnector(plot, max_points=300, update_rate=100))

'''
Move view to the top on every 150 ticks (data update).
X range is fixed to -1 and 1.
'''

widget = LivePlotWidget(title=f"Rolling X at half of max points with 50% left offset, fixed Y range @ 100Hz",
                        x_range_controller=LiveAxisRange(fixed_range=[-1, 1]),
                        y_range_controller=LiveAxisRange(roll_on_tick=150, offset_left=0.5))
plot = LiveLinePlot(pen="white")
widget.addItem(plot)
layout.addWidget(widget, row=1, col=2)
args2.append(DataConnector(plot, max_points=300, update_rate=100))

"""
Move view to the right on every 600 ticks (data update).
Y range is automatically adjudicating every tick.
"""
left_axis = LiveAxis("left", axisPen="red", textPen="red")
bottom_axis = LiveAxis("bottom", axisPen="green", textPen="green", **{Axis.TICK_FORMAT: Axis.TIME})
time_axis_plot_widget = LivePlotWidget(title="Rolling X view range, auto Y range @ 100Hz",
                                       axisItems={'bottom': bottom_axis, 'left': left_axis},
                                       x_range_controller=LiveAxisRange(roll_on_tick=600))
plot = LiveLinePlot(pen="yellow")
time_axis_plot_widget.addItem(plot)
args.append(DataConnector(plot, max_points=600))
layout.addWidget(time_axis_plot_widget, row=2, col=0)

"""
Move view to the right on every 300 ticks (data update).
Y range is automatically adjudicating every tick.
In this case we set offset_left to 0.5 (50% of last 300 points in the DataConnector's buffer).
Like this we can always display fixed first 300 ticks on every roll (not starting with blank view).
Of course we need to set max_points to value 2 * roll_on_ticks.
"""
left_axis = LiveAxis("left", axisPen="red", textPen="red")
bottom_axis = LiveAxis("bottom", axisPen="green", textPen="green", **{Axis.TICK_FORMAT: Axis.TIME})
time_axis_plot_widget = LivePlotWidget(
    title="Rolling X at half of max points with 50% left offset, fixed Y range @ 100Hz",
    axisItems={'bottom': bottom_axis, 'left': left_axis},
    x_range_controller=LiveAxisRange(roll_on_tick=300, offset_left=0.5))
plot = LiveLinePlot(pen="yellow")
time_axis_plot_widget.addItem(plot)
args.append(DataConnector(plot, max_points=600))
layout.addWidget(time_axis_plot_widget, row=2, col=1)

"""
Move view to the right on every 100 ticks (data update).
Y range is automatically adjudicating every tick.
"""
left_axis = LiveAxis("left", axisPen="red", textPen="red")
bottom_axis = LiveAxis("bottom", axisPen="green", textPen="green", **{Axis.TICK_FORMAT: Axis.TIME})
time_axis_plot_widget = LivePlotWidget(title="Rolling X at 1/6 of max points, fixed Y range @ 100Hz",
                                       axisItems={'bottom': bottom_axis, 'left': left_axis},
                                       x_range_controller=LiveAxisRange(roll_on_tick=100))
plot = LiveLinePlot(pen="yellow")
time_axis_plot_widget.addItem(plot)
args.append(DataConnector(plot, max_points=600))
layout.addWidget(time_axis_plot_widget, row=2, col=2)

# ---

layout.show()
Thread(target=examples.sin_wave_generator, args=args).start()
Thread(target=examples.sin_wave_generator, args=args2, kwargs={"flip": True}).start()
examples.app.exec()
examples.stop()
