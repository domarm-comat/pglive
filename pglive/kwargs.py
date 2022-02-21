class Crosshair:
    """Keyword arguments related to Crosshair used in LivePlotWidget"""

    ENABLED = "Crosshair_Enabled"  # Toggle crosshair: bool
    LINE_PEN = "Crosshair_Line_Pen"  # Pen to draw crosshair: QPen
    TEXT_KWARGS = "Text_Kwargs"  # Kwargs for crosshair markers: dict


class Axis:
    TICK_FORMAT = "Tick_Format"  # "Tick format"
    DATETIME = "DateTime"
    TIME = "Time"


class LeadingLine:
    HORIZONTAL = "Horizontal"
    VERTICAL = "Vertical"
    TEXT_COLOR = "TextColor"
    AXIS_X = "x"
    AXIS_Y = "y"
