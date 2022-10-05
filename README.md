# Live pyqtgraph plot

Pglive package adds support for thread-safe live plotting to pyqtgraph.  
It supports PyQt5, PyQt6, PySide2 and PySide6.

# Description #

By default, pyqtgraph doesn't support live plotting. Aim of this package is to provide easy implementation of Line,
Scatter and Bar Live plot. Every plot is connected with it's DataConnector, which sole purpose is to consume data points
and manage data re-plotting. DataConnector interface provides Pause and Resume method, update rate and maximum number of
plotted points. Each time data point is collected, call `DataConnector.cb_set_data`
or `DataConnector.cb_append_data_point` callback. That's all You need to update plot with new data. Callbacks are Thread
safe, so it works nicely in applications with multiple data collection Threads.

**Focus on data collection and leave plotting to pglive.**

To make firsts steps easy, package comes with many examples implemented in PyQt5 or PyQt6.
Support for PySide2 and PySide6 was added in version 0.3.0.

# Code examples #

```python
import sys
from math import sin
from threading import Thread
from time import sleep

from PyQt6.QtWidgets import QApplication

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
In this example Line plot is displayed.
"""
app = QApplication(sys.argv)
running = True

plot_widget = LivePlotWidget(title="Line Plot @ 100Hz")
plot_curve = LiveLinePlot()
plot_widget.addItem(plot_curve)
# DataConnector holding 600 points and plots @ 100Hz
data_connector = DataConnector(plot_curve, max_points=600, update_rate=100)


def sin_wave_generator(connector):
    """Sine wave generator"""
    x = 0
    while running:
        x += 1
        data_point = sin(x * 0.01)
        # Callback to plot new data point
        connector.cb_append_data_point(data_point, x)

        sleep(0.01)


plot_widget.show()
Thread(target=sin_wave_generator, args=(data_connector,)).start()
app.exec()
running = False
```

Output:

![Plot example](https://i.postimg.cc/RFYGfNS6/pglive.gif)

To run built-in examples, use python3 -m parameter like:  
`python3 -m pglive.examples_pyqt6.all_plot_types`  
`python3 -m pglive.examples_pyqt6.crosshair`

# Using PyQt5/6 designer #

1. Add QWidget to Your layout
2. Promote QWidget to `LivePlotWidget` and set header file to `pglive.sources.live_plot_widget`
3. Click `Add` and `Promote` button

![All plot types](https://i.postimg.cc/m25NVJZm/designer-promotion.png)

# Available plot types #

Pglive supports four plot types: `LiveLinePlot`, `LiveScatterPlot`, `LiveHBarPlot` (horizontal bar plot),
`LiveVBarPlot` (vertical bar plot) and `LiveCandleStickPlot`.

![All plot types](https://i.postimg.cc/637CsKRC/pglive-allplots.gif)
![CandleStick plot](https://i.postimg.cc/0QcmMMb0/plot-candlestick.gif)
![live-categorized-bar.gif](https://i.postimg.cc/xqrwXXjY/live-categorized-bar.gif)

# Plot speed optimizations  #

Scaling plot view to plotted data has a huge impact on plotting performance.
Re-plotting might be laggy when using high update frequencies and multiple plots.    
To increase plotting performance, pglive introduces `LiveAxisRange`, that can be used in `LivePlotWidget`.
User can now specify when and how is new view of plotted data calculated.

Have a look in the `live_plot_range.py` example, to see how it can be used.

![Range_optimization](https://i.postimg.cc/3wrMbbTY/a.gif)

In case you want to plot wider area with LiveAxisRange you can use crop_offset_to_data flag.
For example, you want to store 60 seconds, display 30 seconds in a view and move view every 1 second.
You will have big empty space to the left without setting flag to True.
Have a look into crop_offset_to_data example.

![crop_offset_to_data](https://i.postimg.cc/90X40Ng7/Peek-2022-09-24-15-20.gif)

Introduced in *v0.4.0*

# Crosshair #

Pglive comes with built-in Crosshair as well.

![Crosshair](https://i.postimg.cc/1z75GZLV/pglive-crosshair.gif)

# Leading lines #

Leading line displays horizontal or vertical line (or both) at the last plotted point.  
You can choose it's color and which axis value is displayed along with it.  

![Leading lines](https://i.postimg.cc/bYKQGBNp/leading-line.gif)

# Axis #

To make life easier, pglive includes few axis improvements:

- Colored axis line using new `axisPen` attribute
- Time and DateTime tick format, converting timestamp into human-readable format

![Crosshair](https://i.postimg.cc/8kr0L2YJ/pglive-axis.gif)

# Summary #

- With Pglive You've got easy Thread-safe implementation of fast Live plots
- You can use all `kwargs` specified in pyqtgraph
- Use your pyqtgraph plots with `DataConnector` directly, no need to use specific `LivePlot` class 
- **Focus on Data Handling, not Data Plotting**