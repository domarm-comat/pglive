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
        self.draw_counts = draw_counts

    def paint(self, p: QtGui.QPainter, *args: Any) -> None:
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self) -> QtCore.QRect:
        return QtCore.QRectF(self.picture.boundingRect())

    def setData(self, x_data: List[str], y_data: List[str], **kwargs: Dict) -> None:
        """y_data must be in format [[open, close, min, max], ...]"""
        if "heatmap" not in kwargs:
            raise Exception("Heatmap attribute must be set")
        self.x_data = list(range(len(x_data)+1))
        self.y_data = list(range(len(y_data)+1))
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen("w"))
        heatmap = kwargs["heatmap"]
        normalized_heatmap = (heatmap - np.min(heatmap)) / (np.max(heatmap) - np.min(heatmap))
        colors = self.colormap.map([normalized_heatmap])[0]

        p.save()
        img_data = []
        for ix, x in enumerate(x_data):
            for iy, y in enumerate(y_data):
                img_data.append(colors[ix][iy])

        cc = np.array(img_data)[:-1]
        img = QtGui.QImage(cc, len(x_data), len(y_data), QtGui.QImage.Format.Format_RGBA8888)
        p.drawImage(QtCore.QPoint(0, 0), img)

        if self.grid_pen is not None:
            p.setPen(self.grid_pen)
            for ix, x in enumerate(x_data):
                p.drawLine(ix, 0, ix, len(y_data))
            p.drawLine(ix+ 1, 0, ix+1, len(y_data))
            for iy, y in enumerate(y_data):
                p.drawLine(0, iy, len(x_data), iy)
            p.drawLine(0, iy + 1, len(x_data), iy + 1)

        p.restore()

        if self.draw_counts:
            matrix = p.transform()
            str_size = p.fontMetrics().boundingRect(str(np.max(heatmap)))
            mapped_size = matrix.map(QtCore.QPointF(str_size.width(), str_size.height()))
            if str_size.width() > str_size.height():
                scale = 1 / mapped_size.x()
            else:
                scale = 1 / mapped_size.y()
            p.scale(scale, -scale)
            matrix = p.transform()
            inv_matrix = matrix.inverted()[0]
            # Convert numbers to strings
            string_heatmap = heatmap.astype(str)
            bounding = self.boundingRect().toAlignedRect()
            for ix, x in enumerate(x_data):
                for iy, y in enumerate(y_data):
                    # Draw numbers inside pixels
                    p.drawText(inv_matrix.mapRect(QtCore.QRectF(ix, iy, 1, 1)),
                               QtCore.Qt.AlignmentFlag.AlignCenter, string_heatmap[ix][iy])

        p.end()
        self.prepareGeometryChange()
        self.informViewBoundsChanged()
        self.bounds = [None, None]
        self.sigPlotChanged.emit(self)

    def getData(self) -> Tuple[List[int], List[int]]:
        return self.x_data, self.y_data

    def data_bounds(self, ax: int = 0, offset: int = 0) -> Tuple[ndarray, ndarray]:
        if self.x_data == [] and self.y_data == []:
            return 0, 0
        if ax == 0:
            sub_range = self.x_data[-offset:]
        else:
            sub_range = self.y_data[-offset:]
        return np.nanmin(sub_range), np.nanmax(sub_range)

    def clear(self):
        self.x_data = []
        self.y_data = []
        self.output_y_data = []
        self.picture = QtGui.QPicture()
        self.prepareGeometryChange()
        self.informViewBoundsChanged()
        self.bounds = [None, None]
        self.sigPlotChanged.emit(self)