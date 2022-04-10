from PyQt5 import QtCore, QtWidgets, QtGui
from PyQt5.QtCore import pyqtSlot
from PyQt5 import uic
import sounddevice as sd
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import sys
import matplotlib.pyplot as plt
import matplotlib
from about import Ui_AboutWindow
from acoustic_locator import AcousticLocator
from main import getBeaconsFrequencies, getBeaconsPositions
matplotlib.use('Qt5Agg')


class MplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot()
        super(MplCanvas, self).__init__(fig)
        self.axes.set_aspect('equal')
    
    
        
class Application(QtWidgets.QMainWindow):
    def __init__(self, acousticLocator):
        self.acoustic_locator = acousticLocator
        QtWidgets.QMainWindow.__init__(self)
        self.setWindowIcon(QtGui.QIcon('assets/icon.jpeg'))
        self.ui = uic.loadUi('main.ui', self)
        self.threadpool = QtCore.QThreadPool()
        self.streamInitialized = False  

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        
        self.update_k(100) 
        self.sampleRateField.setText("44100")
        self.kValueSlider.valueChanged.connect(self.update_k)
        self.sampleRateField.textChanged["QString"].connect(self.update_sample_rate)
        self.startButton.clicked.connect(self.start_worker)
        self.aboutButton.clicked.connect(self.showAboutPage)

    def showAboutPage(self):
        self.aboutPage = QtWidgets.QMainWindow()
        self.ui2 = Ui_AboutWindow()
        self.ui2.setupUi(self.aboutPage)
        self.aboutPage.show()
        

    def start_worker(self):
        if (self.startButton.text() == "Start"):
            self.kValueSlider.setEnabled(False)
            self.sampleRateField.setEnabled(False)
            self.ui.horizontalLayout_2.addWidget(self.canvas)
            self.startButton.setText("Stop")
            self.streamInitialized = True
            self.worker = Worker(self.run_loop, )
            self.threadpool.start(self.worker)	
        else: 
            self.startButton.setText("Start")
            self.kValueSlider.setEnabled(True)
            self.sampleRateField.setEnabled(True)
            self.streamInitialized = False
            self.canvas.setParent(None)

    def run_loop(self):
         while True:
            if (self.streamInitialized):
                input_signal = self.acoustic_locator.record_audio()
                outs = self.acoustic_locator.compute_convolution(input_signal)
                powers = self.acoustic_locator.compute_powers(outs)
                position, r = self.acoustic_locator.compute_position(powers)
                print(f'X: {position[0][0]}, Y: {position[1][0]}')
                self.plot_position(position, r)
            else:
                break
            
    
    def plot_position(self, receiver_position, r):
        cir1 = plt.Circle((self.acoustic_locator.b1[0], self.acoustic_locator.b1[1]), r[0], color='red', fill=False)
        cir2 = plt.Circle((self.acoustic_locator.b2[0], self.acoustic_locator.b2[1]), r[1], color='blue', fill=False)
        cir3 = plt.Circle((self.acoustic_locator.b3[0], self.acoustic_locator.b3[1]), r[2], color='green', fill=False)
        
        self.canvas.axes.set_aspect('equal')
    
        self.canvas.axes.clear()
        self.canvas.axes.add_patch(cir1)
        self.canvas.axes.add_patch(cir2)
        self.canvas.axes.add_patch(cir3)

        self.canvas.axes.scatter(receiver_position[0], receiver_position[1], color='black', label='You')
        self.canvas.axes.scatter(self.acoustic_locator.b1[0], self.acoustic_locator.b1[1], color='red', label='Beacon 1')
        self.canvas.axes.scatter(self.acoustic_locator.b2[0], self.acoustic_locator.b2[1], color='blue', label='Beacon 2')
        self.canvas.axes.scatter(self.acoustic_locator.b3[0], self.acoustic_locator.b3[1], color='green', label='Beacon 3')
        
        self.canvas.axes.set_ylim( ymin=-5, ymax=5)	
        self.canvas.axes.set_xlim( xmin=-5, xmax=6)	
        self.canvas.axes.legend()
        self.canvas.draw()
        
      

    def update_k(self, value):
        self.acoustic_locator.K = round((int(value) * 0.01), 2)
        self.klabel.setText(f'K ({str(self.acoustic_locator.K)})')

    def update_sample_rate(self, value):
        self.acoustic_locator.sampleRate = int(value)
        sd.default.samplerate = self.sampleRateField


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
    try:
        beacon_positions = getBeaconsPositions()
        beacon_frequencies = getBeaconsFrequencies()
    except FileNotFoundError:
        exit('\033[91m' + 'Error! Configuration file not found')
        
    locator = AcousticLocator(beacon_positions, beacon_frequencies)
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = Application(locator)
    mainWindow.show()
    

    sys.exit(app.exec_())