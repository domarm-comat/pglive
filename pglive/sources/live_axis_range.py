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
            return self.fixed_range
        if tick % self.roll_on_tick == 0:
            self.previous_x_range = (min(axis_data) - (axis_data[-1] - axis_data[0]) * self.offset_left,
                    max(axis_data) + (axis_data[-1] - axis_data[0]) * self.offset_right)
        elif tick == 0:
            self.previous_x_range = axis_data[0] * self.offset_left, axis_data[1] * self.offset_right
        elif tick == 1:
            self.previous_x_range = ((axis_data[-1] - axis_data[0]) * self.offset_left,
                                     (axis_data[-1] - axis_data[0]) * self.roll_on_tick * self.offset_right)
        return self.previous_x_range

    def get_y_range(self, axis_data, tick):
        if self.fixed_range is not None:
            return self.fixed_range
        if tick % self.roll_on_tick == 0:
            self.previous_y_range = (min(axis_data) - (axis_data[-1] - axis_data[0]) * self.offset_top,
                    max(axis_data) + (axis_data[-1] - axis_data[0]) * self.offset_bottom)
        elif tick == 0:
            self.previous_y_range = axis_data[0] * self.offset_top, axis_data[1] * self.offset_bottom
        elif tick == 1:
            self.previous_y_range = ((axis_data[-1] - axis_data[0]) * self.offset_top,
                                     (axis_data[-1] - axis_data[0]) * self.roll_on_tick * self.offset_bottom)
        return self.previous_y_range
