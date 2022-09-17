from typing import List, Tuple

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from pglive.sources.live_mixins import MixinLivePlot, MixinLeadingLine


class LiveCandleStickPlot(pg.GraphicsObject, MixinLivePlot, MixinLeadingLine):
    """Live candlestick plot, plotting data [[open, close, min, max], ...]"""
    sigPlotChanged = QtCore.Signal(object)

    def __init__(self, outline_color: str = "w", high_color: str = 'g', low_color: str = 'r') -> None:
        """Choose colors of candle"""
        pg.GraphicsObject.__init__(self)
        self.x_data = []
        self.y_data = []
        self.output_y_data = []
        self.outline_pen = pg.mkPen(outline_color)
        self.high_brush = pg.mkBrush(high_color)
        self.low_brush = pg.mkBrush(low_color)
        self.picture = QtGui.QPicture()

    def paint(self, p, *args) -> None:
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self) -> QtCore.QRect:
        return QtCore.QRectF(self.picture.boundingRect())

    def setData(self, x_data: List[float], y_data: List[Tuple[float]]) -> None:
        """y_data must be in format [[open, close, min, max], ...]"""
        self.x_data = x_data
        self.y_data = y_data
        self.output_y_data = []
        if len(x_data) != len(y_data):
            raise Exception("Len of x_data must be the same as y_data")

        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(self.outline_pen)
        try:
            w = (x_data[1] - x_data[0]) / 3.
        except IndexError:
            w = 1 / 3

        for index, (open, close, min, max) in enumerate(y_data):
            t = x_data[index]
            p.drawLine(QtCore.QPointF(t, min), QtCore.QPointF(t, max))
            if open > close:
                p.setBrush(self.low_brush)
            else:
                p.setBrush(self.high_brush)
            p.drawRect(QtCore.QRectF(t - w, open, w * 2, close - open))
            self.output_y_data.extend([min, max])
        p.end()

        self.prepareGeometryChange()
        self.informViewBoundsChanged()
        self.bounds = [None, None]
        self.sigPlotChanged.emit(self)

    def update_leading_line(self) -> None:
        """Leading line will display all four fields"""
        last_x_point = self.x_data[-1]
        last_y_point = self.y_data[-1][0]
        if self._vl_kwargs is not None:
            self._vl_kwargs["line"].setPos(last_x_point)
        if self._hl_kwargs is not None:
            self._hl_kwargs["line"].setPos(last_y_point)

        y_text = str([round(x, 4) for x in self.y_data[-1]])
        self.update_leading_text(last_x_point, last_y_point, y_text=y_text)

    def getData(self):
        return self.x_data, self.y_data

    def data_bounds(self, ax=0, offset=0) -> Tuple:
        x, y = self.x_data, self.output_y_data
        if ax == 0:
            sub_range = x[-offset:]
        else:
            sub_range = y[-offset * 2:]
        return np.nanmin(sub_range), np.nanmax(sub_range)
