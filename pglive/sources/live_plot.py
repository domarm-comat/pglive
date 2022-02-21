import numpy as np
import pyqtgraph as pg
from pyqtgraph import GraphicsObject

from pglive.sources.live_mixins import MixinLivePlot, MixinLeadingLine, MixinLiveBarPlot

if pg.Qt.QT_LIB == pg.Qt.PYQT6:
    from PyQt6.QtCore import pyqtSlot
else:
    from PyQt5.QtCore import pyqtSlot


class LiveLinePlot(pg.PlotDataItem, MixinLivePlot, MixinLeadingLine):
    """Line plot"""

    @pyqtSlot()
    def update_leading_line(self):
        if self._vl_kwargs is not None:
            self._vl_kwargs["line"].setPos(self.xData[-1])

        if self._hl_kwargs is not None:
            self._hl_kwargs["line"].setPos(self.yData[-1])
        self.update_leading_text(self.xData[-1], self.yData[-1])


class LiveScatterPlot(pg.ScatterPlotItem, MixinLivePlot, MixinLeadingLine):
    """Scatter plot"""

    @pyqtSlot()
    def update_leading_line(self):
        last_point = self.data[-1]
        if self._vl_kwargs is not None:
            self._vl_kwargs["line"].setPos(last_point[0])
        if self._hl_kwargs is not None:
            self._hl_kwargs["line"].setPos(last_point[1])

        self.update_leading_text(last_point[0], last_point[1])


class LiveHBarPlot(pg.BarGraphItem, MixinLiveBarPlot, MixinLeadingLine):
    """Horizontal Bar Plot"""

    def __init__(self, x0=0, bar_height=1, **kwargs):
        self.bar_height = bar_height
        self.x0 = x0
        super().__init__(x0=x0, y=[0], width=0, height=0, **kwargs)

    def setData(self, x: float, y: float, kwargs: dict):
        self.setOpts(x0=self.x0, y=x, height=self.bar_height, width=y, **kwargs)
        self.sigPlotChanged.emit()

    @pyqtSlot()
    def update_leading_line(self):
        if self._vl_kwargs is not None:
            self._vl_kwargs["line"].setPos(self.opts["width"][-1])
        if self._hl_kwargs is not None:
            self._hl_kwargs["line"].setPos(self.opts["y"][-1])
        self.update_leading_text(self.opts["width"][-1], self.opts["y"][-1])


class LiveVBarPlot(pg.BarGraphItem, MixinLiveBarPlot, MixinLeadingLine):
    """Vertical Bar Plot"""

    def __init__(self, y0=0, bar_width=1, **kwargs):
        self.bar_width = bar_width
        self.y0 = y0
        super().__init__(y0=y0, x=[0], width=0, height=0, **kwargs)

    def setData(self, x: float, y: float, kwargs: dict):
        self.setOpts(y0=self.y0, x=x, height=y, width=self.bar_width, **kwargs)
        self.sigPlotChanged.emit()

    @pyqtSlot()
    def update_leading_line(self):
        if self._vl_kwargs is not None:
            self._vl_kwargs["line"].setPos(self.opts["x"][-1])
        if self._hl_kwargs is not None:
            self._hl_kwargs["line"].setPos(self.opts["height"][-1])
        self.update_leading_text(self.opts["x"][-1], self.opts["height"][-1])


def make_live(plot: GraphicsObject):
    """Convert plot into Live plot"""
    if isinstance(plot, pg.BarGraphItem):
        # Create horizontal bar plot in case of bar plot
        plot.bar_width = 1
        plot.y0 = 0
        plot.slot_new_data = lambda y, x, kwargs: plot.setOpts(y0=plot.y0, x=x, height=y, width=plot.bar_width,
                                                               **kwargs)
    elif isinstance(plot, pg.PlotCurveItem):
        plot.slot_new_data = lambda y, x, kwargs: plot.setData(np.array(x), np.array(y), **kwargs)
    else:
        plot.slot_new_data = lambda y, x, kwargs: plot.setData(x, y, **kwargs)
