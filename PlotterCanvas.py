from PySide import QtGui, QtCore
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

#Creates and manages the MatPlotLib aspects of the program


class MatplotlibWidget(FigureCanvas):
    def __init__(self, main_window):
        super(MatplotlibWidget, self).__init__(Figure())
        self.main_window = main_window
        self.figure = plt.figure(tight_layout=True, dpi=600, linewidth=2)
        # print(plt.rcParams)
        plt.rc('font', size=1.5)
        plt.rc('lines', linewidth=.4)
        plt.rc('xtick.major', pad=0, size=1, width=0.2)
        plt.rc('xtick.minor', pad=0, size=1, width=0.2)
        plt.rc('ytick.major', pad=0, size=1, width=0.2)
        plt.rc('ytick.minor', pad=0, size=1, width=0.2)
        plt.rc('axes', linewidth=0.2)
        plt.rc('figure', frameon=False)
        plt.rc('figure.subplot', bottom=0.1, hspace=0.1, left=0.01, right=0.1, top=0.1, wspace=0.1)

        # https://matplotlib.org/users/customizing.html
        self.canvas = FigureCanvas(self.figure)

        try:
            self.ax.cla()
            self.ax2.cla()
            self.ax3.cla()
        except AttributeError:
            pass

        self.ax = self.figure.add_subplot(111)
        self.ax2 = self.ax.twinx()
        self.ax2.set_visible(False)
        self.ax3 = self.ax.twinx()
        self.ax3.set_visible(False)
        self.axUnoActive = False
        self.axDosActive = False
        self.axTresActive = False

    def build_plot(self):
        if self.main_window.tabWidget.currentIndex() == 2:
            for item in signalsMaster:
                if not isinstance(item, str):
                    if item.isActive and item.fileSelect.currentText() != '':
                        if not isinstance(item, str):
                            if item.radio1.isChecked():
                                self.axUnoActive = True
                            elif item.radio2.isChecked():
                                self.axDosActive = True
                            elif item.radio3.isChecked():
                                self.axTresActive = True
                        if self.axUnoActive and self.axDosActive and self.axTresActive:
                            break
            for item in signalsMaster:
                if not isinstance(item, str):
                    if item.signalSelect.currentText() != 'None Selected' and item.isActive:
                        if item.radio1.isChecked():
                            if self.main_window.bottomRadio.isChecked():
                                self.ax.plot(
                                    openMaster[int(item.fileSelect.currentText())].signalDict['plotDist'],
                                    openMaster[int(item.fileSelect.currentText())].signalDict[
                                        item.signalSelect.currentText()],
                                    color=item.bgcolor)

                            else:
                                self.ax.plot(
                                    openMaster[int(item.fileSelect.currentText())].signalDict['plotTime'],
                                    openMaster[int(item.fileSelect.currentText())].signalDict[
                                        item.signalSelect.currentText()],
                                    color=item.bgcolor)
                                print(min(openMaster[int(item.fileSelect.currentText())].signalDict[
                                              item.signalSelect.currentText()]))
                                print(max(openMaster[int(item.fileSelect.currentText())].signalDict[
                                              item.signalSelect.currentText()]))
                        elif item.radio2.isChecked():
                            if self.main_window.bottomRadio.isChecked():
                                self.ax2.plot(
                                    openMaster[int(item.fileSelect.currentText())].signalDict['plotDist'],
                                    openMaster[int(item.fileSelect.currentText())].signalDict[
                                        item.signalSelect.currentText()],
                                    color=item.bgcolor)
                            else:
                                self.ax2.plot(
                                    openMaster[int(item.fileSelect.currentText())].signalDict['plotTime'],
                                    openMaster[int(item.fileSelect.currentText())].signalDict[
                                        item.signalSelect.currentText()],
                                    color=item.bgcolor)
                        elif item.radio3.isChecked():
                            if self.main_window.bottomRadio.isChecked():
                                self.ax3.plot(
                                    openMaster[int(item.fileSelect.currentText())].signalDict['plotDist'],
                                    openMaster[int(item.fileSelect.currentText())].signalDict[
                                        item.signalSelect.currentText()],
                                    color=item.bgcolor)
                            else:
                                self.ax3.plot(
                                    openMaster[int(item.fileSelect.currentText())].signalDict['plotTime'],
                                    openMaster[int(item.fileSelect.currentText())].signalDict[
                                        item.signalSelect.currentText()],
                                    color=item.bgcolor)

            if self.main_window.vertAutoCheck.isChecked():
                if self.axUnoActive:
                    self.main_window.vert_upper_auto_set(1)
                    self.main_window.vert_lower_auto_set(1)
                if self.axDosActive:
                    self.main_window.vert_upper_auto_set(2)
                    self.main_window.vert_lower_auto_set(2)
                if self.axTresActive:
                    self.main_window.vert_upper_auto_set(3)
                    self.main_window.vert_lower_auto_set(3)
                self.main_window.pad_axes()
            if self.main_window.horizAutoCheck.isChecked():
                self.main_window.horiz_lower_auto_set()
                self.main_window.horiz_upper_auto_set()
                self.main_window.pad_axes('horiz')
            self.ax.set_xlim(float(self.main_window.horizLowerEntry.text()),
                             float(self.main_window.horizUpperEntry.text()))
            if self.axUnoActive:
                self.ax.set_ylim(float(self.main_window.vertUnoLowerEntry.text()),
                                 float(self.main_window.vertUnoUpperEntry.text()))
                self.ax.set_visible(True)
            else:
                self.ax.set_visible(False)
            if self.axDosActive:
                self.ax.set_ylim(float(self.main_window.vertDosLowerEntry.text()),
                                 float(self.main_window.vertDosUpperEntry.text()))
                self.ax2.set_visible(True)
            else:
                self.ax2.set_visible(False)
            if self.axTresActive:
                self.ax3.set_ylim(float(self.main_window.vertTresLowerEntry.text()),
                                  float(self.main_window.vertTresUpperEntry.text()))
                self.ax3.spines["right"].set_position(('axes', 1.1))
                self.ax3.set_visible(True)
            else:
                self.ax3.set_visible(False)

            # self.ax.axhline(y=0, xmin=-10, xmax=10, c='black')
            self.canvas.draw()
            self.main_window.rightPlotLayout.addWidget(self.canvas)

