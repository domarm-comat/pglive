import time
import warnings
from collections import deque
from math import inf
from threading import Lock
from typing import List, Union

import numpy as np
from pyqtgraph.Qt import QtCore

from pglive.sources.live_plot import MixinLivePlot, MixinLiveBarPlot, make_live

warnings.filterwarnings("ignore", category=np.VisibleDeprecationWarning)


class DataConnector(QtCore.QObject):
    sig_new_data = QtCore.Signal(object, object, dict)
    sig_data_roll_tick = QtCore.Signal(object, int)
    sig_data_reset = QtCore.Signal(object)
    sig_paused = QtCore.Signal()
    sig_resumed = QtCore.Signal()
    paused = False
    # Last update time, using perf_counter for most precise counter
    last_update = 0
    last_plot = 0

    def __init__(self, plot: Union[MixinLivePlot, MixinLiveBarPlot], max_points: float = inf, update_rate: float = inf,
                 plot_rate: float = inf, ignore_auto_range: bool = False) -> None:
        """
        DataConnector is connecting plot with data and makes sure, that all updates are thread-safe.
        To make plot compatible and work with Connector, it must implement slot_new_data method.
        This can be achieved either by inheriting from LiveMixin or LiveMixinBarPlot class or DataConnector, tries to
        use make_live function and add slot in runtime.
        Use ignore_auto_range if you have more than one plot to calculate range for only one main plot.
        This can also improve performance for multiple plots inside one widget.
        :param plot: Plot to be connected with Data
        :param max_points: Maximum amount of data points to plot
        :param float update_rate: Update rate in Hz
        :param float plot_rate: Plot rate in Hz
        :param bool ignore_auto_range: If set to True auto range is not calculated when new data is acquired
        """
        super().__init__()
        self.rolling_index = 0
        self.ignore_auto_range = ignore_auto_range

        if not isinstance(plot, (MixinLivePlot, MixinLiveBarPlot)):
            # Attempt to convert plot into live if it's not already
            make_live(plot)
        # Data update lock, ensuring thread-safety
        self.data_lock = Lock()
        # Maximum number of points to plot
        self.max_points = max_points
        # Calculating update timeout from update_rate frequency
        self.update_timeout = 1 / update_rate
        self.plot_timeout = 1 / plot_rate
        self.tick_position_indexes = None
        self.plot = plot
        # Set plot and connect sig_new_data with plot.slot_new_data
        self.sig_new_data.connect(self.plot.slot_new_data)
        self.sig_data_reset.connect(self.plot.slot_connector_reset)
        self.sig_data_roll_tick.connect(self.plot.slot_roll_tick)
        if self.max_points == inf:
            # Use simple list if there is no point limits
            self.x, self.y = [], []
        else:
            # Use deque with maxlen otherwise
            self.x, self.y = deque(maxlen=self.max_points), deque(maxlen=self.max_points)

    @property
    def max_points(self):
        return self._max_len

    @max_points.setter
    def max_points(self, new_max_len: Union[int, float]) -> None:
        assert new_max_len > 0
        self._max_len = new_max_len

    def pause(self) -> None:
        """Pause data plotting"""
        self.paused = True
        self.sig_paused.emit()

    def resume(self) -> None:
        """Resume data plotting"""
        self.paused = False
        self.sig_resumed.emit()

    def _skip_update(self) -> bool:
        """Skip data update"""
        return self.paused or (time.perf_counter() - self.last_update) < self.update_timeout or self.data_lock.locked()

    def _skip_plot(self) -> bool:
        """Skip data plot"""
        return self.paused or (time.perf_counter() - self.last_plot) < self.plot_timeout

    def _update_data(self, **kwargs):
        """Update data and last update time"""
        # Notify all connected plots
        self.sig_new_data.emit(np.asarray(self.y), np.asarray(self.x), kwargs)
        self.last_plot = time.perf_counter()

    def cb_set_data(self, y: List[Union[int, float, List]], x: List[Union[int, float]] = None, **kwargs) -> None:
        """Replace current data"""
        if self._skip_update():
            return

        with self.data_lock:
            if self.max_points == inf:
                self.y = y
            else:
                self.y = deque(y, maxlen=self.max_points)
            if x is not None:
                if self.max_points == inf:
                    self.x = x
                else:
                    self.x = deque(x, maxlen=self.max_points)
            else:
                self.x = range(len(self.y))

            self.last_update = time.perf_counter()

            if not self._skip_plot():
                self._update_data(**kwargs)
                self.sig_data_reset.emit(self)
                self.sig_data_roll_tick.emit(self, len(self.x) - 1)
                self.rolling_index = len(self.x)

    def cb_append_data_point(self, y: Union[int, float, List], x: Union[int, float] = None, **kwargs) -> None:
        """Append new data point"""
        if self._skip_update():
            return

        with self.data_lock:
            self.y.append(y)
            if x is not None:
                self.x.append(x)
            elif len(self.x) == 0:
                self.x.append(0)
            else:
                self.x.append(self.x[-1] + 1)
            if self.tick_position_indexes is not None:
                if len(self.tick_position_indexes) == 0:
                    self.tick_position_indexes.append(0.0)
                elif len(self.tick_position_indexes) == self.tick_position_indexes.maxlen:
                    self.tick_position_indexes.rotate(-1)
                else:
                    self.tick_position_indexes.append(self.tick_position_indexes[-1] + 1.0)
            self.last_update = time.perf_counter()

            if not self._skip_plot():
                self._update_data(**kwargs)
                self.sig_data_roll_tick.emit(self, self.rolling_index)
                self.rolling_index += 1
