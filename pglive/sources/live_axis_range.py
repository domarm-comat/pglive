import numbers
import time
from copy import copy
from typing import Optional, List, Tuple, Dict


class LiveAxisRange:
    def __init__(
        self,
        roll_on_tick: int = 1,
        offset_left: float = 0.0,
        offset_right: float = 0.0,
        offset_top: float = 0.0,
        offset_bottom: float = 0.0,
        fixed_range: Optional[List[float]] = None,
    ) -> None:
        self.roll_on_tick = roll_on_tick
        self.offset_left = offset_left
        self.offset_right = offset_right
        self.offset_top = offset_top
        self.offset_bottom = offset_bottom
        self.crop_left_offset_to_data = False
        self.crop_right_offset_to_data = False
        self.crop_top_offset_to_data = False
        self.crop_bottom_offset_to_data = False
        self.fixed_range = fixed_range
        self.x_range: Dict[str, List[float]] = {}
        self.y_range: Dict[str, List[float]] = {}
        self.final_x_range = [0.0, 0.0]
        self.final_y_range = [0.0, 0.0]
        self.ignored_data_connectors: List[str] = []

    def get_x_range(self, data_connector, tick: int) -> List[float]:
        x, _ = data_connector.plot.getData()
        if x is None:
            return [0.0]
        if tick == 0:
            if isinstance(x[0], numbers.Number):
                axis_range = [x[0], x[0]]
            else:
                axis_range = [0, data_connector.plot.data_tick(ax=0)]
        elif tick == 1:
            if isinstance(x[0], numbers.Number):
                axis_range = [x[0], x[1]]
            else:
                axis_range = [0, data_connector.plot.data_tick(ax=0) * 2]
        else:
            axis_range = data_connector.plot.data_bounds(ax=0, offset=self.roll_on_tick if self.roll_on_tick > 1 else 0)
        final_range = self._get_range(axis_range, tick, (self.offset_left, self.offset_right))
        if final_range is None:
            return self.final_x_range
        offset_x = data_connector.plot.pos().x()
        final_range[0] += offset_x
        final_range[1] += offset_x
        # Check left and right offset and crop to data if flag is set
        if self.crop_left_offset_to_data and final_range[0] < x[0]:
            final_range[0] = x[0]
        if self.crop_right_offset_to_data and final_range[1] > x[-1]:
            final_range[1] = x[-1]
        self.x_range[data_connector.__hash__()] = copy(final_range)
        for connector_id, x_range in self.x_range.items():
            if connector_id in self.ignored_data_connectors:
                continue
            if final_range[0] > x_range[0]:
                final_range[0] = x_range[0]
            if final_range[1] < x_range[1]:
                final_range[1] = x_range[1]
        if final_range[0] == final_range[1]:
            # Pyqtgraph ViewBox.setRange doesn't like same value for min and max,
            # therefore in that case we must set some range
            final_range[0] -= 0.4
            final_range[1] += 0.4
        if self.final_x_range != final_range:
            self.final_x_range = final_range
        return self.final_x_range

    def recalculate_x_range(self):
        final_range = None
        for connector_id, x_range in self.x_range.items():
            if connector_id in self.ignored_data_connectors:
                continue
            elif final_range is None:
                final_range = copy(x_range)
                continue
            if final_range[0] > x_range[0]:
                final_range[0] = x_range[0]
            if final_range[1] < x_range[1]:
                final_range[1] = x_range[1]
        if final_range is None:
            final_range = [0, 0]
        if final_range[0] == final_range[1]:
            # Pyqtgraph ViewBox.setRange doesn't like same value for min and max,
            # therefore in that case we must set some range
            final_range[0] -= 0.4
            final_range[1] += 0.4
        if self.final_x_range != final_range:
            self.final_x_range = final_range
        return self.final_x_range

    def get_y_range(self, data_connector, tick: int) -> List[float]:
        _, y = data_connector.plot.getData()
        if y is None:
            return [0.0]
        if tick == 0:
            if isinstance(y[0], numbers.Number):
                axis_range = [y[0], y[0]]
            else:
                axis_range = [0, data_connector.plot.data_tick(ax=1)]
        elif tick == 1:
            if isinstance(y[0], numbers.Number):
                axis_range = [y[0], y[1]]
            else:
                axis_range = [0, data_connector.plot.data_tick(ax=1) * 2]
        else:
            axis_range = data_connector.plot.data_bounds(ax=1, offset=self.roll_on_tick if self.roll_on_tick > 1 else 0)
        final_range = self._get_range(axis_range, tick, (self.offset_bottom, self.offset_top))
        if final_range is None:
            return self.final_y_range
        offset_y = data_connector.plot.pos().y()
        final_range[0] += offset_y
        final_range[1] += offset_y
        # Check left and right offset and crop to data if flag is set
        if self.crop_bottom_offset_to_data and final_range[0] < y[0]:
            final_range[0] = y[0]
        if self.crop_top_offset_to_data and final_range[1] > y[-1]:
            final_range[1] = y[-1]
        self.y_range[data_connector.__hash__()] = copy(final_range)
        for connector_id, y_range in self.y_range.items():
            if connector_id in self.ignored_data_connectors:
                continue
            if final_range[0] > y_range[0]:
                final_range[0] = y_range[0]
            if final_range[1] < y_range[1]:
                final_range[1] = y_range[1]
        if final_range[0] == final_range[1]:
            # Pyqtgraph ViewBox.setRange doesn't like same value for min and max,
            # therefore in that case we must set some range
            final_range[0] -= 0.4
            final_range[1] += 0.4
        if self.final_y_range != final_range:
            self.final_y_range = final_range
        return self.final_y_range

    def recalculate_y_range(self):
        final_range = None
        for connector_id, y_range in self.y_range.items():
            if connector_id in self.ignored_data_connectors:
                continue
            elif final_range is None:
                final_range = copy(y_range)
                continue
            if final_range[0] > y_range[0]:
                final_range[0] = y_range[0]
            if final_range[1] < y_range[1]:
                final_range[1] = y_range[1]
        if final_range is None:
            final_range = [0, 0]
        if final_range[0] == final_range[1]:
            # Pyqtgraph ViewBox.setRange doesn't like same value for min and max,
            # therefore in that case we must set some range
            final_range[0] -= 0.4
            final_range[1] += 0.4
        if self.final_y_range != final_range:
            self.final_y_range = final_range
        return self.final_y_range

    def _get_range(
        self, axis_range: Tuple[float, float], tick: int, offsets: Tuple[float, float]
    ) -> Optional[List[float]]:
        if self.fixed_range is not None:
            # Return fixed defined range
            return self.fixed_range
        elif self.roll_on_tick == 1:
            # Rolling on every tick
            if offsets[0] + offsets[1] == 0:
                # Return full range if there are no offsets
                return [axis_range[0], axis_range[1]]
            elif tick > 0:
                # Return range of width specified by offsets
                range_width = (abs(axis_range[1] - axis_range[0])) / tick
                return [
                    axis_range[1] - range_width * offsets[0],
                    (axis_range[1] + range_width) + (range_width * offsets[1]),
                ]
            else:
                # Just return axis ranges subtracted by offsets
                return [axis_range[0] - offsets[0], axis_range[1] + offsets[1]]
        elif tick % self.roll_on_tick == 0 or tick < 2:
            # Rolling when tick % self.roll_on_tick == 0
            range_width = abs(axis_range[1] - axis_range[0])
            if tick < 2:
                range_width = range_width * (self.roll_on_tick - (tick + 1))
                return [axis_range[1], axis_range[1] + range_width]
            else:
                return [
                    axis_range[1] - range_width * offsets[0],
                    (axis_range[1] + range_width) + (range_width * offsets[1]),
                ]
        else:
            return None

    def ignore_connector(self, data_connector, flag: bool) -> None:
        if not flag:
            self.ignored_data_connectors.append(data_connector.__hash__())
        else:
            self.ignored_data_connectors.remove(data_connector.__hash__())
        try:
            self.get_x_range(data_connector, data_connector.rolling_index)
        except TypeError:
            return None
        try:
            self.get_y_range(data_connector, data_connector.rolling_index)
        except TypeError:
            return None

    def remove_data_connector(self, data_connector):
        if data_connector.__hash__() in self.ignored_data_connectors:
            del self.ignored_data_connectors[data_connector.__hash__()]
        if data_connector.__hash__() in self.y_range:
            del self.y_range[data_connector.__hash__()]
        if data_connector.__hash__() in self.x_range:
            del self.x_range[data_connector.__hash__()]
