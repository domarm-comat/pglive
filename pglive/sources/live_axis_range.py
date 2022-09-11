from typing import Optional, Tuple


class LiveAxisRange:

    def __init__(self, roll_on_tick=1, offset_left=0, offset_right=0, offset_top=0, offset_bottom=0,
                 fixed_range: Optional[Tuple[float, float]] = None):
        self.roll_on_tick = roll_on_tick
        self.offset_left = offset_left
        self.offset_right = offset_right
        self.offset_top = offset_top
        self.offset_bottom = offset_bottom
        self.fixed_range = fixed_range
        self.previous_x_range = None
        self.previous_y_range = None

    def get_x_range(self, axis_data, tick):
        if self.fixed_range is not None:
            self.previous_x_range = self.fixed_range
        elif self.roll_on_tick == 1:
            self.previous_x_range = (min(axis_data), max(axis_data))
        elif tick % self.roll_on_tick == 0:
            rs = int(len(axis_data) / self.roll_on_tick) * self.roll_on_tick
            if rs == 0:
                range_width = axis_data[-1] - axis_data[0]
            else:
                data_subset = axis_data[rs - self.roll_on_tick:rs]
                range_width = data_subset[-1] - data_subset[0]
            self.previous_x_range = (axis_data[-1] - range_width * self.offset_left,
                                     (axis_data[-1] + range_width) + (range_width * self.offset_right))
        elif tick == 1:
            self.previous_x_range = (float(axis_data[0]),
                                     (axis_data[-1] - axis_data[0]) * self.roll_on_tick)
        return self.previous_x_range

    def get_y_range(self, axis_data, tick):
        if self.fixed_range is not None:
            self.previous_y_range = self.fixed_range
        elif self.roll_on_tick == 1:
            self.previous_y_range = (min(axis_data), max(axis_data))
        elif tick % self.roll_on_tick == 0:
            rs = int(len(axis_data) / self.roll_on_tick) * self.roll_on_tick
            if rs == 0:
                range_width = axis_data[-1] - axis_data[0]
            else:
                data_subset = axis_data[rs - self.roll_on_tick:rs]
                range_width = data_subset[-1] - data_subset[0]
            self.previous_y_range = (axis_data[-1] - range_width * self.offset_bottom,
                                     (axis_data[-1] + range_width) + (range_width * self.offset_top))
        elif tick == 1:
            self.previous_y_range = (float(axis_data[0]),
                                     (axis_data[-1] - axis_data[0]) * self.roll_on_tick)
        return self.previous_y_range
