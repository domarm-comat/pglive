# Live pyqtgraph plot

Pglive package adds support for thread-safe live plotting to pyqtgraph.  
It supports PyQt5 and PyQt6.

# Description #

By default, pyqtgraph doesn't support live plotting.
Aim of this package is to provide easy implementation of Line, Scatter and Bar Live plot.
Every plot is connected with it's DataConnector, which sole purpose is to consume data points and manage data re-plotting.
DataConnector interface provides Pause and Resume method, update rate and maximum number of plotted points.
Each time data point is collected, call `DataConnector.cb_set_data` or `DataConnector.cb_append_data_point` callback.
That's all You need to update plot with new data.
Callbacks are Thread safe, so it works nicely in applications with multiple data collection Threads.  

**Focus on data collection and leave plotting to pglive.**

To make firsts steps easy, package comes with many examples implemented in PyQt5 or PyQt6.

# Code examples #

```python
import pglive.examples_pyqt6 as examples
import signal
from threading import Thread

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
In this example Line plot is displayed.
"""
win = LivePlotWidget(title="Line Plot @ 100Hz")
plot = LiveLinePlot()
win.addItem(plot)

data_connector = DataConnector(plot, max_points=600)

win.show()

Thread(target=examples.sin_wave_generator, args=(data_connector,)).start()
signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
examples.app.exec()
examples.stop()
```

Output:  

![Plot example](https://i.postimg.cc/RFYGfNS6/pglive.gif)

# Crosshair #

Pglive comes with built-in Crosshair as well.

![Crosshair](https://i.postimg.cc/1z75GZLV/pglive-crosshair.gif)

# Available plot types #

Pglive supports four plot types: `LiveLinePlot`, `LiveScatterPlot`, `LiveHBarPlot` (horizontal bar plot) and `LiveVBarPlot` (vertical bar plot).

![All plot types](https://i.postimg.cc/637CsKRC/pglive-allplots.gif)

# Summary #

- With Pglive You've got easy Thread-safe implementation of fast Live plots.
- You can use all `kwargs` specified in pyqtgraph
- **Focus on Data Collection, not Data Plotting**