import signal
from threading import Thread

import pglive.examples_pyqt6 as examples
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_candleStickPlot import LiveCandleStickPlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
In this example Scatter plot is displayed.
"""
win = LivePlotWidget(title="Candlestick Plot @ 10Hz")
plot = LiveCandleStickPlot()
win.addItem(plot)

data_connector = DataConnector(plot, max_points=50, update_rate=10)

win.show()

Thread(target=examples.candle_generator, args=(data_connector,)).start()
signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
examples.app.exec()
examples.stop()
