import signal
import sys
from math import sin
from time import sleep

from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QApplication

running = True
app = QApplication(sys.argv)


def stop():
    """Stop current QApplication"""
    global running
    running = False
    app.exit(0)


def sin_wave_generator(*data_connectors, flip=False):
    """Sinus wave generator"""
    x = 0
    while running:
        x += 1
        for data_connector in data_connectors:
            if flip:
                data_connector.cb_append_data_point(x, sin(x * 0.025))
            else:
                data_connector.cb_append_data_point(sin(x * 0.025), x)
        sleep(0.01)


def colors():
    """Primitive color cycler"""
    while True:
        for r in range(50, 250, 2):
            for g in range(50, 250, 2):
                for b in range(50, 250, 2):
                    yield QColor(r, g, b)
                for c in range(50, 250, 2):
                    yield QColor(r, g, b - c)


# Initiate color generator
colors = colors()
# Connect SIGINT with stop function
signal.signal(signal.SIGINT, lambda sig, frame: stop())
