import random
import signal
import sys
from math import sin, cos
from time import sleep
from typing import List

from PySide2.QtGui import QColor
from PySide2.QtWidgets import QApplication

running = True
app = QApplication(sys.argv)


def stop():
    """Stop current QApplication"""
    global running
    running = False
    app.exit(0)


def sin_wave_generator(*data_connectors, flip=False):
    """Sine wave generator"""
    x = 0
    while running:
        x += 1
        for data_connector in data_connectors:
            if flip:
                data_connector.cb_append_data_point(x, sin(x * 0.025))
            else:
                data_connector.cb_append_data_point(sin(x * 0.025), x)
        sleep(0.01)


def cos_wave_generator(*data_connectors, flip=False):
    """Cosine wave generator"""
    x = 0
    while running:
        x += 1
        for data_connector in data_connectors:
            if flip:
                data_connector.cb_append_data_point(x, cos(x * 0.025))
            else:
                data_connector.cb_append_data_point(cos(x * 0.025), x)
        sleep(0.01)


def candle_generator(*data_connectors, flip=False):
    """Candle stick generator"""
    x = 0
    while running:
        x += 1
        for data_connector in data_connectors:
            a, b = sin(x * 0.025), sin(x * 0.020)
            s = min(a, b) - random.randint(0, 1000) * 1e-3
            e = max(a, b) + random.randint(0, 1000) * 1e-3
            candle = (a, b, s, e)
            if flip:
                data_connector.cb_append_data_point(x, candle)
            else:
                data_connector.cb_append_data_point(candle, x)
        sleep(0.01)


def category_generator(*data_connectors, categories: List, flip: bool = False):
    """Category generator"""
    x = 0
    while running:
        x += 1
        for data_connector in data_connectors:
            random_categories = random.sample(categories, random.randint(0, len(categories)))
            if flip:
                data_connector.cb_append_data_point(x * 0.01, random_categories)
            else:
                data_connector.cb_append_data_point(random_categories, x * 0.01)
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
