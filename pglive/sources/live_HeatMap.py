import time
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
                 heatmap: Optional[heatmap_data_T] = None) -> None:
        """Choose colors of candle"""
        pg.GraphicsObject.__init__(self)
        self.colormap = colormap
        self.picture = QtGui.QPicture()
        self.x_data = x_data
        if self.x_data is None:
            self.x_data = []
        self.y_data = x_data
        if self.y_data is None:
            self.y_data = []
        self.heatmap = heatmap
        if heatmap is None:
            self.heatmap = np.array([[], []])
        # self.setData(self.x_data, self.y_data, heatmap = self.heatmap)

    def paint(self, p: QtGui.QPainter, *args: Any) -> None:
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self) -> QtCore.QRect:
        return QtCore.QRectF(0,0,5,5)

    def setData(self, x_data: List[str], y_data: List[str], **kwargs: Dict) -> None:
        """y_data must be in format [[open, close, min, max], ...]"""
        if "heatmap" not in kwargs:
            raise Exception("Heatmap attribute must be set")

        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(pg.mkPen("w"))
        p.setBrush(pg.mkBrush("g"))
        heatmap = kwargs["heatmap"]

        normalized_heatmap = (heatmap - np.min(heatmap)) / (np.max(heatmap) - np.min(heatmap))
        colors = self.colormap.map([normalized_heatmap])[0]

        x_size = 1 / heatmap.shape[0] if heatmap.shape[0] > 0 else 0
        y_size = 1 / heatmap.shape[1] if heatmap.shape[1] > 0 else 0

        font = p.font()
        font.setPixelSize(1)
        p.setFont(font)

        p.save()
        p.setPen(QtCore.Qt.PenStyle.NoPen)

        for ix, x in enumerate(x_data):
            for iy, y in enumerate(y_data):
                rect = QtCore.QRectF(ix * x_size, iy * y_size, x_size, y_size)
                p.setBrush(pg.mkBrush(colors[ix][iy]))
                p.drawRect(rect)
        p.restore()


        # p.translate(0, 1)
        p.scale(1, -1)
        p.rotate(1)
        # p.drawText(0, 0, "Y0")
        # A = self.getViewBox().mapToScene(QtCore.QPointF(0, 0))
        # B = self.getViewBox().mapSceneToView(QtCore.QPointF(300, 300))
        # print(A, B)
        # print(self.getViewBox().viewRect(), self.scene().width(), self.scene().height())


        self.sigPlotChanged.emit(self)

    def getData(self) -> Tuple[List[float], List[Tuple[float, ...]]]:
        return self.x_data, self.y_data

    def data_bounds(self, ax: int = 0, offset: int = 0) -> Tuple[ndarray, ndarray]:
        return np.nanmin([0, 10]), np.nanmax([0, 10])
