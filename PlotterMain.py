import sys
from PySide import QtGui, QtCore
import numpy as np
import pyperclip
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from PlotterOpen import OpenFile

app = QtGui.QApplication(sys.argv)
app.setStyle('Plastique')
GUI = Window()

#Create and group file open GUI items and support structure
open1 = OpenFile(1, GUI)
open2 = OpenFile(2, GUI)
open3 = OpenFile(3, GUI)
open4 = OpenFile(4, GUI)
open5 = OpenFile(5, GUI)
open6 = OpenFile(6, GUI)
open7 = OpenFile(7, GUI)
open8 = OpenFile(8, GUI)
open9 = OpenFile(9, GUI)
open10 = OpenFile(10, GUI)
openMaster = ['blank', open1, open2, open3, open4, open5, open6, open7, open8, open9, open10]

#Create and group signal GUI items and support structure
signals1 = Signals('#1f77b4', 'black', 1, GUI)
signals2 = Signals('#ff7f0e', 'black', 2, GUI)
signals3 = Signals('#2ca02c', 'black', 3, GUI)
signals4 = Signals('#d62728', 'black', 4, GUI)
signals5 = Signals('#9467bd', 'black', 5, GUI)
signals6 = Signals('#8c564b', 'black', 6, GUI)
signals7 = Signals('#e377c2', 'black', 7, GUI)
signals8 = Signals('#7f7f7f', 'black', 8, GUI)
signals9 = Signals('#bcbd22', 'black', 9, GUI)
signals10 = Signals('#17becf', 'black', 10, GUI)
signalsMaster = ['signalHeader', signals1, signals2, signals3, signals4, signals5, signals6, signals7, signals8,
                 signals9, signals10]

plotFrame = MatplotlibWidget(GUI)
plotFrame.build_plot()
GUI.tabWidget.currentChanged.connect(plotFrame.build_plot)

sys.exit(app.exec_())
