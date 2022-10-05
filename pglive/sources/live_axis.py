import datetime
from math import floor
from typing import Any, Optional, List

import pyqtgraph as pg
from pyqtgraph import debug as debug, mkPen, getConfigOption
from pyqtgraph.Qt import QtGui

from pglive.kwargs import Axis
from pglive.sources.utils import get_scaled_time_duration


class LiveAxis(pg.AxisItem):
    """Implements live axis"""

    def __init__(self, orientation, pen=None, textPen=None, axisPen=None, linkView=None, parent=None, maxTickLength=-5,
                 showValues=True, text='', units='', unitPrefix='', **kwargs: Any) -> None:
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
        self.tick_format = kwargs.get(Axis.TICK_FORMAT, None)
        self.categories = kwargs.get(Axis.CATEGORIES, [])
        self.df_short = kwargs.get(Axis.DURATION_FORMAT, Axis.DF_SHORT) == Axis.DF_SHORT
        if self.tick_format == Axis.CATEGORY:
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

    def tickStrings(self, values: list, scale: float, spacing: float) -> list:
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
        bounding = self.boundingRect().toAlignedRect()
        p.setClipRect(bounding)
        for rect, flags, text in textSpecs:
            p.drawText(rect, int(flags), text)

        profiler('draw text')
