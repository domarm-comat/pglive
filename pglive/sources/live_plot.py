from typing import List, Union

import pyqtgraph as pg

if pg.Qt.QT_LIB == pg.Qt.PYQT6:
    from PyQt6.QtCore import pyqtSlot
else:
    from PyQt5.QtCore import pyqtSlot


class LiveMixin:

    @pyqtSlot(object, object, dict)
    def slot_new_data(self, y: List[Union[int, float]], x: List[Union[int, float]], kwargs):
        self.setData(x, y, **kwargs)


class LiveMixinBarPlot:

    @pyqtSlot(object, object, dict)
    def slot_new_data(self, y: List[Union[int, float]], x: List[Union[int, float]], kwargs):
        self.setData(x, y, kwargs)


class LiveLinePlot(pg.PlotDataItem, LiveMixin):
    ...


class LiveScatterPlot(pg.ScatterPlotItem, LiveMixin):
    ...


class LiveHBarPlot(pg.BarGraphItem, LiveMixinBarPlot):

    def __init__(self, x0=0, bar_height=1, **kwargs):
        self.bar_height = bar_height
        self.x0 = x0
        super().__init__(x0=x0, y=[0], width=0, height=0, **kwargs)

    def setData(self, x, y, kwargs):
        self.setOpts(x0=self.x0, y=x, height=self.bar_height, width=y, **kwargs)


class LiveVBarPlot(pg.BarGraphItem, LiveMixinBarPlot):

    def __init__(self, y0=0, bar_width=1, **kwargs):
        self.bar_width = bar_width
        self.y0 = y0
        super().__init__(y0=y0, x=[0], width=0, height=0, **kwargs)

    def setData(self, x, y, kwargs):
        self.setOpts(y0=self.y0, x=x, height=y, width=self.bar_width, **kwargs)
