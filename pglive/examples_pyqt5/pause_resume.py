import pglive.examples_pyqt6 as examples
import signal
from threading import Thread

from PyQt6.QtWidgets import QWidget, QGridLayout, QPushButton, QLabel

from pglive.sources.data_connector import DataConnector
from pglive.sources.live_plot import LiveScatterPlot
from pglive.sources.live_plot_widget import LivePlotWidget

"""
In this example Pause and Resume functionality of DataConnector is demonstrated.
There are two buttons, that pause and resume live plotting.
When Live plot is paused, data are not collected.
"""
# Create parent widget
widget = LivePlotWidget(title="Line Plot @ 100Hz")
plot = LiveScatterPlot()
widget.addItem(plot)

# Create plot widget
parent_widget = QWidget()
parent_layout = QGridLayout()
parent_widget.setLayout(parent_layout)

# Connect plot with DataConnector
data_connector = DataConnector(plot, max_points=600)

# Create Pause, Resume buttons and Live status label
pause_button = QPushButton("Pause live plot")
resume_button = QPushButton("Resume live plot")
status_label = QLabel("Live")

# Add widgets int parent widget
parent_layout.addWidget(widget)
parent_layout.addWidget(pause_button)
parent_layout.addWidget(resume_button)
parent_layout.addWidget(status_label)

# Connect signals with respective methods
pause_button.clicked.connect(data_connector.pause)
resume_button.clicked.connect(data_connector.resume)

# Connect sig_paused and sig_resume with live signal status label
data_connector.sig_paused.connect(lambda: status_label.setText("Paused"))
data_connector.sig_resumed.connect(lambda: status_label.setText("Live"))

parent_widget.show()

Thread(target=examples.sin_wave_generator, args=(data_connector,)).start()
signal.signal(signal.SIGINT, lambda sig, frame: examples.stop())
examples.app.exec()
examples.stop()
