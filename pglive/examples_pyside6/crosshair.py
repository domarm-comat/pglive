import pglive.examples_pyside6 as examples
import signal
from threading import Thread

import pyqtgraph as pg  # type: ignore
from PySide6.QtCore import QPointF
from PySide6.QtWidgets import QWidget, QGridLayout, QLabel

from pglive.kwargs import Crosshair
from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveLinePlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
We create plot with Crosshair in this example.
Crosshair has few signals implemented:
    sig_crosshair_moved - fired when crosshair is moved within plot area
    sig_crosshair_out - fired when crosshair leaves plot area
    sig_crosshair_in - fired when crosshair enters plot area
There are three text labels displayed below plot showing crosshair status, X and Y value.
"""

# Create parent widget
parent_widget = QWidget()
parent_layout = QGridLayout()
parent_widget.setLayout(parent_layout)

# Define crosshair parameters
kwargs = {Crosshair.ENABLED: True,
          Crosshair.LINE_PEN: pg.mkPen(color="red", width=1),
          Crosshair.TEXT_KWARGS: {"color": "green"}}

# Create plot widget
widget = LivePlotWidget(title="Line Plot and Crosshair @ 100Hz", **kwargs)
"""
To add crosshair after LivePlotWidget has been created use:
widget.add_crosshair(crosshair_pen=pg.mkPen(color="red", width=1), crosshair_text_kwargs={"color": "green"})

To remove crosshair use:
widget.remove_crosshair()
"""

plot = LiveLinePlot()
widget.addItem(plot)

# Connect plot with DataConnector
data_connector = DataConnector(plot, max_points=600)

# Create crosshair X, Y label
ch_status_value = QLabel("Crosshair: Outside plot")
ch_x_value = QLabel("X: Unavailable")
ch_y_value = QLabel("Y: Unavailable")

# Add widgets int parent widget
parent_layout.addWidget(widget)
parent_layout.addWidget(ch_status_value)
parent_layout.addWidget(ch_x_value)
parent_layout.addWidget(ch_y_value)


def crosshair_moved(crosshair_pos: QPointF):
    """Update crosshair X, Y label when crosshair move"""
    ch_x_value.setText(f"X: {crosshair_pos.x()}")
    ch_y_value.setText(f"Y: {crosshair_pos.y()}")


def crosshair_out():
    """Update crosshair X, Y label when crosshair leaves plot area"""
    ch_status_value.setText("Crosshair: Outside plot")
    ch_x_value.setText(f"X: Unavailable")
    ch_y_value.setText(f"Y: Unavailable")


def crosshair_in():
    """Update crosshair X, Y label when crosshair enters plot area"""
    ch_status_value.setText("Crosshair: Inside plot")


# Connect moved and out signals with respective functions
widget.sig_crosshair_moved.connect(crosshair_moved)
widget.sig_crosshair_out.connect(crosshair_out)
widget.sig_crosshair_in.connect(crosshair_in)

parent_widget.show()

Thread(target=examples.sin_wave_generator, args=(data_connector,)).start()
signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
examples.app.exec()
examples.stop()
