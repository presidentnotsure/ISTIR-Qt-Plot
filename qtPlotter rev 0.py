import sys
from PySide import QtGui, QtCore
import numpy as np

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
        self.open_tab()
        self.setup_tab()
        self.plot_tab()
        self.about_tab()

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
        self.vertLabel = QtGui.QLabel("Define Vertical Axes' Values")
        self.vertAutoLabel = QtGui.QLabel('Auto')
        self.vertAutoCheck = QtGui.QCheckBox()
        self.vertLowerLabel = QtGui.QLabel('Lower')
        self.vertUpperLabel = QtGui.QLabel('Upper')
        self.vertUnoLabel = QtGui.QLabel('1:')
        self.vertDosLabel = QtGui.QLabel('2:')
        self.vertTresLabel = QtGui.QLabel('3:')
        self.vertUnoLowerButton = QtGui.QPushButton('◄')
        self.vertDosLowerButton = QtGui.QPushButton('◄')
        self.vertTresLowerButton = QtGui.QPushButton('◄')
        self.vertUnoLowerEntry = QtGui.QLineEdit()
        self.vertDosLowerEntry = QtGui.QLineEdit()
        self.vertTresLowerEntry = QtGui.QLineEdit()
        self.vertUnoUpperEntry = QtGui.QLineEdit()
        self.vertDosUpperEntry = QtGui.QLineEdit()
        self.vertTresUpperEntry = QtGui.QLineEdit()
        self.vertUnoUpperButton = QtGui.QPushButton('►')
        self.vertDosUpperButton = QtGui.QPushButton('►')
        self.vertTresUpperButton = QtGui.QPushButton('►')
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
        self.horizLowerLabel = QtGui.QLabel('Lower')
        self.horizUpperLabel = QtGui.QLabel('Upper')
        self.horizLowerButton = QtGui.QPushButton('◄')
        self.horizLowerEntry = QtGui.QLineEdit()
        self.horizUpperEntry = QtGui.QLineEdit()
        self.horizUpperButton = QtGui.QPushButton('►')
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
        self.topRadio = QtGui.QRadioButton('Time')
        self.bottomRadio = QtGui.QRadioButton('Time')

        self.typeLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

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
        self.axesLayout.addWidget(self.bottomRadio,11,3)
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
        self.rightPlotLayout = QtGui.QVBoxLayout()
        self.plotTabLayout.addLayout(self.rightPlotLayout,0,1)
        self.plotHolder = QtGui.QLineEdit()
        #self.plotHolder.setFixedWidth(700)
        #self.plotHolder.setFixedHeight(700)
        self.rightPlotLayout.addWidget(self.plotHolder)
        

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


class open_file(QtGui.QWidget):
    def __init__(self,number):
        super(open_file, self).__init__()
        self.number = number
        self.fileName = 'Test.dat'
        self.fileNameShort = ''
        self.offset  = 0.0
        self.xListOffset = []
        self.schedule = []
        self.header = []
        self.weldDistance = []
        self.timeList = []
        self.signalDict = {}
        self.signalList = []

        self.openLayout = QtGui.QGridLayout()
        self.setLayout(self.openLayout)

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
        self.openIndex = QtGui.QLabel(str(self.number))
        self.radioSelect = QtGui.QRadioButton()
        self.openButton = QtGui.QPushButton('Open File')
        self.openButton.released.connect(self.file_grab)
        self.headerButton = QtGui.QPushButton('Read Header')
        self.scheduleButton = QtGui.QPushButton('Read WLD Program')
        self.clearButton = QtGui.QPushButton('Clear')
        self.fileLabel = QtGui.QLabel(self.fileName)
        self.offsetLabel = QtGui.QLabel('Horizontal Offset')
        self.offsetEntry = QtGui.QLineEdit(str(self.offset))

        self.openIndex.setFixedWidth(15)
        self.radioSelect.setFixedWidth(15)
        self.openButton.setFixedHeight(30)
        self.headerButton.setFixedHeight(30)
        self.scheduleButton.setFixedHeight(30)
        self.clearButton.setFixedWidth(40)
        self.clearButton.setFixedHeight(30)
        self.fileLabel.setFixedHeight(30)
        self.offsetLabel.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)
        self.offsetLabel.setFixedHeight(30)
        self.offsetEntry.setFixedWidth(150)
        self.offsetEntry.setFixedHeight(30)

        self.openLayout.addWidget(self.openIndex,0,0,1,1)
        self.openLayout.addWidget(self.radioSelect,0,1,1,1)
        self.openLayout.addWidget(self.openButton,0,2,1,1)
        self.openLayout.addWidget(self.headerButton,0,3,1,1)
        self.openLayout.addWidget(self.scheduleButton,0,4,1,1)
        self.openLayout.addWidget(self.clearButton,1,0,1,2)
        self.openLayout.addWidget(self.fileLabel,1,2,1,3)
        self.openLayout.addWidget(self.offsetLabel,2,2,1,1)
        self.openLayout.addWidget(self.offsetEntry,2,3,1,2)
        self.openLayout.addWidget(self.bottomSpace,3,0,1,1)

    def initial_read(self):
        with open(self.fileName,'r') as self.f:
            for line in self.f:
                self.header.append(line.strip())
                if line.strip() == 'Weld Program Listing:' or 'START OF WELD PROGRAM LISTING' in line:
                    self.header.pop()
                    self.weld_data_read()
                    break
                elif 'Sample Rate :' in line:
                    self.header = []
                    self.samplerate = float(line.split(' ')[3])
                    self.data_recoder_read()
                    break
                    
    def data_recoder_read(self):
        for line in self.f:
            if str.isdigit(line[0]) == True or line[0] == '-':
                break
            else:
                self.signalList.append(line.strip())

        for line in self.f:
            for i,val in enumerate(line.strip().split(',')):
                try:
                    self.signalDict[self.signalList[i]].append(val)
                except:
                    self.signalDict[self.signalList[i]] = [val]

        for i,val in enumerate(self.signalList):
            self.signalDict[val] = np.asanyarray(self.signalDict[val])
            

    def weld_data_read(self):
        self.f.readline()
        for line in self.f:
            if line.strip() == 'Data' or 'Data:' in line or '=====' in line:
                break
            self.schedule.append(line.strip())

        for line in self.f:
                if 'Sample Rate :' in line:
                    self.samplerate = float(line.split(' ')[3])
                    self.data_recoder_read()
                    break

    def file_grab(self):
        self.fileDialog = QtGui.QWidget()
        #self.fileDialog.resize(320, 240)
        self.fileNameOld = self.fileName

        try:
            self.fileName = QtGui.QFileDialog.getOpenFileName(self.fileDialog, 'Open File', '/')[0]
        except:
            pass

        if self.fileName != self.fileNameOld:
            self.initial_read()

        elif self.fileName == '' and self.fileNameOld != '':
            self.fileName = self.fileNameOld

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
        self.schedulePanelLayout = QtGui.QVBoxLayout()
        self.schedulePanel.setLayout(self.schedulePanelLayout)
        self.schedulePanel.setWindowTitle('File '+str(self.number)+' Weld Schedule')

        self.scheduleListBox = QtGui.QListWidget()
        #self.scheduleListBox = QtGui.QListView

        for item in self.schedule:
            self.scheduleListBox.addItem(item)

        self.scheduleListBox.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
    
        
        #self.scheduleListBox = QtGui.QLabel(self.scheduleText)
        #self.scheduleLabel.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.schedulePanelLayout.addWidget(self.scheduleListBox)
        self.schedulePanel.show()

class signals(QtGui.QWidget):
    def __init__(self, bgcolor, fgcolor, number):
        super(signals, self).__init__()       
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor
        self.number = number
        self.selectList = ['None Selected']
        self.isActive = False
        self.activeFile = 1
        self.activeAxis = 1

        if self.number == 0:
            pass
        else:
            self.build_signals()
            self.build_plot()

    def build_signals(self):
        self.numberButton = QtGui.QPushButton(str(self.number)+':')
        self.signalSelect = QtGui.QComboBox()
        self.signalValue = QtGui.QLabel()
        self.radio1 = QtGui.QRadioButton()
        self.radio2 = QtGui.QRadioButton()
        self.radio3 = QtGui.QRadioButton()
        self.fileSelect = QtGui.QComboBox()

        self.numberButton.setStyleSheet('background-color: ' + str(self.bgcolor)+';'+
                                        'color: '+ str(self.fgcolor)+';')
        self.signalValue.setStyleSheet('border:1px solid grey')       
        

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

        GUI.signalLayout.addWidget(self.numberButton,self.number+1,0)
        GUI.signalLayout.addWidget(self.signalSelect,self.number+1,1)
        GUI.signalLayout.addWidget(self.signalValue,self.number+1,2)
        GUI.signalLayout.addWidget(self.radio1,self.number+1,3)
        GUI.signalLayout.addWidget(self.radio2,self.number+1,4)
        GUI.signalLayout.addWidget(self.radio3,self.number+1,5)
        GUI.signalLayout.addWidget(self.fileSelect,self.number+1,6)

    def build_plot(self):
        #self.plotLayout = QtGui.QGridLayout()
        self.activeCheck = QtGui.QCheckBox(str(self.number))
        self.activeCheck.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.fileCombo = QtGui.QComboBox()
        #self.fileCombo.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        #self.fileCombo.setStyleSheet('background-color: ' + str(self.bgcolor)+';'+'color: '+ str(self.fgcolor)+';')
        self.axisCombo = QtGui.QComboBox()
        #self.axisCombo.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        #self.axisCombo.setStyleSheet('background-color: ' + str(self.bgcolor)+';'+'color: '+ str(self.fgcolor)+';')
        self.signalCombo = QtGui.QComboBox()
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

sys.exit(app.exec_())
