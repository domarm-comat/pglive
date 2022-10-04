from typing import Union, Optional, Any, List

import pyqtgraph as pg
from pyqtgraph import ViewBox
from pyqtgraph.Qt import QtCore
from pyqtgraph.Qt import QtGui

from pglive.kwargs import Crosshair
from pglive.sources.live_axis import LiveAxis
from pglive.sources.live_axis_range import LiveAxisRange


class LivePlotWidget(pg.PlotWidget):
    """Implements main plot widget for all live plots"""
    mouse_position: Optional[QtCore.QPointF] = None
    sig_crosshair_moved = QtCore.Signal(QtCore.QPointF)
    sig_crosshair_out = QtCore.Signal()
    sig_crosshair_in = QtCore.Signal()

    def __init__(self, parent=None, background: str = 'default', plotItem=None,
                 x_range_controller: Optional[LiveAxisRange] = None,
                 y_range_controller: Optional[LiveAxisRange] = None, **kwargs: Any) -> None:
        # Make sure we have LiveAxis in the bottom
        if "axisItems" not in kwargs:
            kwargs["axisItems"] = {"bottom": LiveAxis("bottom")}
        elif "bottom" not in kwargs["axisItems"]:
            kwargs["axisItems"]["bottom"] = LiveAxis("bottom")
        assert isinstance(kwargs["axisItems"]["bottom"], LiveAxis)
        self.x_range_controller = LiveAxisRange() if x_range_controller is None else x_range_controller
        self.y_range_controller = LiveAxisRange() if y_range_controller is None else y_range_controller
        self.manual_range = False

        super().__init__(parent=parent, background=background, plotItem=plotItem, **kwargs)
        self.crosshair_enabled = kwargs.get(Crosshair.ENABLED, False)
        self.crosshair_items = []
        self.final_x_range: List[float, float] = [self.viewRect().x(), self.viewRect().width()]
        self.final_y_range: List[float, float] = [self.viewRect().y(), self.viewRect().height()]
        self.life_ranges = {}
        self.crosshair_x_axis = kwargs.get(Crosshair.X_AXIS, "bottom")
        self.crosshair_y_axis = kwargs.get(Crosshair.Y_AXIS, "left")
        if self.crosshair_enabled:
            self._add_crosshair(kwargs.get(Crosshair.LINE_PEN, None),
                                kwargs.get(Crosshair.TEXT_KWARGS, {}))
        self.getPlotItem().autoBtn.clicked.disconnect()
        self.getPlotItem().autoBtn.clicked.connect(self.auto_btn_clicked)

        # Override addItem method
        def addItem(*args: Any) -> None:
            if hasattr(args[0], "_vl_kwargs") and args[0]._vl_kwargs is not None:
                self.plotItem.addItem(args[0]._vl_kwargs["line"], ignoreBounds=True)
                self.plotItem.addItem(args[0]._vl_kwargs["text"], ignoreBounds=True)
            if hasattr(args[0], "_hl_kwargs") and args[0]._hl_kwargs is not None:
                self.plotItem.addItem(args[0]._hl_kwargs["line"], ignoreBounds=True)
                self.plotItem.addItem(args[0]._hl_kwargs["text"], ignoreBounds=True)
            if hasattr(args[0], "update_leading_line"):
                setattr(args[0], "x_format", self.x_format)
                setattr(args[0], "y_format", self.y_format)
            self.plotItem.addItem(*args)
            args[0].plot_widget = self

        self.disableAutoRange()
        self.getPlotItem().vb.setRange = self.set_range
        self.getPlotItem().vb.sigRangeChangedManually.connect(self.sm)
        self.addItem = addItem

    def sm(self, *args, **kwargs):
        self.manual_range = True

    def _add_crosshair(self, crosshair_pen: QtGui.QPen, crosshair_text_kwargs: dict) -> None:
        """Add crosshair into plot"""
        self.vLine = pg.InfiniteLine(angle=90, movable=False, pen=crosshair_pen)
        self.hLine = pg.InfiniteLine(angle=0, movable=False, pen=crosshair_pen)
        self.x_value_label = pg.TextItem(**crosshair_text_kwargs)
        self.y_value_label = pg.TextItem(**crosshair_text_kwargs)
        # All Crosshair items
        self.crosshair_items = [self.hLine, self.vLine, self.x_value_label, self.y_value_label]
        for item in self.crosshair_items:
            # Make sure, that every crosshair item is painted on top of everything
            item.setZValue(999)
            self.addItem(item, ignoreBounds=True)
        # Hide crosshair at the beginning
        self.hide_crosshair()

    def _update_crosshair_position(self) -> None:
        """Update position of crosshair based on mouse position"""
        if self.mouse_position:
            mouse_point = self.plotItem.vb.mapSceneToView(self.mouse_position)
            # Move crosshair to mouse pointer position
            self.vLine.setPos(mouse_point.x())
            self.hLine.setPos(mouse_point.y())

            self.x_value_label.setText(f"X = {self.x_format(mouse_point.x())}")
            self.y_value_label.setText(f"Y = {self.y_format(mouse_point.y())}")

            x_pos = self.mouse_position.x() + 5
            y_pos = self.mouse_position.y() - self.x_value_label.boundingRect().height()

            # Resolve position of crosshair text to be in view of the plot
            text_height = self.x_value_label.boundingRect().height()
            if self.mouse_position.x() + self.x_value_label.boundingRect().width() > self.plotItem.width():
                x_pos = self.mouse_position.x() - 5 - self.x_value_label.boundingRect().width()
            elif self.mouse_position.x() + self.y_value_label.boundingRect().width() > self.plotItem.width():
                x_pos = self.mouse_position.x() - 5 - self.x_value_label.boundingRect().width()
            if self.mouse_position.y() - self.x_value_label.boundingRect().height() - 2 * text_height - 5 < 0:
                y_pos += text_height * 2 + 5

            # Move X marker to position
            x_marker_point = self.plotItem.vb.mapSceneToView(
                QtCore.QPointF(x_pos, y_pos - self.x_value_label.boundingRect().height()))
            self.x_value_label.setPos(x_marker_point.x(), x_marker_point.y())

            # Move Y marker to position
            y_marker_point = self.plotItem.vb.mapSceneToView(QtCore.QPointF(x_pos, y_pos))
            self.y_value_label.setPos(y_marker_point.x(), y_marker_point.y())

            # Emit crosshair moved signal
            self.sig_crosshair_moved.emit(mouse_point)

    def x_format(self, value: Union[int, float]) -> str:
        """X tick format"""
        try:
            # Get crosshair X str format from bottom tick axis format
            return self.getPlotItem().axes[self.crosshair_x_axis]["item"].tickStrings((value,), 0, 1)[0]
        except Exception:
            return str(round(value, 4))

    def y_format(self, value: Union[int, float]) -> str:
        """Y tick format"""
        try:
            # Get crosshair Y str format from left tick axis format
            return self.getPlotItem().axes[self.crosshair_y_axis]["item"].tickStrings((value,), 0, 1)[0]
        except Exception:
            return str(round(value, 4))

    def leaveEvent(self, ev: QtCore.QEvent) -> None:
        """Mouse left PlotWidget"""
        if self.crosshair_enabled:
            self.hide_crosshair()
        self.mouse_position = None
        self.sig_crosshair_out.emit()
        super().leaveEvent(ev)

    def enterEvent(self, ev: QtCore.QEvent) -> None:
        """Mouse enter PlotWidget"""
        if self.crosshair_enabled:
            self.show_crosshair()
        self.sig_crosshair_in.emit()
        super().enterEvent(ev)

    def mouseMoveEvent(self, ev: QtCore.QEvent) -> None:
        """Mouse moved in PlotWidget"""
        if pg.Qt.QT_LIB == pg.Qt.PYQT6:
            ev_pos = ev.position()
        else:
            ev_pos = ev.pos()

        if self.crosshair_enabled and self.sceneBoundingRect().contains(ev_pos):
            self.mouse_position = ev_pos
            self._update_crosshair_position()
        super().mouseMoveEvent(ev)

    def paintEvent(self, ev: QtCore.QEvent) -> None:
        """Update crosshair position when replot"""
        self._update_crosshair_position()
        return super().paintEvent(ev)

    def hide_crosshair(self) -> None:
        """Hide crosshair items"""
        for item in self.crosshair_items:
            item.hide()

    def show_crosshair(self) -> None:
        """Show crosshair items"""
        for item in self.crosshair_items:
            item.show()

    def auto_btn_clicked(self) -> None:
        """Controls auto button"""
        self.manual_range = False
        self.set_range(xRange=self.final_x_range, yRange=self.final_y_range)

    def slot_roll_tick(self, data_connector, tick: int) -> None:
        if data_connector.ignore_auto_range:
            # Don't calculate range for this DataConnector
            return
        final_x_range = self.x_range_controller.get_x_range(data_connector, tick)
        final_y_range = self.y_range_controller.get_y_range(data_connector, tick)

        if self.final_x_range != final_x_range or self.final_y_range != final_y_range:
            self.final_x_range = final_x_range
            self.final_y_range = final_y_range
            if not self.manual_range:
                self.set_range(xRange=final_x_range, yRange=final_y_range)

    def slot_connector_reset(self, data_connector):
        """Reset both range controllers when data_connector sets new data"""
        self.x_range_controller.reset(data_connector)
        self.y_range_controller.reset(data_connector)

    def set_range(self, *args, **kwargs):
        kwargs["disableAutoRange"] = True
        ViewBox.setRange(self.getPlotItem().vb, *args, **kwargs)
