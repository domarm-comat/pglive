class Crosshair:
    """Keyword arguments related to Crosshair used in LivePlotWidget"""

    ENABLED = "Crosshair_Enabled"  # Toggle crosshair: bool
    LINE_PEN = "Crosshair_Line_Pen"  # Pen to draw crosshair: QPen
    TEXT_KWARGS = "Text_Kwargs"  # Kwargs for crosshair markers: dict
    X_AXIS = "Crosshair_x_axis"  # Pick axis [default bottom] format and source for x ticks displayed in crosshair: str
    Y_AXIS = "Crosshair_y_axis"  # Pick axis [default left] format and source for y ticks displayed in crosshair: str


class Axis:
    TICK_FORMAT = "Tick_Format"  # "Tick format"
    DATETIME = "DateTime"
    TIME = "Time"
    CATEGORY = "Category"
    CATEGORIES = "Categories"
    SHOW_ALL_CATEGORIES = "Show all categories"
    DURATION = "Duration"
    DURATION_FORMAT = "Duration_Format"
    # Duration format options
    DF_SHORT = "short"
    DF_LONG = "long"


class LeadingLine:
    HORIZONTAL = "Horizontal"
    VERTICAL = "Vertical"
    AXIS_X = "x"
    AXIS_Y = "y"

class Orientation:
    AUTO = "Auto"
    HORIZONTAL = "Horizontal"
    VERTICAL = "Vertical"