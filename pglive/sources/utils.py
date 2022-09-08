class RangeController:

    ...

class RollingRangeController(RangeController):

    def __init__(self, roll_on_tick=-1, padding=0):
        self.roll_on_tick = roll_on_tick
        self.padding = padding
