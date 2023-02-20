from typing import Union, Optional, Protocol, Dict

import pyqtgraph as pg  # type: ignore
from pyqtgraph.Qt import QtGui, QtCore  # type: ignore

from pglive.kwargs import LeadingLine
from pglive.sources.live_plot_widget import LivePlotWidget
from pglive.sources.utils import NUM_LIST


class SupportsLivePlot(Protocol):
    plot_widget: Optional[LivePlotWidget]
    sigPlotChanged: QtCore.Signal
    opts: Dict

    def setData(self, x: NUM_LIST, y: NUM_LIST, kwargs: dict) -> None: ...

    def getViewBox(self) -> pg.ViewBox: ...


class MixinLivePlot(SupportsLivePlot):
    """Implements new_data slot for any plot"""
    plot_widget: Optional[LivePlotWidget] = None
    min_x, min_y, max_x, max_y = 0, 0, 0, 0

    def slot_new_data(self, y: NUM_LIST, x: NUM_LIST, kwargs) -> None:
        self.setData(x, y, **kwargs)

    def slot_connector_toggle(self, data_connector, flag: bool):
        if self.plot_widget is not None:
            self.plot_widget.slot_connector_toggle(data_connector, flag)
        else:
            raise Exception("Plot must be added into LivePlotWidget before setting any data.")

    def slot_roll_tick(self, data_connector, tick: int) -> None:
        if self.plot_widget is not None:
            self.plot_widget.slot_roll_tick(data_connector, tick)
        else:
            raise Exception("Plot must be added into LivePlotWidget before setting any data.")


class MixinLiveBarPlot(SupportsLivePlot):
    """Implements new_data slot for Bar Plot"""
    plot_widget: Optional[LivePlotWidget] = None
    sigPlotChanged = QtCore.Signal()

    def slot_new_data(self, y: NUM_LIST, x: NUM_LIST, kwargs) -> None:
        self.setData(x, y, kwargs)

    def slot_connector_toggle(self, data_connector, flag: bool):
        if self.plot_widget is not None:
            self.plot_widget.slot_connector_toggle(data_connector, flag)
        else:
            raise Exception("Plot must be added into LivePlotWidget before setting any data.")

    def slot_roll_tick(self, data_connector, tick: int) -> None:
        if self.plot_widget is not None:
            self.plot_widget.slot_roll_tick(data_connector, tick)
        else:
            raise Exception("Plot must be added into LivePlotWidget before setting any data.")


class MixinLeadingLine(SupportsLivePlot):
    """Implements leading line"""
    _hl_kwargs = None
    _vl_kwargs = None

    def set_leading_line(self, orientation: str = LeadingLine.VERTICAL,
                         pen: QtGui.QPen = None, text_axis: str = LeadingLine.AXIS_X, **kwargs) -> Dict:
        text_axis = text_axis.lower()
        assert text_axis in (LeadingLine.AXIS_X, LeadingLine.AXIS_Y)

        self.sigPlotChanged.connect(self.update_leading_line)

        if pen is None:
            pen = self.opts.get("pen")
        if orientation == LeadingLine.VERTICAL:
            _v_leading_line = pg.InfiniteLine(angle=90, movable=False, pen=pen)
            _v_leading_text = pg.TextItem(color="black", angle=-90, fill=pen.color())
            _v_leading_line.setZValue(999)
            _v_leading_text.setZValue(999)
            self._vl_kwargs = {"line": _v_leading_line, "text": _v_leading_text, "pen": pen, "text_axis": text_axis,
                               **kwargs}
            return self._vl_kwargs
        elif orientation == LeadingLine.HORIZONTAL:
            _h_leading_line = pg.InfiniteLine(angle=0, movable=False, pen=pen)
            _h_leading_text = pg.TextItem(color="black", fill=pen.color())
            _h_leading_text.setZValue(999)
            _h_leading_text.setZValue(999)
            self._hl_kwargs = {"line": _h_leading_line, "text": _h_leading_text, "pen": pen, "text_axis": text_axis,
                               **kwargs}
            return self._hl_kwargs
        else:
            raise TypeError("Unsupported LeadingLine type")

    def update_leading_line(self):
        raise NotImplementedError

    def x_format(self, value: Union[int, float]) -> str:
        """X tick format (will be overwritten when inserted in LivePlotWidget)"""
        return str(round(value, 4))

    def y_format(self, value: Union[int, float]) -> str:
        """Y tick format (will be overwritten when inserted in LivePlotWidget)"""
        return str(round(value, 4))

    def update_leading_text(self, x: float, y: float, x_text: Optional[str] = None,
                            y_text: Optional[str] = None) -> None:
        """Update position and text of Vertical and Horizontal leading text"""
        vb = self.getViewBox()
        width, height = vb.width(), vb.height()
        if x_text is None:
            x_text = self.x_format(x)
        if y_text is None:
            y_text = self.y_format(y)

        if self._vl_kwargs is not None:
            text_axis = x_text if self._vl_kwargs["text_axis"] == LeadingLine.AXIS_X else y_text
            self._vl_kwargs["text"].setText(text_axis)
            pixel_pos = vb.mapViewToScene(QtCore.QPointF(x, y))
            y_pos = 0 + self._vl_kwargs["text"].boundingRect().height() + 10
            new_pos = vb.mapSceneToView(QtCore.QPointF(pixel_pos.x(), y_pos))
            self._vl_kwargs["text"].setPos(new_pos.x(), new_pos.y())

        if self._hl_kwargs is not None:
            text_axis = x_text if self._hl_kwargs["text_axis"] == LeadingLine.AXIS_X else y_text
            self._hl_kwargs["text"].setText(text_axis)
            pixel_pos = vb.mapViewToScene(QtCore.QPointF(x, y))
            x_pos = width - self._hl_kwargs["text"].boundingRect().width() + 21
            new_pos = vb.mapSceneToView(QtCore.QPointF(x_pos, pixel_pos.y()))
            self._hl_kwargs["text"].setPos(new_pos.x(), new_pos.y())
