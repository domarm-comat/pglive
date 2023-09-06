import datetime
from math import floor
from typing import Any, Optional, List

import pyqtgraph as pg  # type: ignore
from pyqtgraph import debug as debug, mkPen, getConfigOption  # type: ignore
from pyqtgraph.Qt import QtGui, QtCore  # type: ignore

from pglive.kwargs import Axis
from pglive.sources.utils import get_scaled_time_duration


class LiveAxis(pg.AxisItem):
    """Implements live axis"""

    def __init__(self, orientation, pen=None, textPen=None, axisPen=None, linkView=None, parent=None, maxTickLength=-5,
                 showValues=True, text='', units='', unitPrefix='', tick_angle: float = 0, **kwargs: Any) -> None:
        self.tick_position_indexes: Optional[List] = None
        super().__init__(orientation, pen=pen, textPen=textPen, linkView=linkView, parent=parent,
                         maxTickLength=maxTickLength, showValues=showValues, text=text, units=units,
                         unitPrefix=unitPrefix, **kwargs)
        # Fixing pyqtgraph bug, not setting textPen properly
        if textPen is None:
            self.setTextPen()
        else:
            self.setTextPen(textPen)
        # Set axisPen
        if axisPen is None:
            self.setAxisPen()
        else:
            self.setAxisPen(axisPen)
        # Tick format
        if tick_angle < 0:
            tick_angle += 360
        self.tick_angle = tick_angle % 360
        self.tick_format = kwargs.get(Axis.TICK_FORMAT, None)
        self.categories = kwargs.get(Axis.CATEGORIES, [])
        self.df_short = kwargs.get(Axis.DURATION_FORMAT, Axis.DF_SHORT) == Axis.DF_SHORT
        if self.tick_format == Axis.CATEGORY and kwargs.get(Axis.SHOW_ALL_CATEGORIES, True):
            # Override ticks spacing and set spacing 1 with step 1
            self.setTickSpacing(1, 1)

    def axisPen(self) -> QtGui.QPen:
        """Get axis pen"""
        if self._axisPen is None:
            return mkPen(getConfigOption('foreground'))
        return mkPen(self._axisPen)

    def setAxisPen(self, *args: Any, **kwargs: Any) -> None:
        """
        Set axis pen used for drawing axis line.
        If no arguments are given, the default foreground color will be used.
        """
        self.picture = None
        if args or kwargs:
            self._axisPen = mkPen(*args, **kwargs)
        else:
            self._axisPen = mkPen(getConfigOption('foreground'))
        self._updateLabel()

    def tickStrings(self, values: List, scale: float, spacing: float) -> List:
        """Convert ticks into final strings"""
        if self.tick_position_indexes:
            try:
                values = [self.tick_position_indexes[int(value - 1)] for value in values]
            except IndexError:
                pass
        if self.tick_format == Axis.DATETIME:
            # Convert tick to Datetime
            tick_strings = [datetime.datetime.fromtimestamp(value).strftime("%Y-%m-%d %H:%M:%S") for value in values]
        elif self.tick_format == Axis.TIME:
            # Convert tick to Time
            tick_strings = [datetime.datetime.fromtimestamp(value).strftime("%H:%M:%S") for value in values]
        elif self.tick_format == Axis.DURATION:
            # Convert tick to Time duration
            tick_strings = [get_scaled_time_duration(value, short=self.df_short) for value in values]
        elif self.tick_format == Axis.CATEGORY:
            # Convert tick to Category name
            tick_strings = []
            for value in values:
                try:
                    value += 0.5
                    tick_strings.append(self.categories[int(value)] if floor(value) >= 0 else "")
                except IndexError:
                    tick_strings.append("")
        else:
            # No specific format
            tick_strings = super().tickStrings(values, scale, spacing)
        return tick_strings

    def drawPicture(self, p, axisSpec, tickSpecs, textSpecs) -> None:
        profiler = debug.Profiler()

        p.setRenderHint(p.RenderHint.Antialiasing, False)
        p.setRenderHint(p.RenderHint.TextAntialiasing, True)

        # draw long line along axis
        pen, p1, p2 = axisSpec
        # Use axis pen to draw axis line
        p.setPen(self.axisPen())
        p.drawLine(p1, p2)
        # Switch back to normal pen
        p.setPen(pen)
        # p.translate(0.5,0)  ## resolves some damn pixel ambiguity

        # draw ticks
        for pen, p1, p2 in tickSpecs:
            p.setPen(pen)
            p.drawLine(p1, p2)
        profiler('draw ticks')
        # Draw all text
        if self.style['tickFont'] is not None:
            p.setFont(self.style['tickFont'])
        p.setPen(self.textPen())
        min_height = p.fontMetrics().height()
        bounding = self.boundingRect().toAlignedRect()
        p.setClipRect(bounding)
        if self.tick_angle == 0:
            for rect, flags, text in textSpecs:
                p.drawText(rect, int(flags), text)
            if self.label.isVisible():
                min_height += self.label.boundingRect().height() * 0.8
            self.fixedHeight = min_height + 7
        else:
            if self.orientation in ("bottom", "top"):
                max_height = min_height
                offset_top = 0
                if self.label.isVisible():
                    offset_top = self.label.boundingRect().height() * 0.8

                for rect, flags, text in textSpecs:
                    p.save()
                    if self.orientation == "bottom":
                        if 0 < self.tick_angle <= 180:
                            rect.moveTopLeft(QtCore.QPointF(rect.center().x(), rect.topLeft().y()))
                            rot_point = QtCore.QPointF(rect.topLeft().x(), rect.center().y())
                        else:
                            rect.moveTopRight(QtCore.QPointF(rect.center().x(), rect.topRight().y()))
                            rot_point = QtCore.QPointF(rect.topRight().x(), rect.center().y())
                    else:
                        if 0 < self.tick_angle <= 180:
                            rect.moveTopLeft(QtCore.QPointF(rect.center().x(), offset_top))
                            rot_point = QtCore.QPointF(rect.topLeft().x(), rect.center().y())
                        else:
                            rect.moveBottomLeft(QtCore.QPointF(rect.center().x(), rect.bottomLeft().y()))
                            rot_point = QtCore.QPointF(rect.bottomLeft().x(), rect.center().y())

                    p.translate(rot_point)
                    p.rotate(self.tick_angle)
                    p.translate(-rot_point)
                    scene_rect = p.transform().mapRect(rect)
                    if scene_rect.height() > max_height:
                        max_height = scene_rect.height()
                    if scene_rect.width() > max_height:
                        max_height = scene_rect.width()
                    p.drawText(rect, int(flags), text)
                    # restoring the painter is *required*!!!
                    p.restore()

                self.fixedHeight = offset_top + max_height + 10
            else:
                for rect, flags, text in textSpecs:
                    p.save()
                    p.translate(rect.center())
                    p.rotate(self.tick_angle)
                    p.translate(-rect.center())
                    p.drawText(rect, int(flags), text)
                    # restoring the painter is *required*!!!
                    p.restore()
        profiler('draw text')
