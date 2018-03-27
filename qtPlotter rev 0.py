import sys
from PySide import QtGui, QtCore
import numpy as np
import pyperclip
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas

class Window(QtGui.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 1366, 768)
        self.setWindowTitle("ISTIR Weld Data Plotter")
        self.setWindowIcon(QtGui.QIcon('par.ico'))

        self.windowLayout = QtGui.QGridLayout(self)
        self.windowLayout.setContentsMargins(5,5,5,5)
        self.setLayout(self.windowLayout)
        self.tabWidget = QtGui.QTabWidget(self)


        self.anyOpen = False
        self.open_tab()
        self.setup_tab()
        self.plot_tab()
        self.about_tab()

        #self.tabWidget.currentChanged.connect(plotFrame.build_plot)
        self.fileActiveList = []

        self.signals_header()
        self.axes()
        self.copy_signal()
        self.generate_signal()
        self.left_plot()
        self.horiz_plot()
        self.print_screen()







        self.windowLayout.addWidget(self.tabWidget)
        self.show()


    def open_tab(self):
        self.openTab = QtGui.QWidget()
        self.openTabLayout = QtGui.QGridLayout()
        self.openTab.setLayout(self.openTabLayout)
        self.openTabLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.openTabLayout.setContentsMargins(1,1,1,1)
        self.tabWidget.addTab(self.openTab, "Open")

    def setup_tab(self):
        #setup tab options
        self.setupTab = QtGui.QWidget()
        self.setupTabLayout = QtGui.QGridLayout()
        self.setupTab.setLayout(self.setupTabLayout)
        self.setupTabLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.setupTabLayout.setContentsMargins(1,1,1,1)

        #setup Signals area of tab
        self.signalLayout = QtGui.QGridLayout()
        self.signalLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.signalLayout.setContentsMargins(1,1,1,1)
        self.setupTabLayout.addLayout(self.signalLayout,0,0)

        #setup Axes area of tab
        self.axesLayout = QtGui.QGridLayout()
        self.axesLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.axesLayout.setContentsMargins(1,1,1,1)
        self.setupTabLayout.addLayout(self.axesLayout,0,1)

        #setup Copy area of tab
        self.copyLayout = QtGui.QHBoxLayout()
        self.copyLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.copyLayout.setContentsMargins(1,1,1,1)
        #self.copyLayout.setFixedWidth(350)
        self.setupTabLayout.addLayout(self.copyLayout,1,0)

        #setup Generate area of tab
        self.generateLayout = QtGui.QGridLayout()
        self.generateLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.generateLayout.setContentsMargins(1,1,1,1)
        self.setupTabLayout.addLayout(self.generateLayout,2,0,1,2)

        self.tabWidget.addTab(self.setupTab, "Setup")

    def signals_header(self):
        self.chooseLabel = QtGui.QLabel('Choose Signal')
        self.valueLabel = QtGui.QLabel('Signal Value')
        self.vertLabel = QtGui.QLabel('Vertical Axis')
        self.unoLabel = QtGui.QLabel(' 1')
        self.dosLabel = QtGui.QLabel(' 2')
        self.tresLabel = QtGui.QLabel(' 3')
        self.fileLabel = QtGui.QLabel('File')

        self.chooseLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.valueLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.vertLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.unoLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.dosLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.tresLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.fileLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.signalLayout.addWidget(self.chooseLabel,0,1,2,1)
        self.signalLayout.addWidget(self.valueLabel,0,2,2,1)
        self.signalLayout.addWidget(self.vertLabel,0,3,1,3)
        self.signalLayout.addWidget(self.unoLabel,1,3,1,1)
        self.signalLayout.addWidget(self.dosLabel,1,4,1,1)
        self.signalLayout.addWidget(self.tresLabel,1,5,1,1)
        self.signalLayout.addWidget(self.fileLabel,0,6,2,1)

    def axes(self):
        self.vertUnoLowerVal = '0.0'
        self.vertDosLowerVal = '0.0'
        self.vertTresLowerVal = '0.0'
        self.vertUnoUpperVal = '1.0'
        self.vertDosUpperVal = '1.0'
        self.vertTresUpperVal = '1.0'
        self.horizLowerVal = '0.0'
        self.horizUpperVal = '1.0'

        self.vertLabel = QtGui.QLabel("Define Vertical Axes' Values")
        self.vertAutoLabel = QtGui.QLabel('Auto')
        self.vertAutoCheck = QtGui.QCheckBox()
        self.vertAutoCheck.setChecked(True)
        self.vertLowerLabel = QtGui.QLabel('Lower')
        self.vertUpperLabel = QtGui.QLabel('Upper')
        self.vertUnoLabel = QtGui.QLabel('1:')
        self.vertDosLabel = QtGui.QLabel('2:')
        self.vertTresLabel = QtGui.QLabel('3:')
        self.vertUnoLowerButton = QtGui.QPushButton('◄')
        self.vertUnoLowerButton.released.connect(lambda: self.vert_lower_auto_set(1))
        self.vertDosLowerButton = QtGui.QPushButton('◄')
        self.vertDosLowerButton.released.connect(lambda: self.vert_lower_auto_set(2))
        self.vertTresLowerButton = QtGui.QPushButton('◄')
        self.vertTresLowerButton.released.connect(lambda: self.vert_lower_auto_set(3))
        self.vertUnoLowerEntry = QtGui.QLineEdit(str(self.vertUnoLowerVal))
        self.vertDosLowerEntry = QtGui.QLineEdit(str(self.vertDosLowerVal))
        self.vertTresLowerEntry = QtGui.QLineEdit(str(self.vertTresLowerVal))
        self.vertUnoUpperEntry = QtGui.QLineEdit(str(self.vertUnoUpperVal))
        self.vertDosUpperEntry = QtGui.QLineEdit(str(self.vertDosUpperVal))
        self.vertTresUpperEntry = QtGui.QLineEdit(str(self.vertTresUpperVal))
        self.vertUnoUpperButton = QtGui.QPushButton('►')
        self.vertUnoUpperButton.released.connect(lambda: self.vert_upper_auto_set(1))
        self.vertDosUpperButton = QtGui.QPushButton('►')
        self.vertDosUpperButton.released.connect(lambda: self.vert_upper_auto_set(2))
        self.vertTresUpperButton = QtGui.QPushButton('►')
        self.vertTresUpperButton.released.connect(lambda: self.vert_upper_auto_set(3))
        self.vertSpace = QtGui.QLabel()

        self.vertLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.vertAutoLabel.setFixedWidth(25)
        self.vertAutoCheck.setFixedWidth(20)
        self.vertLowerLabel.setFixedWidth(80)
        self.vertLowerLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.vertUpperLabel.setFixedWidth(80)
        self.vertUpperLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.vertUnoLabel.setFixedWidth(20)
        self.vertUnoLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.vertDosLabel.setFixedWidth(20)
        self.vertDosLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.vertTresLabel.setFixedWidth(20)
        self.vertTresLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.vertUnoLowerButton.setFixedWidth(20)
        self.vertDosLowerButton.setFixedWidth(20)
        self.vertTresLowerButton.setFixedWidth(20)
        self.vertUnoLowerEntry.setFixedWidth(80)
        self.vertDosLowerEntry.setFixedWidth(80)
        self.vertTresLowerEntry.setFixedWidth(80)
        self.vertUnoUpperEntry.setFixedWidth(80)
        self.vertDosUpperEntry.setFixedWidth(80)
        self.vertTresUpperEntry.setFixedWidth(80)
        self.vertUnoUpperButton.setFixedWidth(20)
        self.vertDosUpperButton.setFixedWidth(20)
        self.vertTresUpperButton.setFixedWidth(20)

        self.vertLabel.setFixedHeight(20)
        self.vertAutoLabel.setFixedHeight(20)
        self.vertAutoCheck.setFixedHeight(20)
        self.vertLowerLabel.setFixedHeight(20)
        self.vertUpperLabel.setFixedHeight(20)
        self.vertUnoLabel.setFixedHeight(20)
        self.vertDosLabel.setFixedHeight(20)
        self.vertTresLabel.setFixedHeight(20)
        self.vertUnoLowerButton.setFixedHeight(20)
        self.vertDosLowerButton.setFixedHeight(20)
        self.vertTresLowerButton.setFixedHeight(20)
        self.vertUnoLowerEntry.setFixedHeight(20)
        self.vertDosLowerEntry.setFixedHeight(20)
        self.vertTresLowerEntry.setFixedHeight(20)
        self.vertUnoUpperEntry.setFixedHeight(20)
        self.vertDosUpperEntry.setFixedHeight(20)
        self.vertTresUpperEntry.setFixedHeight(20)
        self.vertUnoUpperButton.setFixedHeight(20)
        self.vertDosUpperButton.setFixedHeight(20)
        self.vertTresUpperButton.setFixedHeight(20)
        self.vertSpace.setFixedHeight(10)

        self.horizLabel = QtGui.QLabel("Define Horizontal Axis' Values")
        self.horizAutoLabel = QtGui.QLabel('Auto')
        self.horizAutoCheck = QtGui.QCheckBox()
        self.horizAutoCheck.setChecked(True)
        self.horizLowerLabel = QtGui.QLabel('Lower')
        self.horizUpperLabel = QtGui.QLabel('Upper')
        self.horizLowerButton = QtGui.QPushButton('◄')
        self.horizLowerButton.released.connect(self.horiz_lower_auto_set)
        self.horizLowerEntry = QtGui.QLineEdit(str(self.horizLowerVal))
        self.horizUpperEntry = QtGui.QLineEdit(str(self.horizUpperVal))
        self.horizUpperButton = QtGui.QPushButton('►')
        self.horizUpperButton.released.connect(self.horiz_upper_auto_set)
        self.horizSpace = QtGui.QLabel()

        self.horizLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.horizAutoLabel.setFixedWidth(25)
        self.horizAutoCheck.setFixedWidth(20)
        self.horizLowerLabel.setFixedWidth(80)
        self.horizLowerLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.horizUpperLabel.setFixedWidth(80)
        self.horizUpperLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.horizLowerButton.setFixedWidth(20)
        self.horizLowerEntry.setFixedWidth(80)
        self.horizUpperEntry.setFixedWidth(80)
        self.horizUpperButton.setFixedWidth(20)

        self.horizLabel.setFixedHeight(20)
        self.horizAutoLabel.setFixedHeight(20)
        self.horizAutoCheck.setFixedHeight(20)
        self.horizLowerLabel.setFixedHeight(20)
        self.horizUpperLabel.setFixedHeight(20)
        self.horizLowerButton.setFixedHeight(20)
        self.horizLowerEntry.setFixedHeight(20)
        self.horizUpperEntry.setFixedHeight(20)
        self.horizUpperButton.setFixedHeight(20)
        self.horizSpace.setFixedHeight(150)

        self.typeLabel = QtGui.QLabel('Define Horizontal\nAxis Type')
        self.typeLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.horizButtonGroup = QtGui.QButtonGroup()
        self.topRadio = QtGui.QRadioButton('Time')
        self.topRadio.setChecked(True)
        self.bottomRadio = QtGui.QRadioButton('Distance')
        self.horizButtonGroup.addButton(self.topRadio)
        self.horizButtonGroup.addButton(self.bottomRadio)

        self.axesLayout.addWidget(self.vertLabel,0,1,1,4)
        self.axesLayout.addWidget(self.vertAutoLabel,1,0)
        self.axesLayout.addWidget(self.vertAutoCheck,1,1)
        self.axesLayout.addWidget(self.vertLowerLabel,1,2)
        self.axesLayout.addWidget(self.vertUpperLabel,1,3)
        self.axesLayout.addWidget(self.vertUnoLabel,2,0)
        self.axesLayout.addWidget(self.vertDosLabel,3,0)
        self.axesLayout.addWidget(self.vertTresLabel,4,0)
        self.axesLayout.addWidget(self.vertUnoLowerButton,2,1)
        self.axesLayout.addWidget(self.vertDosLowerButton,3,1)
        self.axesLayout.addWidget(self.vertTresLowerButton,4,1)
        self.axesLayout.addWidget(self.vertUnoLowerEntry,2,2)
        self.axesLayout.addWidget(self.vertDosLowerEntry,3,2)
        self.axesLayout.addWidget(self.vertTresLowerEntry,4,2)
        self.axesLayout.addWidget(self.vertUnoUpperEntry,2,3)
        self.axesLayout.addWidget(self.vertDosUpperEntry,3,3)
        self.axesLayout.addWidget(self.vertTresUpperEntry,4,3)
        self.axesLayout.addWidget(self.vertUnoUpperButton,2,4)
        self.axesLayout.addWidget(self.vertDosUpperButton,3,4)
        self.axesLayout.addWidget(self.vertTresUpperButton,4,4)
        self.axesLayout.addWidget(self.vertSpace,5,1)

        self.axesLayout.addWidget(self.horizLabel,6,1,1,4)
        self.axesLayout.addWidget(self.horizAutoLabel,7,0)
        self.axesLayout.addWidget(self.horizAutoCheck,7,1)
        self.axesLayout.addWidget(self.horizLowerLabel,7,2)
        self.axesLayout.addWidget(self.horizUpperLabel,7,3)
        self.axesLayout.addWidget(self.horizLowerButton,8,1)
        self.axesLayout.addWidget(self.horizLowerEntry,8,2)
        self.axesLayout.addWidget(self.horizUpperEntry,8,3)
        self.axesLayout.addWidget(self.horizUpperButton,8,4)

        self.axesLayout.addWidget(self.typeLabel,10,1,2,2)
        self.axesLayout.addWidget(self.topRadio,10,3)
        #self.axesLayout.addWidget(self.bottomRadio,11,3)
        self.axesLayout.addWidget(self.horizSpace,12,1)

    def copy_signal(self):
        self.mainButton = QtGui.QPushButton('Copy chosen signals')
        self.fromLabel = QtGui.QLabel('from File')
        self.firstBox = QtGui.QComboBox()
        self.toLabel = QtGui.QLabel('to File')
        self.secondBox = QtGui.QComboBox()
        self.copySpacer = QtGui.QLabel()

        self.copyLayout.addWidget(self.mainButton)
        self.copyLayout.addWidget(self.fromLabel)
        self.copyLayout.addWidget(self.firstBox)
        self.copyLayout.addWidget(self.toLabel)
        self.copyLayout.addWidget(self.secondBox)
        self.copyLayout.addWidget(self.copySpacer)

        self.mainButton.setFixedWidth(120)
        self.mainButton.setFixedHeight(30)
        self.fromLabel.setFixedWidth(50)
        self.fromLabel.setFixedHeight(30)
        self.firstBox.setFixedWidth(40)
        self.firstBox.setFixedHeight(30)
        self.toLabel.setFixedWidth(40)
        self.toLabel.setFixedHeight(30)
        self.secondBox.setFixedWidth(40)
        self.secondBox.setFixedHeight(30)
        self.copySpacer.setFixedWidth(150)

    def generate_signal(self):
        self.sourceLabel = QtGui.QLabel('Select\nFile')
        self.firstLabel = QtGui.QLabel('Choose First Signal')
        self.secondLabel = QtGui.QLabel('Choose Second Signal')
        self.fileSelect = QtGui.QComboBox()
        self.spaceLabel = QtGui.QLabel(' ')
        self.firstEntry = QtGui.QLineEdit()
        self.timesLabel = QtGui.QLabel('*')
        self.firstBox = QtGui.QComboBox()
        self.addLabel = QtGui.QLabel('+')
        self.secondEntry = QtGui.QLineEdit()
        self.multiLabel = QtGui.QLabel('*')
        self.secondBox = QtGui.QComboBox()
        self.equalsLabel = QtGui.QLabel('=')
        self.nameLabel = QtGui.QLabel('Select name of\nnew variable')
        self.nameEntry = QtGui.QLineEdit()
        self.generateButton = QtGui.QPushButton('Generate\nNew\nSignal')

        self.generateLayout.addWidget(self.sourceLabel,0,0)
        self.generateLayout.addWidget(self.firstLabel,0,4)
        self.generateLayout.addWidget(self.secondLabel,0,8)
        self.generateLayout.addWidget(self.fileSelect,1,0)
        self.generateLayout.addWidget(self.spaceLabel,1,1)
        self.generateLayout.addWidget(self.firstEntry,1,2)
        self.generateLayout.addWidget(self.timesLabel,1,3)
        self.generateLayout.addWidget(self.firstBox,1,4)
        self.generateLayout.addWidget(self.addLabel,1,5)
        self.generateLayout.addWidget(self.secondEntry,1,6)
        self.generateLayout.addWidget(self.multiLabel,1,7)
        self.generateLayout.addWidget(self.secondBox,1,8)
        self.generateLayout.addWidget(self.equalsLabel,1,9)
        self.generateLayout.addWidget(self.nameLabel,2,0,1,4)
        self.generateLayout.addWidget(self.nameEntry,2,4)
        self.generateLayout.addWidget(self.generateButton,0,10,3,1)

        self.fileSelect.setFixedWidth(45)
        self.spaceLabel.setFixedWidth(1)
        self.firstEntry.setFixedWidth(40)
        self.timesLabel.setFixedWidth(5)
        self.firstBox.setFixedWidth(250)
        self.addLabel.setFixedWidth(10)
        self.secondEntry.setFixedWidth(40)
        self.multiLabel.setFixedWidth(5)
        self.secondBox.setFixedWidth(250)
        self.equalsLabel.setFixedWidth(5)
        self.nameEntry.setFixedWidth(250)
        self.generateButton.setFixedWidth(55)

        self.sourceLabel.setFixedHeight(45)
        self.firstLabel.setFixedHeight(30)
        self.secondLabel.setFixedHeight(30)
        self.fileSelect.setFixedHeight(30)
        self.spaceLabel.setFixedHeight(30)
        self.firstEntry.setFixedHeight(30)
        self.timesLabel.setFixedHeight(30)
        self.firstBox.setFixedHeight(30)
        self.addLabel.setFixedHeight(30)
        self.secondEntry.setFixedHeight(30)
        self.multiLabel.setFixedHeight(30)
        self.secondBox.setFixedHeight(30)
        self.equalsLabel.setFixedHeight(30)
        self.nameLabel.setFixedHeight(30)
        self.nameEntry.setFixedHeight(30)
        self.generateButton.setFixedHeight(90)

        self.sourceLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.firstLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.secondLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.nameLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def plot_tab(self):
        #setup main plot area
        self.plotTab = QtGui.QWidget()
        self.plotTabLayout = QtGui.QGridLayout()
        self.plotTab.setLayout(self.plotTabLayout)
        self.plotTabLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.plotTabLayout.setContentsMargins(1,1,1,1)

        #setup left plot area
        self.leftPlotLayout = QtGui.QGridLayout()
        self.plotTabLayout.addLayout(self.leftPlotLayout,0,0,2,1)


        #setup right plot area
        self.rightPlotLayout = QtGui.QGridLayout()
        self.plotTabLayout.addLayout(self.rightPlotLayout,0,1)
        #self.plotHolder = QtGui.QLineEdit()
        #self.plotHolder.setFixedWidth(700)
        #self.plotHolder.setFixedHeight(700)
        #self.rightPlotLayout.addWidget(self.plotHolder)


        #setup horizontal axis area
        self.bottomLPlotLayout = QtGui.QHBoxLayout()
        self.plotTabLayout.addLayout(self.bottomLPlotLayout,1,1)
        self.bottomLPlotLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.bottomCPlotLayout = QtGui.QHBoxLayout()
        self.plotTabLayout.addLayout(self.bottomCPlotLayout,1,1)
        self.bottomCPlotLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)



        self.tabWidget.addTab(self.plotTab, "Plot")

    def print_screen(self):
        self.prntScrnLayout = QtGui.QHBoxLayout()
        self.prntScrnButton = QtGui.QPushButton('Print Screen')
        self.saveScrnButton = QtGui.QPushButton('Save Screen')
        self.prntScrnLayout.addWidget(self.prntScrnButton)
        self.prntScrnLayout.addWidget(self.saveScrnButton)
        self.prntScrnLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.leftPlotLayout.addLayout(self.prntScrnLayout,22,0,1,4)

    def left_plot(self):
        self.plotActiveLabel = QtGui.QLabel('Plot?')
        self.plotActiveLabel.setFixedHeight(25)
        self.plotActiveLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.plotActiveLabel.setStyleSheet('border:1px solid grey')
        self.plotFileLabel = QtGui.QLabel('File')
        self.plotFileLabel.setFixedHeight(25)
        self.plotFileLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.plotFileLabel.setStyleSheet('border:1px solid grey')
        self.plotAxisLabel = QtGui.QLabel('Axis')
        self.plotAxisLabel.setFixedHeight(25)
        self.plotAxisLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.plotAxisLabel.setStyleSheet('border:1px solid grey')
        self.plotSignalLabel = QtGui.QLabel('Signal')
        self.plotSignalLabel.setFixedHeight(25)
        self.plotSignalLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.plotSignalLabel.setStyleSheet('border:1px solid grey')
        self.plotValueLabel = QtGui.QLabel('Value')
        self.plotValueLabel.setFixedHeight(25)
        self.plotValueLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.plotValueLabel.setStyleSheet('border:1px solid grey')

        self.plotSignalLabel.setFixedWidth(250)

        self.leftPlotLayout.addWidget(self.plotActiveLabel,0,0)
        self.leftPlotLayout.addWidget(self.plotFileLabel,0,1)
        self.leftPlotLayout.addWidget(self.plotAxisLabel,0,2)
        self.leftPlotLayout.addWidget(self.plotValueLabel,0,3)
        self.leftPlotLayout.addWidget(self.plotSignalLabel,1,0,1,4)

    def horiz_plot(self):
        self.lineNumLabel = QtGui.QLabel('Line Number:')
        self.lineValLabel = QtGui.QLabel('1')
        self.highlightLabel = QtGui.QLabel('Highlight Line Start/End:')
        self.highlightLowValLabel = QtGui.QLabel('0')
        self.highlightHiValLabel = QtGui.QLabel('0')
        self.xValLabel = QtGui.QLabel('0.00')
        self.xUnitLabel = QtGui.QLabel('seconds')

        self.lineNumLabel.setFixedWidth(65)
        self.lineValLabel.setFixedWidth(15)
        self.highlightLabel.setFixedWidth(120)
        self.highlightLowValLabel.setFixedWidth(15)
        self.highlightHiValLabel.setFixedWidth(15)
        self.xValLabel.setFixedWidth(15)
        self.xUnitLabel.setFixedWidth(40)

        self.bottomLPlotLayout.addWidget(self.lineNumLabel)
        self.bottomLPlotLayout.addWidget(self.lineValLabel)
        self.bottomLPlotLayout.addWidget(self.highlightLabel)
        self.bottomLPlotLayout.addWidget(self.highlightLowValLabel)
        self.bottomLPlotLayout.addWidget(self.highlightHiValLabel)
        self.bottomCPlotLayout.addWidget(self.xValLabel)
        self.bottomCPlotLayout.addWidget(self.xUnitLabel)

    def about_tab(self):
        self.aboutTab = QtGui.QWidget()
        self.aboutTab.setLayout(QtGui.QHBoxLayout())
        self.aboutLabel = QtGui.QLabel('© 2018 PaR Systems, Inc.\nDeveloper: Jeremy Brown (jbrown@par.com)')
        self.aboutLabel.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.aboutTab.layout().addWidget(self.aboutLabel)
        self.tabWidget.addTab(self.aboutTab, "About")

    def add_active_files(self, input):
        if str(input) not in self.fileActiveList:
            self.fileActiveList.append(str(input))
            self.fileActiveList.sort()
            for item in signalsMaster:
                if isinstance(item, str) is False:
                    item.fileSelect.clear()
                    item.fileSelect.addItems(self.fileActiveList)
                    item.fileSelect.setParent = None
                    self.signalLayout.addWidget(item.fileSelect, item.number + 1, 6)
                    item.fileCombo.clear()
                    item.fileCombo.addItems(self.fileActiveList)
                    item.fileCombo.setParent = None
                    self.leftPlotLayout.addWidget(item.fileCombo, 2 * item.number, 1)
        self.horiz_radio_update()

    def remove_active_files(self, input):
        if str(input) in self.fileActiveList:
            self.fileActiveList.remove(str(input))
            self.fileActiveList.sort()
            for item in signalsMaster:
                if isinstance(item, str) is False:
                    item.fileSelect.clear()
                    item.fileSelect.addItems(self.fileActiveList)
                    item.fileSelect.setParent = None
                    self.signalLayout.addWidget(item.fileSelect, item.number + 1, 6)
                    item.fileCombo.clear()
                    item.fileCombo.addItems(self.fileActiveList)
                    item.fileCombo.setParent = None
                    self.leftPlotLayout.addWidget(item.fileCombo, 2 * item.number, 1)
        self.horiz_radio_update()

    def redline_signal_value(self):
        pass

    def horiz_radio_update(self):
        self.radioList = []
        self.count = 0
        for item in signalsMaster:
            if isinstance(item, str) == False:
                self.radioList += item.selectList
        for item in self.radioList:
            if item == 'Weld Distance, in' or item == 'Weld Distance, mm':
                self.count += 1
        if self.count == 10:
            self.axesLayout.addWidget(self.bottomRadio, 11, 3)
        else:
            self.bottomRadio.setParent(None)
            self.topRadio.setChecked(True)

    def horiz_lower_auto_set(self):
        minlist = []
        if self.bottomRadio.isChecked() == True:
            for i,val in enumerate(openMaster):
                if isinstance(val, str) == False and val.fileName != '':
                    minlist.append(min(val.signalDict['plotDist']))
        else:
            for i,val in enumerate(openMaster):
                if isinstance(val, str) == False and val.fileName != '':
                    minlist.append(min(val.signalDict['plotTime']))

            self.horizLowerEntry.setText(str(min(minlist)))

    def horiz_upper_auto_set(self):
        maxlist = []
        if self.bottomRadio.isChecked() == True:
            for i,val in enumerate(openMaster):
                if isinstance(val, str) == False and val.fileName != '':
                    maxlist.append(max(val.signalDict['plotDist']))
        else:
            for i,val in enumerate(openMaster):
                if isinstance(val, str) == False and val.fileName != '':
                    maxlist.append(max(val.signalDict['plotTime']))
            self.horizUpperEntry.setText(str(max(maxlist)))
        if float(self.horizUpperEntry.text()) <= float(self.horizLowerEntry.text()):
            self.horizUpperEntry.setText(str(float(self.horizLowerEntry.text()) + 1))

    def vert_lower_auto_set(self, input):
        minlist = []
        for item in signalsMaster:
            if isinstance(item, str) == False:
                if item.fileSelect.currentText() != '':
                    file = int(item.fileSelect.currentText())
                    signal = item.signalSelect.currentText()
                    if item.radio1.isChecked() == True and input == 1:
                        minlist.append(min(openMaster[file].signalDict[signal]))
                    elif item.radio2.isChecked() == True and input == 2:
                        minlist.append(min(openMaster[file].signalDict[signal]))
                    elif item.radio3.isChecked() == True and input == 3:
                        minlist.append(min(openMaster[file].signalDict[signal]))

        if minlist  == []:
            minlist = [0]

        if input == 1:
            self.vertUnoLowerEntry.setText(str(min(minlist)))
        elif input == 2:
            self.vertDosLowerEntry.setText(str(min(minlist)))
        elif input == 3:
            self.vertTresLowerEntry.setText(str(min(minlist)))

    def vert_upper_auto_set(self, input):
        maxlist = []
        for item in signalsMaster:
            if isinstance(item,str) == False:
                if item.fileSelect.currentText() != '':
                    file = int(item.fileSelect.currentText())
                    signal = item.signalSelect.currentText()
                    if item.radio1.isChecked() == True and input == 1:
                        maxlist.append(max(openMaster[file].signalDict[signal]))
                    elif item.radio2.isChecked() == True and input == 2:
                        minlist.append(min(openMaster[file].signalDict[signal]))
                    elif item.radio3.isChecked() == True and input == 3:
                        minlist.append(min(openMaster[file].signalDict[signal]))

        if maxlist == []:
            maxlist = [1]

        if input == 1:
            self.vertUnoUpperEntry.setText(str(max(maxlist)))
        elif input == 2:
            self.vertDosUpperEntry.setText(str(max(maxlist)))
        elif input == 3:
            self.vertTresUpperEntry.setText(str(max(maxlist)))

    def build_plot(self):
        if self.tabWidget.currentIndex() == 2:
            for val in openMaster:
                if isinstance(val, str) == False:
                    self.ax = self.figure.add_subplot(111, autoscale_on=True)
                    if val.fileName != '':
                        self.axUnoActive = False
                        self.axDosActive = False
                        self.axTresActive = False
                        for item in signalsMaster:
                            if isinstance(item, str) == False:
                                if item.radio1.isChecked() == True:
                                    self.axUnoActive = True
                                elif item.radio2.isChecked() == True:
                                    self.axDosActive = True
                                elif item.radio3.isChecked() == True:
                                    self.axTresActive = True
                            if self.axUnoActive == True and self.axDosActive == True and self.axTresActive == True:
                                break
                        if self.vertAutoCheck.isChecked() == True:
                            if self.axUnoActive == True:
                                self.vert_upper_auto_set(1)
                                self.vert_lower_auto_set(1)
                            if self.axDosActive == True:
                                self.vert_upper_auto_set(2)
                                self.vert_lower_auto_set(2)
                            if self.axTresActive == True:
                                self.vert_upper_auto_set(3)
                                self.vert_lower_auto_set(3)
                        if self.horizAutoCheck.isChecked() == True:
                            self.horiz_lower_auto_set()
                            self.horiz_upper_auto_set()
                        self.ax.set_xlim(float(self.horizLowerEntry.text()),float(self.horizUpperEntry.text()))
                        self.ax.set_ylim(float(self.vertUnoLowerEntry.text()),float(self.vertUnoUpperEntry.text()))
                        if self.axDosActive == True:
                            self.ax2 = self.ax.twinx()
                            self.ax.set_ylim(float(self.vertDosLowerEntry.text()), float(self.vertDosUpperEntry.text()))
                        if self.axTresActive == True:
                            self.ax3 = self.ax.twinx()
                            self.ax3.set_ylim(float(self.vertTresLowerEntry.text()), float(self.vertTresUpperEntry.text()))
                            self.ax3.spines["right"].set_position(('axes', 1.1))
                        for item in signalsMaster:
                            if isinstance(item, str) == False:
                                if item.signalSelect.currentText() != 'None Selected' and item.numberButton.isActive == True:
                                    if item.radio1.isChecked() == True:
                                        if self.bottomRadio.isChecked() == True:
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
                                    elif item.radio2.isChecked() == True:
                                        if self.bottomRadio.isChecked() == True:
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
                                    elif item.radio3.isChecked() == True:
                                        if self.bottomRadio.isChecked() == True:
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
                        break
            self.ax.axhline(y=0, xmin=-10, xmax=10, c='black')
            self.canvas.draw()
            self.rightPlotLayout.addWidget(self.canvas)

class open_file(QtGui.QFrame):
    def __init__(self,number):
        super(open_file, self).__init__()
        self.number = number
        self.isActive = False
        self.fileName = ''
        self.offset  = 0.0
        self.schedule = []
        self.header = []
        self.signalDict = {}
        self.signalList = []

        self.openLayout = QtGui.QGridLayout()
        self.setFrameShape(QtGui.QFrame.StyledPanel)
        self.setFrameShadow(QtGui.QFrame.Raised)
        self.setLayout(self.openLayout)

        self.setAcceptDrops(True)

        self.set_tab_pos()
        self.build_gui()



        GUI.openTabLayout.addWidget(self,self.openRow,self.openCol)

    def set_tab_pos(self):
        if self.number < 6:
            self.openRow = self.number - 1
            self.openCol = 0
        else:
            self.openRow = self.number - 6
            self.openCol = 1

    def build_gui(self):
        self.setLayout(QtGui.QGridLayout())
        self.setFixedHeight(120)

        self.bottomSpace = QtGui.QLabel()
        self.openIndex = QtGui.QLabel('   '+str(self.number))
        self.radioSelect = QtGui.QRadioButton()
        self.openButton = QtGui.QPushButton('Open File')
        self.openButton.released.connect(self.file_grab)
        self.headerButton = QtGui.QPushButton('Read Header')
        self.headerButton.released.connect(self.disp_header)
        self.scheduleButton = QtGui.QPushButton('Read WLD Program')
        self.scheduleButton.released.connect(self.disp_schedule)
        self.clearButton = QtGui.QPushButton('Clear')
        self.clearButton.released.connect(self.deactivate)
        self.fileLabel = QtGui.QLineEdit(self.fileName)
        self.fileLabel.setReadOnly(True)

        #self.fileLabel.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.RightToLeft | QtCore.Qt.AlignJustify)
        self.offsetLabel = QtGui.QLabel('Horizontal Offset')
        self.offsetEntry = QtGui.QLineEdit(str(self.offset))

        self.openIndex.setFixedWidth(30)
        self.openIndex.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.radioSelect.setFixedWidth(15)
        self.openButton.setFixedHeight(30)
        self.openButton.setFixedWidth(80)
        self.headerButton.setFixedHeight(30)
        self.headerButton.setFixedWidth(100)
        self.scheduleButton.setFixedHeight(30)
        self.scheduleButton.setFixedWidth(120)
        self.clearButton.setFixedWidth(30)
        self.clearButton.setFixedHeight(30)
        self.fileLabel.setFixedHeight(30)
        self.fileLabel.setFixedWidth(350)
        self.offsetLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.offsetLabel.setFixedHeight(30)
        self.offsetEntry.setFixedWidth(150)
        self.offsetEntry.setFixedHeight(30)

        self.openLayout.addWidget(self.openIndex,0,0,1,2)
        #self.openLayout.addWidget(self.radioSelect,0,1,1,1)
        self.openLayout.addWidget(self.openButton,0,2,1,1)
        #self.openLayout.addWidget(self.headerButton,0,3,1,1)
        #self.openLayout.addWidget(self.scheduleButton,0,4,1,1)
        self.openLayout.addWidget(self.clearButton,1,0,1,2)
        self.openLayout.addWidget(self.fileLabel,1,2,1,4)
        self.openLayout.addWidget(self.offsetLabel,2,2,1,1)
        self.openLayout.addWidget(self.offsetEntry,2,3,1,3)
        #self.openLayout.addWidget(self.bottomSpace,3,0,1,1)

    def dragEnterEvent(self, event):
        event.accept()
        '''
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()
        '''

    def dropEvent(self, event):
        self.fileName = str(event.mimeData().urls()[0])[28:-2]
        self.fileLabel.setText(self.fileName)
        self.initial_read()

    def file_grab(self):
        self.fileDialog = QtGui.QWidget()
        self.fileNameOld = self.fileName
        try:
            self.fileName = QtGui.QFileDialog.getOpenFileName(self.fileDialog, 'Open File', '/')[0]
        except:
            pass
        if self.fileName == '':
            self.fileName = self.fileNameOld
        elif self.fileName != self.fileNameOld:
            self.fileLabel.setText(self.fileName)
            self.isActive = True
            self.initial_read()

    def initial_read(self):
        with open(self.fileName,'r') as self.f:
            for line in self.f:
                self.header.append(line.strip())
                if 'Weld Program Listing:' in line or 'START OF WELD PROGRAM LISTING' in line:
                    self.header.pop()
                    self.openLayout.addWidget(self.headerButton, 0, 3, 1, 1)
                    self.openLayout.addWidget(self.scheduleButton, 0, 4, 1, 1)
                    self.weld_data_read()
                    break
                elif 'Sample Rate :' in line:
                    self.header = []
                    self.sampleRate = float(line.split(' ')[3])
                    self.data_recoder_read()
                    break

    def data_recoder_read(self):
        self.signalDict['None Selected'] = []

        for line in self.f:
            if str.isdigit(line[0]) == True or line[0] == '-':
                self.signalDict['None Selected'].append(0.0)
                for i, val in enumerate(line.strip().split(',')):
                    try:
                        self.signalDict[self.signalList[i]].append(float(val))
                    except:
                        self.signalDict[self.signalList[i]] = [float(val)]
            else:
                self.signalList.append(line.strip())
        self.signalDict['Weld Time, sec'] = []
        for i,val in enumerate(self.signalDict['None Selected']):
            self.signalDict['Weld Time, sec'].append(float(i)/self.sampleRate)
        for i,val in enumerate(self.signalDict.keys()):
            self.signalDict[val] = np.asanyarray(self.signalDict[val])
        self.signalList.insert(0, 'None Selected')
        self.signalDict['plotTime'] = self.signalDict['Weld Time, sec']
        if 'Weld Distance, in' in self.signalList:
            self.signalDict['plotDist'] = self.signalDict['Weld Distance, in']
        if 'Weld Distance, mm' in self.signalList:
            self.signalDict['plotDist'] = self.signalDict['Weld Distance, mm']

        print(len(self.signalDict['plotTime']))
        print(len(self.signalDict['Weld Time, sec']))
        print(len(self.signalDict['None Selected']))
        print(len(self.signalDict[self.signalList[12]]))
        GUI.add_active_files(self.number)

    def weld_data_read(self):
        self.f.readline()
        for line in self.f:
            if line.strip() == 'Data' or 'Data:' in line or '=====' in line:
                break
            self.schedule.append(line.strip())

        for i in range(len(self.schedule)-1,0,-1):
            if self.schedule[i].strip() == '':
                self.schedule.pop()
            else:
                break

        for line in self.f:
                if 'Sample Rate :' in line:
                    self.sampleRate = float(line.split(' ')[3])
                    self.data_recoder_read()
                    break

    def deactivate(self):
        self.isActive = False
        self.fileName = ''
        self.offset  = 0.0
        self.schedule = []
        self.header = []
        self.signalDict = {}
        self.signalList = []
        self.fileLabel.setText(self.fileName)
        self.headerButton.setParent(None)
        self.scheduleButton.setParent(None)
        GUI.remove_active_files(str(self.number))


    def disp_header(self):
        self.headerPanel = QtGui.QWidget()
        self.headerPanelLayout = QtGui.QVBoxLayout()
        self.headerPanel.setLayout(self.headerPanelLayout)
        self.headerPanel.setWindowTitle('File '+str(self.number)+' Header Info')
        self.headerText = ''
        for item in self.header:
            self.headerText += item+'\n'
        self.headerLabel = QtGui.QLabel(self.headerText)
        self.headerLabel.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.headerPanelLayout.addWidget(self.headerLabel)
        self.headerPanel.show()

    def disp_schedule(self):
        self.schedulePanel = QtGui.QWidget()
        self.schedulePanel.setMinimumHeight(720)
        self.schedulePanel.setMinimumWidth(450)
        self.schedulePanel.setWindowTitle('File ' + str(self.number) + ' Weld Schedule')
        self.schedulePanelLayout = QtGui.QVBoxLayout()
        self.schedulePanel.setLayout(self.schedulePanelLayout)
        self.schedulePanelButtonsLayout = QtGui.QHBoxLayout()
        self.schedulePanelListsLayout = QtGui.QHBoxLayout()
        self.schedulePanelLayout.addLayout(self.schedulePanelButtonsLayout)
        self.schedulePanelLayout.addLayout(self.schedulePanelListsLayout)
        self.scheduleCopyButton = QtGui.QPushButton('Copy\nSchedule')
        self.scheduleCopyButton.setFixedWidth(100)
        self.scheduleClearButton = QtGui.QPushButton('Clear\nHighlight')
        self.scheduleClearButton.setFixedWidth(100)
        self.scheduleListBox = QtGui.QTableWidget()
        self.scheduleListBox.setRowCount(len(self.schedule))
        self.scheduleListBox.setColumnCount(1)
        self.scheduleListBox.setHorizontalHeaderLabels(['WLD Code'])
        self.scheduleListBox.setColumnWidth(0,400)
        for i,val in enumerate(self.schedule):
            self.scheduleListBox.setItem(i,0,QtGui.QTableWidgetItem(str(val)))
        self.scheduleClearButton.released.connect(self.scheduleListBox.clearSelection)
        self.scheduleCopyButton.released.connect(lambda: self.copy_to_clipboard(self.schedule))
        self.schedulePanelButtonsLayout.addWidget(self.scheduleCopyButton)
        self.schedulePanelButtonsLayout.addWidget(self.scheduleClearButton)
        self.schedulePanelListsLayout.addWidget(self.scheduleListBox)
        self.schedulePanel.show()

    def copy_to_clipboard(self, item):
        if type(item) is list:
            tempstring = ''
            for val in item:
                tempstring += val+'\r\n'
            pyperclip.copy(tempstring[:-1])
        else:
            pyperclip.copy(str(item))

class signals(QtGui.QWidget):
    def __init__(self, bgcolor, fgcolor, number):
        super(signals, self).__init__()
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor
        self.number = number
        self.selectList = ['None Selected']
        self.isActive = True
        self.activeAxis = 1
        if self.number == 0:
            pass
        else:
            self.build_signals()
            self.build_plot_items()

    def build_signals(self):
        self.numberButton = QtGui.QPushButton(str(self.number)+':')
        self.signalSelect = QtGui.QComboBox()
        self.signalSelect.addItems(self.selectList)
        self.signalSelect.currentIndexChanged.connect(
            lambda: self.normalize_signal_boxes(self.signalSelect.currentIndex()))
        self.signalSelect.setMaxVisibleItems(22)
        self.signalValue = QtGui.QLabel()
        self.radio1 = QtGui.QRadioButton()
        self.radio2 = QtGui.QRadioButton()
        self.radio3 = QtGui.QRadioButton()
        self.radioGroup =QtGui.QButtonGroup()
        self.radioGroup.addButton(self.radio1,1)
        self.radioGroup.addButton(self.radio2,2)
        self.radioGroup.addButton(self.radio3,3)
        self.radio1.released.connect(lambda: self.normalize_axes(1))
        self.radio2.released.connect(lambda: self.normalize_axes(2))
        self.radio3.released.connect(lambda: self.normalize_axes(3))
        self.fileSelect = QtGui.QComboBox()
        self.fileSelect.currentIndexChanged.connect(self.change_file)


        self.numberButton.setStyleSheet('background-color: ' + str(self.bgcolor)+';'+
                                        'color: '+ str(self.fgcolor)+';')
        self.signalValue.setStyleSheet('border:1px solid grey')

        self.numberButton.released.connect(self.num_butt_toggle)

        self.numberButton.setFixedWidth(25)
        self.signalSelect.setFixedWidth(250)
        self.signalValue.setFixedWidth(100)
        self.radio1.setFixedWidth(20)
        self.radio2.setFixedWidth(20)
        self.radio3.setFixedWidth(20)
        self.fileSelect.setFixedWidth(40)

        self.numberButton.setFixedHeight(30)
        self.signalSelect.setFixedHeight(30)
        self.signalValue.setFixedHeight(30)
        self.radio1.setFixedHeight(30)
        self.radio2.setFixedHeight(30)
        self.radio3.setFixedHeight(30)
        self.fileSelect.setFixedHeight(30)

        self.radio1.setChecked(True)

        GUI.signalLayout.addWidget(self.numberButton,self.number+1,0)
        GUI.signalLayout.addWidget(self.signalSelect,self.number+1,1)
        GUI.signalLayout.addWidget(self.signalValue,self.number+1,2)
        GUI.signalLayout.addWidget(self.radio1,self.number+1,3)
        GUI.signalLayout.addWidget(self.radio2,self.number+1,4)
        GUI.signalLayout.addWidget(self.radio3,self.number+1,5)
        GUI.signalLayout.addWidget(self.fileSelect,self.number+1,6)

    def num_butt_toggle(self):
        if self.isActive == True:
            self.isActive = False
            self.numberButton.setStyleSheet('background-color: ' + 'grey' + ';' +
                                            'color: ' + 'light grey' + ';')
        else:
            self.isActive = True
            self.numberButton.setStyleSheet('background-color: ' + str(self.bgcolor) + ';' +
                                            'color: ' + str(self.fgcolor) + ';')
            plotFrame.build_plot()

    def change_file(self, index):
        if self.fileSelect.currentIndex() != index:
            self.fileSelect.setCurrentIndex(index)

        if self.fileCombo.currentIndex() != index:
            self.fileCombo.setCurrentIndex(index)

        if self.fileSelect.currentText() != '':
            self.selectList = openMaster[int(self.fileSelect.currentText())].signalList
            self.signalCombo.clear()
            self.signalSelect.clear()
            self.signalCombo.setParent(None)
            self.signalSelect.setParent(None)
            self.signalCombo.addItems(self.selectList)
            self.signalSelect.addItems(self.selectList)
            GUI.signalLayout.addWidget(self.signalSelect, self.number + 1, 1)
            GUI.leftPlotLayout.addWidget(self.signalCombo, 2 * self.number + 1, 0, 1, 4)

    def build_plot_items(self):
        #self.plotLayout = QtGui.QGridLayout()
        self.activeCheck = QtGui.QCheckBox(str(self.number))
        self.activeCheck.setChecked(True)
        self.activeCheck.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.activeCheck.stateChanged.connect(self.num_butt_toggle)
        self.fileCombo = QtGui.QComboBox()
        self.axisCombo = QtGui.QComboBox()
        self.axisCombo.addItems(['1','2','3'])
        self.axisCombo.currentIndexChanged.connect(lambda: self.normalize_axes(self.axisCombo.currentText()))
        self.signalCombo = QtGui.QComboBox()
        self.signalCombo.addItems(self.selectList)
        self.signalCombo.currentIndexChanged.connect(
            lambda: self.normalize_signal_boxes(self.signalCombo.currentIndex()))
        #self.signalCombo.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.signalCombo.setStyleSheet('background-color: ' + str(self.bgcolor)+';'+
                                       'color: '+ str(self.fgcolor)+';')
        self.plotLabel = QtGui.QLabel()
        #self.plotLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        #self.plotLabel.setStyleSheet('background-color: ' + str(self.bgcolor)+';'+'color: '+ str(self.fgcolor)+';')
        self.plotLabel.setStyleSheet('border:1px solid grey')

        self.activeCheck.setFixedWidth(30)
        self.fileCombo.setFixedWidth(40)
        self.axisCombo.setFixedWidth(40)
        self.signalCombo.setFixedWidth(250)
        self.plotLabel.setFixedWidth(120)

        self.activeCheck.setFixedHeight(25)
        self.fileCombo.setFixedHeight(25)
        self.axisCombo.setFixedHeight(25)
        self.signalCombo.setFixedHeight(25)
        self.plotLabel.setFixedHeight(25)


        GUI.leftPlotLayout.addWidget(self.activeCheck,2*self.number,0)
        GUI.leftPlotLayout.addWidget(self.fileCombo,2*self.number,1)
        GUI.leftPlotLayout.addWidget(self.axisCombo,2*self.number,2)
        GUI.leftPlotLayout.addWidget(self.plotLabel,2*self.number,3)
        GUI.leftPlotLayout.addWidget(self.signalCombo,2*self.number+1,0,1,4)

    def normalize_signal_boxes(self,index):
        if self.signalSelect.currentIndex() != index:
            self.signalSelect.setCurrentIndex(index)

        if self.signalCombo.currentIndex() != index:
            self.signalCombo.setCurrentIndex(index)

        plotFrame.build_plot()

    def normalize_axes(self, index):
        if self.radioGroup.checkedId() != index:
            if index == '1':
                self.radio1.setChecked(True)
            elif index == '2':
                self.radio2.setChecked(True)
            elif index == '3':
                self.radio3.setChecked(True)

        if self.axisCombo.currentText() != index:
            self.axisCombo.setCurrentIndex(index-1)

        plotFrame.build_plot()

class MatplotlibWidget(FigureCanvas):
    def __init__(self, parent=None):
        super(MatplotlibWidget, self).__init__(Figure())
        self.figure = plt.figure(tight_layout=True, dpi = 300, linewidth = 2)
        plt.rc('font', size=3)
        #https://matplotlib.org/users/customizing.html
        self.canvas = FigureCanvas(self.figure)


    def build_plot(self):
        if GUI.tabWidget.currentIndex() == 2:
            for val in openMaster:
                if isinstance(val, str) == False:
                    self.ax = self.figure.add_subplot(111, autoscale_on=True)
                    if val.fileName != '':
                        self.axUnoActive = False
                        self.axDosActive = False
                        self.axTresActive = False
                        for item in signalsMaster:
                            if isinstance(item, str) == False:
                                if item.radio1.isChecked() == True:
                                    self.axUnoActive = True
                                elif item.radio2.isChecked() == True:
                                    self.axDosActive = True
                                elif item.radio3.isChecked() == True:
                                    self.axTresActive = True
                            if self.axUnoActive == True and self.axDosActive == True and self.axTresActive == True:
                                break
                        if GUI.vertAutoCheck.isChecked() == True:
                            if self.axUnoActive == True:
                                GUI.vert_upper_auto_set(1)
                                GUI.vert_lower_auto_set(1)
                            if self.axDosActive == True:
                                GUI.vert_upper_auto_set(2)
                                GUI.vert_lower_auto_set(2)
                            if self.axTresActive == True:
                                GUI.vert_upper_auto_set(3)
                                GUI.vert_lower_auto_set(3)
                        if GUI.horizAutoCheck.isChecked() == True:
                            GUI.horiz_lower_auto_set()
                            GUI.horiz_upper_auto_set()
                        self.ax.set_xlim(float(GUI.horizLowerEntry.text()),float(GUI.horizUpperEntry.text()))
                        self.ax.set_ylim(float(GUI.vertUnoLowerEntry.text()),float(GUI.vertUnoUpperEntry.text()))
                        if self.axDosActive == True:
                            self.ax2 = self.ax.twinx()
                            self.ax.set_ylim(float(GUI.vertDosLowerEntry.text()), float(GUI.vertDosUpperEntry.text()))
                        if self.axTresActive == True:
                            self.ax3 = self.ax.twinx()
                            self.ax3.set_ylim(float(GUI.vertTresLowerEntry.text()), float(GUI.vertTresUpperEntry.text()))
                            self.ax3.spines["right"].set_position(('axes', 1.1))
                        for item in signalsMaster:
                            if isinstance(item, str) == False:
                                if item.signalSelect.currentText() != 'None Selected' and item.isActive == True:
                                    if item.radio1.isChecked() == True:
                                        if GUI.bottomRadio.isChecked() == True:
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
                                    elif item.radio2.isChecked() == True:
                                        if GUI.bottomRadio.isChecked() == True:
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
                                    elif item.radio3.isChecked() == True:
                                        if GUI.bottomRadio.isChecked() == True:
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
                        break
            self.ax.axhline(y=0, xmin=-10, xmax=10, c='black')
            self.canvas.draw()
            GUI.rightPlotLayout.addWidget(self.canvas)

app = QtGui.QApplication(sys.argv)
theme = QtGui.QApplication.setStyle('Plastique')
GUI = Window()


open1 = open_file(1)
open2 = open_file(2)
open3 = open_file(3)
open4 = open_file(4)
open5 = open_file(5)
open6 = open_file(6)
open7 = open_file(7)
open8 = open_file(8)
open9 = open_file(9)
open10 = open_file(10)
openMaster = ['blank', open1, open2, open3, open4, open5, open6, open7, open8, open9, open10]

signals1 = signals('#00008B', 'white',  1)
signals2 = signals('#000000', 'white',  2)
signals3 = signals('#8B008B', 'white',  3)
signals4 = signals('#006400', 'white',  4)
signals5 = signals('#8B4513', 'white',  5)
signals6 = signals('#FF69B4', 'black',  6)
signals7 = signals('#00FFFF', 'black',  7)
signals8 = signals('#BF3EFF', 'black',  8)
signals9 = signals('#7FFF00', 'black',  9)
signals10 = signals('#FFA500', 'black', 10)
signalsMaster = ['signalHeader', signals1, signals2, signals3, signals4, signals5, signals6, signals7, signals8, signals9, signals10]

plotFrame = MatplotlibWidget()
plotFrame.build_plot()
GUI.tabWidget.currentChanged.connect(plotFrame.build_plot)

sys.exit(app.exec_())
