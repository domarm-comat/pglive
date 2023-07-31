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
imv = LiveHeatMap(colormap=cmap, grid_pen=pg.mkPen("red"))
win.addItem(imv)
for i in range(10):
    imv.setData(["A", "B", "C", "E", "G", "H"], ["A", "B", "C", "F", "E", "H"],
                heatmap=np.array([[1, 5, 1, 3, 1, 4], [1, 5, 8, 1, 9, 15], [9, 3, 6, 1, 3, 5], [2, 7, 1, 7, 1, 12], [2, 7, 1, 7, 23, 12], [2, 7, 1, 7, 23, 12]]))
# data_connector = DataConnector(plot, max_points=600)

win.show()

# Thread(target=examples.sin_wave_generator, args=(data_connector,)).start()
# signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
examples.app.exec()
examples.stop()
