from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
import sounddevice as sd
import queue
import numpy as np
import matplotlib.ticker as ticker
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import matplotlib.pyplot as plt
import matplotlib

from acoustic_locator import AcousticLocator
from main import getBeaconsFrequencies, getBeaconsPositions
matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)
        fig.tight_layout()


class Application(QtWidgets.QMainWindow):
    def __init__(self, acousticLocator):
        self.acoustic_locator = acousticLocator
        QtWidgets.QMainWindow.__init__(self)
        self.ui = uic.loadUi('main.ui', self)
        self.threadpool = QtCore.QThreadPool()

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.ui.gridLayout_3.addWidget(self.canvas, 2, 1, 1, 1)
        self.reference_plot = None
        self.q = queue.Queue(maxsize=20)

        self.timer = QtCore.QTimer()
        self.sampleRateField.setText("44100")
        self.kValueSlider.valueChanged.connect(self.update_k)
        self.sampleRateField.textChanged["QString"].connect(self.update_sample_rate)
        self.updateIntervalField.textChanged["QString"].connect(self.update_update_interval)
        self.pushButton.clicked.connect(self.start_worker)



    def start_worker(self):
        worker = Worker(self.start_stream, )
        self.threadpool.start(worker)	

    def start_stream(self):
        self.kValueSlider.setEnabled(False)
        self.sampleRateField.setEnabled(False)
        self.updateIntervalField.setEnabled(False)
        self.run_loop()
    
    def run_loop(self):
         while True:
            input_signal = self.acoustic_locator.record_audio()
            outs = self.acoustic_locator.compute_convolution(input_signal)
            powers = self.acoustic_locator.compute_powers(outs)
            position, r = self.acoustic_locator.compute_position(powers)
            print(position)
            # self.acoustic_locator.plot_position(position, r, self.canvas.axes)
            self.plot_position(position, r)
            
    
    def plot_position(self, receiver_position, r):
        pass

    def update_k(self, value):
        self.acoustic_locator.K = int(value)
        self.kLabel.setText(str(value))

    def update_sample_rate(self, value):
        self.acoustic_locator.sampleRate = int(value)
        sd.default.samplerate = self.samplerate
    
    def update_update_interval(self, value):
        pass

class Worker(QtCore.QRunnable):
    def __init__(self, function, *args, **kwargs):
        super(Worker, self).__init__()
        self.function = function
        self.args = args
        self.kwargs = kwargs

    @pyqtSlot()
    def run(self):
        self.function(*self.args, **self.kwargs)		



if __name__ == '__main__':
    beacon_positions = getBeaconsPositions()
    beacon_frequencies = getBeaconsFrequencies()
    locator = AcousticLocator(beacon_positions, beacon_frequencies)
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Application(locator)
    mainWindow.show()
    sys.exit(app.exec_())