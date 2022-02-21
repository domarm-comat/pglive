from typing import Union, Optional

import pyqtgraph as pg

if pg.Qt.QT_LIB == pg.Qt.PYQT6:
    from PyQt6.QtCore import QPointF, pyqtSignal, QEvent
    from PyQt6.QtGui import QPen
else:
    from PyQt5.QtCore import QPointF, pyqtSignal, QEvent
    from PyQt5.QtGui import QPen

from pglive.kwargs import Crosshair


class LivePlotWidget(pg.PlotWidget):
    """Implements main plot widget for all live plots"""
    mouse_position: Optional[QPointF] = None
    sig_crosshair_moved = pyqtSignal(QPointF)
    sig_crosshair_out = pyqtSignal()
    sig_crosshair_in = pyqtSignal()

    def __init__(self, parent=None, background='default', plotItem=None, **kwargs) -> None:
        super().__init__(parent=parent, background=background, plotItem=plotItem, **kwargs)
        self.crosshair_enabled = kwargs.get(Crosshair.ENABLED, False)
        self.crosshair_items = []
        if self.crosshair_enabled:
            self._add_crosshair(kwargs.get(Crosshair.LINE_PEN, None),
                                kwargs.get(Crosshair.TEXT_KWARGS, {}))

        # Override addItem method
        def addItem(*args):
            if hasattr(args[0], "_vl_kwargs") and args[0]._vl_kwargs is not None:
                self.plotItem.addItem(args[0]._vl_kwargs["line"], ignoreBounds=True)
                self.plotItem.addItem(args[0]._vl_kwargs["text"], ignoreBounds=True)
            if hasattr(args[0], "_hl_kwargs") and args[0]._hl_kwargs is not None:
                self.plotItem.addItem(args[0]._hl_kwargs["line"], ignoreBounds=True)
                self.plotItem.addItem(args[0]._hl_kwargs["text"], ignoreBounds=True)
            self.plotItem.addItem(*args)

        self.addItem = addItem

    def _add_crosshair(self, crosshair_pen: QPen, crosshair_text_kwargs: dict) -> None:
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
                QPointF(x_pos, y_pos - self.x_value_label.boundingRect().height()))
            self.x_value_label.setPos(x_marker_point.x(), x_marker_point.y())

            # Move Y marker to position
            y_marker_point = self.plotItem.vb.mapSceneToView(QPointF(x_pos, y_pos))
            self.y_value_label.setPos(y_marker_point.x(), y_marker_point.y())

            # Emit crosshair moved signal
            self.sig_crosshair_moved.emit(mouse_point)

    def x_format(self, value: Union[int, float]) -> str:
        """X tick format"""
        return str(round(value, 4))

    def y_format(self, value: Union[int, float]) -> str:
        """Y tick format"""
        return str(round(value, 4))

    def leaveEvent(self, ev: QEvent) -> None:
        """Mouse left PlotWidget"""
        if self.crosshair_enabled:
            self.hide_crosshair()
        self.mouse_position = None
        self.sig_crosshair_out.emit()
        super().leaveEvent(ev)

    def enterEvent(self, ev: QEvent) -> None:
        """Mouse enter PlotWidget"""
        if self.crosshair_enabled:
            self.show_crosshair()
        self.sig_crosshair_in.emit()
        super().enterEvent(ev)

    def mouseMoveEvent(self, ev: QEvent) -> None:
        """Mouse moved in PlotWidget"""
        if pg.Qt.QT_LIB == pg.Qt.PYQT6:
            ev_pos = ev.position()
        else:
            ev_pos = ev.pos()

        if self.crosshair_enabled and self.sceneBoundingRect().contains(ev_pos):
            self.mouse_position = ev_pos
            self._update_crosshair_position()
        super().mouseMoveEvent(ev)

    def paintEvent(self, ev: QEvent) -> None:
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
