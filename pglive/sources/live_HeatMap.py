from functools import cache
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
                 heatmap: Optional[heatmap_data_T] = None, grid_pen: Optional[QtGui.QPen] = None,
                 counts_pen: Optional[QtGui.QPen] = None) -> None:
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
        self.input_x_data = []
        self.input_y_data = []
        self.heatmap = heatmap
        if heatmap is None:
            self.heatmap = np.array([[], []])
        self.grid_pen = grid_pen
        self.counts_pen = counts_pen
        self.drawing = False
        self.image_item = pg.ImageItem()
        self.image_item.setColorMap(self.colormap)
        self.histogram = pg.HistogramLUTWidget()
        self.histogram.setImageItem(self.image_item)
        self.histogram.gradient.setColorMap(self.colormap)
        self.histogram.gradient.showTicks(False)
        self.histogram.sigLookupTableChanged.connect(self.slot_gradient_changed)
        self.histogram.sigLevelChangeFinished.connect(self.slot_levels_changed)

    def slot_gradient_changed(self, *args, **kwargs):
        if self.colormap != self.histogram.gradient.colorMap():
            self.colormap = self.histogram.gradient.colorMap()
            self.setData(self.input_x_data, self.input_y_data, heatmap=self.heatmap)

    def slot_levels_changed(self, *args, **kwargs):
        if not self.drawing:
            self.setData(self.input_x_data, self.input_y_data, heatmap=self.heatmap)

    def paint(self, p: QtGui.QPainter, *args: Any) -> None:
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self) -> QtCore.QRect:
        return QtCore.QRectF(self.picture.boundingRect())

    def setData(self, x_data: List[str], y_data: List[str], **kwargs: Dict) -> None:
        if "heatmap" not in kwargs:
            raise Exception("Heatmap attribute must be set")

        self.drawing = True
        x_data_len, y_data_len = len(x_data), len(y_data)
        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        if self.counts_pen:
            p.setPen(self.counts_pen)
        self.heatmap = np.array(kwargs["heatmap"])

        try:
            map_min, map_max = np.min(self.heatmap), np.max(self.heatmap)
        except ValueError:
            return

        if self.x_data:
            levels = self.histogram.getLevels()
        else:
            levels = [map_min, map_max]
        normalized_heatmap = (self.heatmap - levels[0]) / (levels[1] - levels[0])
        colors = self.colormap.map([normalized_heatmap])[0]

        self.x_data = list(range(x_data_len + 1))
        self.y_data = list(range(y_data_len + 1))
        self.input_x_data = x_data
        self.input_y_data = y_data

        p.save()
        img_data = [[colors[x][y] for y in range(y_data_len)] for x in range(x_data_len)]
        cc = np.array(img_data)[:-1]
        img = QtGui.QImage(cc, x_data_len, y_data_len, QtGui.QImage.Format.Format_RGBA8888)
        p.scale(1, -1)
        p.translate(0, -y_data_len)
        p.drawImage(QtCore.QPoint(0, 0), img)

        if self.grid_pen is not None:
            p.setPen(self.grid_pen)
            for ix, x in enumerate(x_data):
                p.drawLine(ix, 0, ix, y_data_len)
            p.drawLine(ix + 1, 0, ix + 1, y_data_len)
            for iy, y in enumerate(y_data):
                p.drawLine(0, iy, x_data_len, iy)
            p.drawLine(0, iy + 1, x_data_len, iy + 1)
        p.restore()

        if self.counts_pen is not None:
            matrix = p.transform()
            p.scale(1, -1)
            p.translate(0, -y_data_len)
            str_size = p.fontMetrics().boundingRect(str(map_max))
            mapped_size = matrix.map(QtCore.QPointF(str_size.width() * 1.3, str_size.height()))
            if str_size.width() > str_size.height():
                side_size = mapped_size.x()
            else:
                side_size = mapped_size.y()
            scale = 1 / side_size
            p.scale(scale, scale)
            # Y string offset
            y_offset = (side_size - mapped_size.y()) / 2
            for ix, x in enumerate(x_data):
                px = ix / scale
                for iy, y in enumerate(y_data):
                    st, stz = self.get_static_text(self.heatmap[iy][ix])
                    x_offset = (side_size - stz.width()) / 2
                    py = iy / scale
                    p.drawStaticText(px + x_offset, py + y_offset, st)
        p.end()
        self.prepareGeometryChange()
        self.informViewBoundsChanged()
        self.bounds = [None, None]
        self.sigPlotChanged.emit(self)

        # Set histogram
        self.image_item = pg.ImageItem(self.heatmap)
        self.histogram.setImageItem(self.image_item)
        self.histogram.setLevels(*levels)
        self.drawing = False

    @cache
    def get_static_text(self, text):
        st = QtGui.QStaticText(str(text))
        return st, st.size()

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
