from typing import List, Tuple, Optional, Dict

import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

from pglive.sources.live_mixins import MixinLivePlot, MixinLeadingLine


class LiveCategorizedBarPlot(pg.GraphicsObject, MixinLivePlot, MixinLeadingLine):
    """Live categorized bar plot, plotting data [[category1, category2, ...], ...]"""
    sigPlotChanged = QtCore.Signal(object)

    def __init__(self, categories: Optional[List[str]] = None, category_color: Optional[Dict[str, str]] = None,
                 bar_height: float = 0.9) -> None:
        pg.GraphicsObject.__init__(self)
        self.x_data = []
        self.y_data = []
        self.bar_height = bar_height
        self.output_y_data = []
        self.outline_pen = pg.mkPen("w")
        self.bar_brush = pg.mkBrush("g")
        self.categories = categories if categories is not None else []
        self.category_color = {category: pg.mkBrush(color) for category, color in
                               category_color.items()} if category_color is not None else {}
        self.picture = QtGui.QPicture()

    @property
    def bar_height(self) -> float:
        return self._bar_height

    @bar_height.setter
    def bar_height(self, new_bar_height: float) -> None:
        assert 0 <= new_bar_height <= 1
        self._bar_height = new_bar_height

    def paint(self, p, *args) -> None:
        p.drawPicture(0, 0, self.picture)

    def boundingRect(self) -> QtCore.QRect:
        return QtCore.QRectF(self.picture.boundingRect())

    def setData(self, x_data: List[float], y_data: List[Tuple[str]]) -> None:
        """y_data must be in format [[category1, category2, ...], ...]"""
        self.x_data = x_data
        self.y_data = y_data
        self.output_y_data = []
        if len(x_data) != len(y_data):
            raise Exception("Len of x_data must be the same as y_data")

        self.picture = QtGui.QPicture()
        p = QtGui.QPainter(self.picture)
        p.setPen(self.outline_pen)

        active_categories = {}
        for index, x in enumerate(x_data):
            for category in y_data[index]:
                if category not in self.categories:
                    self.categories.append(category)
                    active_categories[category] = x
                if category not in active_categories:
                    active_categories[category] = x
            for category in tuple(active_categories.keys()):
                if category not in y_data[index]:
                    try:
                        p.setBrush(self.category_color[category])
                    except KeyError:
                        p.setBrush(self.bar_brush)
                    w = x - active_categories[category]
                    p.drawRect(
                        QtCore.QRectF(active_categories[category],
                                      self.categories.index(category) - self.bar_height / 2, w, self.bar_height))
                    del active_categories[category]
        for category in active_categories.keys():
            try:
                p.setBrush(self.category_color[category])
            except KeyError:
                p.setBrush(self.bar_brush)
            w = x - active_categories[category]
            p.drawRect(
                QtCore.QRectF(active_categories[category], self.categories.index(category) - self.bar_height / 2, w,
                              self.bar_height))

        p.end()

        self.prepareGeometryChange()
        self.informViewBoundsChanged()
        self.bounds = [None, None]
        self.sigPlotChanged.emit(self)

    def update_leading_line(self) -> None:
        """Leading line will display all four fields"""
        last_x_point = self.x_data[-1]
        last_y_point = len(self.categories) - 1
        if self._vl_kwargs is not None:
            self._vl_kwargs["line"].setPos(last_x_point)
        if self._hl_kwargs is not None:
            self._hl_kwargs["line"].setPos(last_y_point)

        y_text = ", ".join(self.y_data[-1])
        self.update_leading_text(last_x_point, last_y_point, y_text=y_text)

    def getData(self):
        return self.x_data, self.y_data

    def data_bounds(self, ax=0, offset=0) -> Tuple:
        x, y = self.x_data, range(len(self.categories))
        if ax == 0:
            sub_range = x[-offset:]
            return np.nanmin(sub_range), np.nanmax(sub_range)
        else:
            h = self.bar_height / 2
            return 0 - h, len(self.categories) - (1 - h)
