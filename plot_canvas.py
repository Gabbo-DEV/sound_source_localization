import sys
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QWidget, QApplication

class PlotCanvas(FigureCanvas):
    def __init__(self, parent):
        fig, self.ax = plt.subplots(figsize=(5, 4), dpi=200)
        super().__init__(fig)
        self.setParent(parent)

        """ 
        Matplotlib Script
        """
       
        


    def getAx(self):
        return self.ax


class AppDemo(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1600, 800)

        chart = PlotCanvas(self)

app = QApplication(sys.argv)        
demo = AppDemo()
demo.show()
sys.exit(app.exec_())