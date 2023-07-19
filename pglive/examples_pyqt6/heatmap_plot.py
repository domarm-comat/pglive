import numpy as np
import pyqtgraph as pg

import pglive.examples_pyqt6 as examples
from pglive.sources.live_HeatMap import LiveHeatMap
from pglive.sources.live_plot_widget import LivePlotWidget

"""
Line plot is displayed in this example.
"""
win = LivePlotWidget(title="Line Plot @ 100Hz")

# color map
cmap = pg.colormap.get('CET-D1')
imv = LiveHeatMap(colormap=cmap)
win.addItem(imv)
imv.setData(["A", "B", "C", "E"], ["A", "B", "C", "F"], heatmap=np.array([[10, 5, 11, 5], [1, 5, 8, 10], [0, 3, 6, 1], [25, 7, 12, 17]]))

# data_connector = DataConnector(plot, max_points=600)

win.show()

# Thread(target=examples.sin_wave_generator, args=(data_connector,)).start()
# signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
examples.app.exec()
examples.stop()
