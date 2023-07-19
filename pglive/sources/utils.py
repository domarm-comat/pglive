import datetime
from typing import List, Union

NUM = Union[int, float]
NUM_LIST = List[NUM]

MAX_SECONDS = 3.154e+9


def get_scaled_time_duration(seconds: float, short: bool = True) -> str:
    """
    Get str formatted duration from number of seconds.milliseconds.
    Output can be in short ar long format, depending on short flag param.
    """
    if seconds < 0:
        return ""
    if seconds >= MAX_SECONDS:
        return "> 100 Years"

    if short:
        sec, msec, min, day, hour, month, year = "s", "ms", "m", "D", "h", "M", "Y"
    else:
        sec, msec, min, day, hour, month, year = "Sec", "MSec", "Min", "Day", "Hour", "Month", "Year"

    d = datetime.datetime(1, 1, 1) + datetime.timedelta(seconds=seconds)

    if seconds < 60:
        milliseconds = int(d.microsecond / 1000)
        if milliseconds > 0:
            duration = "{} {} {} {}".format(d.second, sec, milliseconds, msec)
        else:
            duration = "{} {}".format(d.second, sec)
    elif 60 <= seconds < 3600:
        duration = "{} {} {} {}".format(d.minute, min, d.second, sec)
    elif 3600 <= seconds < 24 * 3600:
        duration = "{} {} {} {}".format(d.hour, hour, d.minute, min)
    elif 24 * 3600 <= seconds < 24 * 3600 * 28:
        duration = "{} {} {} {} {} {}".format(d.day - 1, day, d.hour, hour, d.minute, min)
    elif 24 * 3600 * 28 <= seconds < 24 * 3600 * 28 * 12:
        duration = "{} {} {} {} {} {}".format(d.month - 1, month, d.day, day, d.hour, hour)
    else:
        duration = "{} {} {} {} {} {}".format(d.year - 1, year, d.month, month, d.day, day)

    return duration


def dt_conversion(value: int, dt_format: str) -> str:
    try:
        return datetime.datetime.fromtimestamp(value).strftime(dt_format)
    except (ValueError, OSError, OverflowError):
        if value > 0:
            return "+inf"
        else:
            return "-inf"
