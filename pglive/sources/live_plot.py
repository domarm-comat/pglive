from typing import Dict, Any, Tuple, List

import numpy as np  # type: ignore
import pyqtgraph as pg  # type: ignore

from pglive.sources.live_mixins import MixinLivePlot, MixinLeadingLine, MixinLiveBarPlot


class LiveLinePlot(pg.PlotDataItem, MixinLivePlot, MixinLeadingLine):
    """Line plot"""

    def update_leading_line(self) -> None:
        if self._vl_kwargs is not None:
            self._vl_kwargs["line"].setPos(self.xData[-1])

        if self._hl_kwargs is not None:
            self._hl_kwargs["line"].setPos(self.yData[-1])
        self.update_leading_text(self.xData[-1], self.yData[-1])

    def clear(self):
        try:
            self.clear_leading_lines()
        except:
            pass

        super().clear()

    def data_bounds(self, ax: int = 0, offset: int = 0) -> Tuple:
        x, y = self.getData()
        if x is None and y is None:
            return 0, 0
        if ax == 0:
            sub_range = x[-offset:]
        else:
            sub_range = y[-offset:]
        return np.nanmin(sub_range), np.nanmax(sub_range)

    def data_tick(self, ax: int = 0):
        x, y = self.getData()
        if x is None and y is None:
            return 0, 0
        if ax == 0:
            return x[0] if len(x) == 1 else x[1] - x[0]
        else:
            return y[0] if len(y) == 1 else y[1] - y[0]


class LiveScatterPlot(pg.ScatterPlotItem, MixinLivePlot, MixinLeadingLine):
    """Scatter plot"""

    def clear(self):
        try:
            self.clear_leading_lines()
        except AttributeError:
            pass

        super().clear()

    def update_leading_line(self) -> None:
        last_point = self.data[-1]
        if self._vl_kwargs is not None:
            self._vl_kwargs["line"].setPos(last_point[0])
        if self._hl_kwargs is not None:
            self._hl_kwargs["line"].setPos(last_point[1])

        self.update_leading_text(last_point[0], last_point[1])

    def data_bounds(self, ax: int = 0, offset: int = 0) -> Tuple[np.ndarray, np.ndarray]:
        x, y = self.getData()
        if x.size == 0 and y.size == 0:
            return 0, 0
        if ax == 0:
            sub_range = x[-offset:]
        else:
            sub_range = y[-offset:]
        return np.nanmin(sub_range), np.nanmax(sub_range)

    def data_tick(self, ax: int = 0):
        x, y = self.getData()
        if x.size == 0 and y.size == 0:
            return 0, 0
        if ax == 0:
            return x[0] if len(x) == 1 else x[1] - x[0]
        else:
            return y[0] if len(y) == 1 else y[1] - y[0]


class LiveHBarPlot(pg.BarGraphItem, MixinLiveBarPlot, MixinLeadingLine):
    """Horizontal Bar Plot"""

    def __init__(self, x0: float = 0., bar_height: float = 1., **kwargs: Any) -> None:
        self.bar_height = bar_height
        self.x0 = x0
        super().__init__(x0=x0, y=[0], width=0, height=0, **kwargs)

    def setData(self, x_data: float, y_data: float, **kwargs: Dict) -> None:
        self.setOpts(x0=self.x0, y=x_data, height=self.bar_height, width=y_data, **kwargs)
        self.sigPlotChanged.emit()

    def clear(self):
        self.setOpts(x0=self.x0, y=[], height=self.bar_height, width=[])
        self.sigPlotChanged.emit()

    def getData(self) -> Tuple[List[float], List[float]]:
        return self.opts["width"], self.opts["y"]

    def update_leading_line(self) -> None:
        if self.opts["width"] is [] and self.opts["y"] is []:
            self.clear_leading_lines()
            return

        if self._vl_kwargs is not None:
            self._vl_kwargs["line"].setPos(self.opts["width"][-1])
        if self._hl_kwargs is not None:
            self._hl_kwargs["line"].setPos(self.opts["y"][-1])
        self.update_leading_text(self.opts["width"][-1], self.opts["y"][-1])

    def data_bounds(self, ax: int = 0, offset: int = 0) -> Tuple[np.ndarray, np.ndarray]:
        x, y = self.getData()
        if x is [] and y is []:
            return 0, 0
        if ax == 0:
            sub_range = x[-offset:]
        else:
            sub_range = y[-offset:]
        return np.nanmin(sub_range), np.nanmax(sub_range)

    def data_tick(self, ax: int = 0):
        x, y = self.getData()
        if x is [] and y is []:
            return 0, 0
        if ax == 0:
            return x[0] if len(x) == 1 else x[1] - x[0]
        else:
            return y[0] if len(y) == 1 else y[1] - y[0]


class LiveVBarPlot(pg.BarGraphItem, MixinLiveBarPlot, MixinLeadingLine):
    """Vertical Bar Plot"""

    def __init__(self, y0: float = 0, bar_width: float = 1, **kwargs: Any) -> None:
        self.bar_width = bar_width
        self.y0 = y0
        super().__init__(y0=y0, x=[0], width=0, height=0, **kwargs)

    def setData(self, x_data: float, y_data: float, **kwargs: Dict) -> None:
        self.setOpts(y0=self.y0, x=x_data, height=y_data, width=self.bar_width, **kwargs)
        self.sigPlotChanged.emit()

    def clear(self):
        self.setOpts(y0=self.y0, x=[], height=[], width=self.bar_width)
        self.sigPlotChanged.emit()

    def update_leading_line(self) -> None:
        if self.opts["x"] is [] and self.opts["height"] is []:
            self.clear_leading_lines()
            return

        if self._vl_kwargs is not None:
            self._vl_kwargs["line"].setPos(self.opts["x"][-1])
        if self._hl_kwargs is not None:
            self._hl_kwargs["line"].setPos(self.opts["height"][-1])
        self.update_leading_text(self.opts["x"][-1], self.opts["height"][-1])

    def data_bounds(self, ax: int = 0, offset: int = 0) -> Tuple[np.ndarray, np.ndarray]:
        x, y = self.getData()
        if x is [] and y is []:
            return 0, 0
        if ax == 0:
            sub_range = x[-offset:]
        else:
            sub_range = y[-offset:]
        return np.nanmin(sub_range), np.nanmax(sub_range)

    def data_tick(self, ax: int = 0):
        x, y = self.getData()
        if x is [] and y is []:
            return 0, 0
        if ax == 0:
            return x[0] if len(x) == 1 else x[1] - x[0]
        else:
            return y[0] if len(y) == 1 else y[1] - y[0]


def make_live(plot: pg.GraphicsObject) -> None:
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

    def data_bounds(ax: int = 0, offset: int = 0) -> Tuple[np.ndarray, np.ndarray]:
        x, y = plot.getData()
        if x is None and y is None:
            return 0, 0
        if ax == 0:
            sub_range = x[-offset:]
        else:
            sub_range = y[-offset:]
        return np.nanmin(sub_range), np.nanmax(sub_range)

    def data_tick(self, ax: int = 0):
        x, y = self.getData()
        if x is None and y is None:
            return 0, 0
        if ax == 0:
            return x[0] if len(x) == 1 else x[1] - x[0]
        else:
            return y[0] if len(y) == 1 else y[1] - y[0]

    plot.data_bounds = data_bounds
    plot.data_tick = data_tick
    plot.slot_connector_toggle = lambda data_connector, flag: plot.plot_widget.slot_connector_toggle(data_connector,
                                                                                                     flag)
    plot.slot_roll_tick = lambda data_connector, tick: plot.plot_widget.slot_roll_tick(data_connector, tick)
