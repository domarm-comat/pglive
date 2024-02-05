# Live pyqtgraph plot

Pglive package adds support for thread-safe live plotting based on pyqtgraph.  
It supports PyQt5, PyQt6 and PySide6.

# Description #

Pyqtgraph doesn't offer easy way to implement live plotting out of the box.
The aim of PgLive module is to provide easy way of thread-safe live plotting.
To do this, PgLive provides DataConnector object, which consumes data 
and manages data plotting. DataConnector interface provides Pause and Resume method, update rate and maximum number of
plotted points. All that needs to be done is to connect plots and data sources with DataConnector.
Once data is collected, DataConnector is sending signals to the GUI main loop.

**Focus on data handling - leave plotting to pglive.**

You can find many examples for PyQt5, PyQt6 or PySide6.

# Code example #

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
Line plot is displayed in this example.
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
# Start sin_wave_generator in new Thread and send data to data_connector
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
User can specify when and how is a new view of plotted data calculated.

Have a look in the [live_plot_range.py](https://github.com/domarm-comat/pglive/blob/main/pglive/examples_pyqt6/live_plot_range.py) example.

![Range_optimization](https://i.postimg.cc/3wrMbbTY/a.gif)

In case you want to plot wider area with LiveAxisRange you can use `crop_offset_to_data` flag.
For example, you want to store 60 seconds, display 30 seconds in a view and move view every 1 second.
You will end up with big empty space to the left if `crop_offset_to_data = False`.
Take a look into [crop_offset_to_data.py](https://github.com/domarm-comat/pglive/blob/main/pglive/examples_pyqt6/crop_offset_to_data.py) example.

![crop_offset_to_data](https://i.postimg.cc/90X40Ng7/Peek-2022-09-24-15-20.gif)

Introduced in *v0.4.0*

# Crosshair #

Pglive comes with built-in Crosshair as well. Take a look at [crosshair.py](https://github.com/domarm-comat/pglive/blob/main/pglive/examples_pyqt6/crosshair.py) example.

![Crosshair](https://i.postimg.cc/1z75GZLV/pglive-crosshair.gif)

# Leading lines #

Leading line displays horizontal or vertical line (or both) at the last plotted point.  
You can choose its color and which axis value is displayed along with it.  
Example at [leading_line.py](https://github.com/domarm-comat/pglive/blob/main/pglive/examples_pyqt6/leading_line.py)

![Leading lines](https://i.postimg.cc/bYKQGBNp/leading-line.gif)

# Axis #

To make life easier, pglive includes a few axis improvements:

- Colored axis line using new `axisPen` attribute
- Time and DateTime tick format, converting timestamp into human-readable format
- Use `tick_angle` attribute to change tick angle from 0 default degree  

Example at [axis.py](https://github.com/domarm-comat/pglive/blob/main/pglive/examples_pyqt6/axis.py)

[![Axis example](https://i.postimg.cc/SQ2hDxBr/Peek-2023-09-03-15-58.gif)](https://postimg.cc/RqBy04V6)

# Summary #

- With Pglive You've got an easy Thread-safe live plot implementation in Pyqt5, Pyqt6 or PySide6
- You can use all `kwargs` that works in [pyqtgraph](https://pyqtgraph.readthedocs.io/en/latest/getting_started/index.html#getting-started-ref)
- Use your plots with `DataConnector` directly
- It works with Python3.9, 3.10, 3.11 and 3.12 as well
- Multiple optimized plot types
- Many examples for easy start

If you find PgLive helpful, please consider [supporting me](https://ko-fi.com/domarmcomatsk), it helps a lot!  
Thanks to all contributors, feel free to suggest missing feature or any bug on [GitHub](https://github.com/domarm-comat/pglive/issues).
