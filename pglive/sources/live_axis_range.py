from copy import copy
from typing import Optional, List


class LiveAxisRange:

    def __init__(self, roll_on_tick=1, offset_left=0, offset_right=0, offset_top=0, offset_bottom=0,
                 fixed_range: Optional[List[float]] = None):
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
        self.x_range = {}
        self.y_range = {}
        self.final_x_range = [0, 0]
        self.final_y_range = [0, 0]

    def get_x_range(self, data_connector, tick):
        axis_range = data_connector.plot.data_bounds(ax=0, offset=self.roll_on_tick if self.roll_on_tick > 1 else 0)
        x, _ = data_connector.plot.getData()
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
        for x_range in self.x_range.values():
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

    def get_y_range(self, data_connector, tick):
        axis_range = data_connector.plot.data_bounds(ax=1, offset=self.roll_on_tick if self.roll_on_tick > 1 else 0)
        _, y = data_connector.plot.getData()
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
        self.y_range[data_connector.__hash__()] = final_range
        for y_range in self.y_range.values():
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

    def _get_range(self, axis_range, tick, offsets):
        if self.fixed_range is not None:
            return self.fixed_range
        elif self.roll_on_tick == 1:
            return [axis_range[0], axis_range[1]]
        elif tick % self.roll_on_tick == 0 or tick < 2:
            range_width = abs(axis_range[1] - axis_range[0])
            if tick < 2:
                range_width = range_width * (self.roll_on_tick - (tick + 1))
                return [axis_range[1], axis_range[1] + range_width]
            else:
                return [axis_range[1] - range_width * offsets[0], (axis_range[1] + range_width) + (
                        range_width * offsets[1])]

    def reset(self, data_connector):
        """Reset ranges"""
        if data_connector.__hash__() in self.x_range:
            del self.x_range[data_connector.__hash__()]
        if data_connector.__hash__() in self.y_range:
            del self.y_range[data_connector.__hash__()]
        self.final_x_range = [0, 0]
        self.final_y_range = [0, 0]
