import time
from functools import lru_cache
from typing import List, Tuple, Any, Dict, Union, Optional

import numpy as np
import pyqtgraph as pg  # type: ignore
from numpy import ndarray
from pyqtgraph.Qt import QtCore, QtGui  # type: ignore

from pglive.sources.live_mixins import MixinLivePlot

heatmap_data_T = Tuple[List[Union[float, int]], List[Union[float, int]]]


class LiveHeatMap(pg.GraphicsObject, MixinLivePlot):
    """Live candlestick plot, plotting data [[open, close, min, max], ...]"""
    sigPlotChanged = QtCore.Signal(object)

    def __init__(self, colormap: pg.ColorMap, x_data: Optional[List[str]] = None, y_data: Optional[List[str]] = None,
                 heatmap: Optional[heatmap_data_T] = None, draw_counts: bool = True, grid_pen: Optional[QtGui.QPen] = None) -> None:
        """Choose colors of candle"""
        pg.GraphicsObject.__init__(self)
        self.colormap = colormap
        self.picture = QtGui.QPicture()
        self.x_data = x_data
        if self.x_data is None:
            self.x_data = []
        self.y_data = y_data
        if self.y_data is None:
            self.y_data = []
        self.heatmap = heatmap
        if heatmap is None:
            self.heatmap = np.array([[], []])
        self.grid_pen = grid_pen
        if grid_pen is None:
            self.grid_pen = QtCore.Qt.PenStyle.NoPen
        self.draw_counts = draw_counts

    def paint(self, p: QtGui.QPainter, *args: Any) -> None:
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self) -> QtCore.QRect:
        return QtCore.QRectF(0, 0, 5, 5)

    def setData(self, x_data: List[str], y_data: List[str], **kwargs: Dict) -> None:
        """y_data must be in format [[open, close, min, max], ...]"""
        if "heatmap" not in kwargs:
            raise Exception("Heatmap attribute must be set")

        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen("w"))
        heatmap = kwargs["heatmap"]

        normalized_heatmap = (heatmap - np.min(heatmap)) / (np.max(heatmap) - np.min(heatmap))
        colors = self.colormap.map([normalized_heatmap])[0]

        x_size = 1 / heatmap.shape[0] if heatmap.shape[0] > 0 else 0
        y_size = 1 / heatmap.shape[1] if heatmap.shape[1] > 0 else 0

        p.save()
        p.setPen(self.grid_pen)

        for ix, x in enumerate(x_data):
            for iy, y in enumerate(y_data):
                p.setBrush(self.get_brush(tuple(colors[ix][iy])))
                p.drawRect(QtCore.QRectF(ix * x_size, iy * y_size, x_size, y_size))
        p.restore()

        if self.draw_counts:
            font = p.font()
            font.setPointSize(1000)
            p.setFont(font)

            matrix = p.transform()
            w = 1 / len(x_data)
            h = 1 / len(y_data)
            str_size = p.fontMetrics().boundingRect(str(np.max(heatmap)))
            mapped_size = matrix.map(QtCore.QPointF(str_size.width(), str_size.height()))
            if str_size.width() > str_size.height():
                ideal_w = w * 0.9
                scale = ideal_w / mapped_size.x()
            else:
                ideal_h = h
                scale = ideal_h / mapped_size.y()
            p.scale(scale, -scale)
            matrix = p.transform()
            inv_matrix = matrix.inverted()[0]

            for ix, x in enumerate(x_data):
                for iy, y in enumerate(y_data):
                    p.drawText(inv_matrix.mapRect(QtCore.QRectF(ix * x_size, iy * y_size, x_size, y_size)),
                               QtCore.Qt.AlignmentFlag.AlignCenter, str(heatmap[ix][iy]))

        self.sigPlotChanged.emit(self)

    def getData(self) -> Tuple[List[float], List[Tuple[float, ...]]]:
        return self.x_data, self.y_data

    def data_bounds(self, ax: int = 0, offset: int = 0) -> Tuple[ndarray, ndarray]:
        return np.nanmin([0, 10]), np.nanmax([0, 10])

    @lru_cache
    def get_brush(self, color):
        return pg.mkBrush(color)
