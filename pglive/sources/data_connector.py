import time
from collections import deque
from math import inf
from threading import Lock
from typing import List, Union

from pyqtgraph.Qt import QT_LIB, PYQT6

if QT_LIB == PYQT6:
    from PyQt6.QtCore import QObject, pyqtSignal
else:
    from PyQt5.QtCore import QObject, pyqtSignal

from pglive.sources.live_plot import MixinLivePlot, MixinLiveBarPlot, make_live


class DataConnector(QObject):
    sig_new_data = pyqtSignal(object, object, dict)
    sig_paused = pyqtSignal()
    sig_resumed = pyqtSignal()
    paused = False
    # Last update time, using perf_counter for most precise counter
    last_update = time.perf_counter()

    def __init__(self, plot: Union[MixinLivePlot, MixinLiveBarPlot], max_points=inf, update_rate=inf) -> None:
        """
        DataConnector is connecting plot with data and makes sure, that all updates are thread-safe.
        To make plot compatible and work with Connector, it must implement slot_new_data method.
        This can be achieved either by inheriting from LiveMixin or LiveMixinBarPlot class or DataConnector, tries to
        use make_live function and add slot in runtime.
        :param plot: Plot to be connected with Data
        :param max_points: Maximum amount of data points to plot
        :param float update_rate: Update rate in Hz
        """
        super().__init__()
        if not isinstance(plot, (MixinLivePlot, MixinLiveBarPlot)):
            # Attempt to convert plot into live if it's not already
            make_live(plot)
        # Data update lock, ensuring thread-safety
        self.data_lock = Lock()
        # Maximum number of points to plot
        self.max_points = max_points
        # Calculating update timeout from update_rate frequency
        self.update_timeout = 1 / update_rate
        if self.max_points == inf:
            # Use simple list if there is no point limits
            self.x, self.y = [], []
        else:
            # Use deque with maxlen otherwise
            self.x, self.y = deque(maxlen=self.max_points), deque(maxlen=self.max_points)
        # Set plot and connect sig_new_data with plot.slot_new_data
        self.plot = plot
        self.sig_new_data.connect(self.plot.slot_new_data)

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
        """Skip update"""
        return self.paused or (time.perf_counter() - self.last_update) < self.update_timeout or self.data_lock.locked()

    def _update_data(self, **kwargs):
        """Update data and last update time"""
        # Notify all connected plots
        self.sig_new_data.emit(self.y, self.x, kwargs)
        self.last_update = time.perf_counter()

    def cb_set_data(self, y: List[Union[int, float]], x: List[Union[int, float]] = None, **kwargs) -> None:
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
            self._update_data(**kwargs)

    def cb_append_data_point(self, y: Union[int, float], x: Union[int, float] = None, **kwargs) -> None:
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
            self._update_data(**kwargs)
