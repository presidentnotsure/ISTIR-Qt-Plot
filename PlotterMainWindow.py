from PySide import QtGui, QtCore

#Creates and manages the main window for this program


class Window(QtGui.QWidget):
    def __init__(self, signals_master, open_master):
        super(Window, self).__init__()
        self.setGeometry(50, 50, 1366, 768)
        self.setWindowTitle("ISTIR Weld Data Plotter")
        self.setWindowIcon(QtGui.QIcon('par.ico'))
        self.signalsMaster = signals_master
        self.openMaster = open_master

        self.windowLayout = QtGui.QGridLayout(self)
        self.windowLayout.setContentsMargins(5, 5, 5, 5)
        self.setLayout(self.windowLayout)
        self.tabWidget = QtGui.QTabWidget(self)

        self.anyOpen = False
        self.open_tab()
        self.setup_tab()
        self.plot_tab()
        self.about_tab()

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
        self.openTabLayout.setContentsMargins(1, 1, 1, 1)
        self.tabWidget.addTab(self.openTab, "Open")

    def setup_tab(self):
        # setup tab options
        self.setupTab = QtGui.QWidget()
        self.setupTabLayout = QtGui.QGridLayout()
        self.setupTab.setLayout(self.setupTabLayout)
        self.setupTabLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.setupTabLayout.setContentsMargins(1, 1, 1, 1)

        # setup Signals area of tab
        self.signalLayout = QtGui.QGridLayout()
        self.signalLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.signalLayout.setContentsMargins(1, 1, 1, 1)
        self.setupTabLayout.addLayout(self.signalLayout, 0, 0)

        # setup Axes area of tab
        self.axesLayout = QtGui.QGridLayout()
        self.axesLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.axesLayout.setContentsMargins(1, 1, 1, 1)
        self.setupTabLayout.addLayout(self.axesLayout, 0, 1)

        # setup Copy area of tab
        self.copyLayout = QtGui.QHBoxLayout()
        self.copyLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.copyLayout.setContentsMargins(1, 1, 1, 1)
        # self.copyLayout.setFixedWidth(350)
        self.setupTabLayout.addLayout(self.copyLayout, 1, 0)

        # setup Generate area of tab
        self.generateLayout = QtGui.QGridLayout()
        self.generateLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.generateLayout.setContentsMargins(1, 1, 1, 1)
        self.setupTabLayout.addLayout(self.generateLayout, 2, 0, 1, 2)

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

        self.signalLayout.addWidget(self.chooseLabel, 0, 1, 2, 1)
        self.signalLayout.addWidget(self.valueLabel, 0, 2, 2, 1)
        self.signalLayout.addWidget(self.vertLabel, 0, 3, 1, 3)
        self.signalLayout.addWidget(self.unoLabel, 1, 3, 1, 1)
        self.signalLayout.addWidget(self.dosLabel, 1, 4, 1, 1)
        self.signalLayout.addWidget(self.tresLabel, 1, 5, 1, 1)
        self.signalLayout.addWidget(self.fileLabel, 0, 6, 2, 1)

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

        self.axesLayout.addWidget(self.vertLabel, 0, 1, 1, 4)
        self.axesLayout.addWidget(self.vertAutoLabel, 1, 0)
        self.axesLayout.addWidget(self.vertAutoCheck, 1, 1)
        self.axesLayout.addWidget(self.vertLowerLabel, 1, 2)
        self.axesLayout.addWidget(self.vertUpperLabel, 1, 3)
        self.axesLayout.addWidget(self.vertUnoLabel, 2, 0)
        self.axesLayout.addWidget(self.vertDosLabel, 3, 0)
        self.axesLayout.addWidget(self.vertTresLabel, 4, 0)
        self.axesLayout.addWidget(self.vertUnoLowerButton, 2, 1)
        self.axesLayout.addWidget(self.vertDosLowerButton, 3, 1)
        self.axesLayout.addWidget(self.vertTresLowerButton, 4, 1)
        self.axesLayout.addWidget(self.vertUnoLowerEntry, 2, 2)
        self.axesLayout.addWidget(self.vertDosLowerEntry, 3, 2)
        self.axesLayout.addWidget(self.vertTresLowerEntry, 4, 2)
        self.axesLayout.addWidget(self.vertUnoUpperEntry, 2, 3)
        self.axesLayout.addWidget(self.vertDosUpperEntry, 3, 3)
        self.axesLayout.addWidget(self.vertTresUpperEntry, 4, 3)
        self.axesLayout.addWidget(self.vertUnoUpperButton, 2, 4)
        self.axesLayout.addWidget(self.vertDosUpperButton, 3, 4)
        self.axesLayout.addWidget(self.vertTresUpperButton, 4, 4)
        self.axesLayout.addWidget(self.vertSpace, 5, 1)

        self.axesLayout.addWidget(self.horizLabel, 6, 1, 1, 4)
        self.axesLayout.addWidget(self.horizAutoLabel, 7, 0)
        self.axesLayout.addWidget(self.horizAutoCheck, 7, 1)
        self.axesLayout.addWidget(self.horizLowerLabel, 7, 2)
        self.axesLayout.addWidget(self.horizUpperLabel, 7, 3)
        self.axesLayout.addWidget(self.horizLowerButton, 8, 1)
        self.axesLayout.addWidget(self.horizLowerEntry, 8, 2)
        self.axesLayout.addWidget(self.horizUpperEntry, 8, 3)
        self.axesLayout.addWidget(self.horizUpperButton, 8, 4)

        self.axesLayout.addWidget(self.typeLabel, 10, 1, 2, 2)
        self.axesLayout.addWidget(self.topRadio, 10, 3)
        # self.axesLayout.addWidget(self.bottomRadio,11,3)
        self.axesLayout.addWidget(self.horizSpace, 12, 1)

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

        self.generateLayout.addWidget(self.sourceLabel, 0, 0)
        self.generateLayout.addWidget(self.firstLabel, 0, 4)
        self.generateLayout.addWidget(self.secondLabel, 0, 8)
        self.generateLayout.addWidget(self.fileSelect, 1, 0)
        self.generateLayout.addWidget(self.spaceLabel, 1, 1)
        self.generateLayout.addWidget(self.firstEntry, 1, 2)
        self.generateLayout.addWidget(self.timesLabel, 1, 3)
        self.generateLayout.addWidget(self.firstBox, 1, 4)
        self.generateLayout.addWidget(self.addLabel, 1, 5)
        self.generateLayout.addWidget(self.secondEntry, 1, 6)
        self.generateLayout.addWidget(self.multiLabel, 1, 7)
        self.generateLayout.addWidget(self.secondBox, 1, 8)
        self.generateLayout.addWidget(self.equalsLabel, 1, 9)
        self.generateLayout.addWidget(self.nameLabel, 2, 0, 1, 4)
        self.generateLayout.addWidget(self.nameEntry, 2, 4)
        self.generateLayout.addWidget(self.generateButton, 0, 10, 3, 1)

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
        # setup main plot area
        self.plotTab = QtGui.QWidget()
        self.plotTabLayout = QtGui.QGridLayout()
        self.plotTab.setLayout(self.plotTabLayout)
        self.plotTabLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignTop)
        self.plotTabLayout.setContentsMargins(1, 1, 1, 1)

        # setup left plot area
        self.leftPlotLayout = QtGui.QGridLayout()
        self.plotTabLayout.addLayout(self.leftPlotLayout, 0, 0, 2, 1)

        # setup right plot area
        self.rightPlotLayout = QtGui.QGridLayout()
        self.plotTabLayout.addLayout(self.rightPlotLayout, 0, 1)
        # self.plotHolder = QtGui.QLineEdit()
        # self.plotHolder.setFixedWidth(700)
        # self.plotHolder.setFixedHeight(700)
        # self.rightPlotLayout.addWidget(self.plotHolder)

        # setup horizontal axis area
        self.bottomLPlotLayout = QtGui.QHBoxLayout()
        self.plotTabLayout.addLayout(self.bottomLPlotLayout, 1, 1)
        self.bottomLPlotLayout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)

        self.bottomCPlotLayout = QtGui.QHBoxLayout()
        self.plotTabLayout.addLayout(self.bottomCPlotLayout, 1, 1)
        self.bottomCPlotLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

        self.tabWidget.addTab(self.plotTab, "Plot")

    def print_screen(self):
        self.prntScrnLayout = QtGui.QHBoxLayout()
        self.prntScrnButton = QtGui.QPushButton('Print Screen')
        self.saveScrnButton = QtGui.QPushButton('Save Screen')
        self.prntScrnLayout.addWidget(self.prntScrnButton)
        self.prntScrnLayout.addWidget(self.saveScrnButton)
        self.prntScrnLayout.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignTop)
        self.leftPlotLayout.addLayout(self.prntScrnLayout, 22, 0, 1, 4)

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

        self.leftPlotLayout.addWidget(self.plotActiveLabel, 0, 0)
        self.leftPlotLayout.addWidget(self.plotFileLabel, 0, 1)
        self.leftPlotLayout.addWidget(self.plotAxisLabel, 0, 2)
        self.leftPlotLayout.addWidget(self.plotValueLabel, 0, 3)
        self.leftPlotLayout.addWidget(self.plotSignalLabel, 1, 0, 1, 4)

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

    def add_active_files(self, input_file):
        if str(input_file) not in self.fileActiveList:
            self.fileActiveList.append(str(input_file))
            self.fileActiveList.sort()
            for item in self.signalsMaster:
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

    def remove_active_files(self, input_file):
        if str(input_file) in self.fileActiveList:
            self.fileActiveList.remove(str(input_file))
            self.fileActiveList.sort()
            for item in self.signalsMaster:
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
        for item in self.signalsMaster:
            if not isinstance(item, str):
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
        min_list = []
        max_list = []
        if self.bottomRadio.isChecked():
            for i, val in enumerate(self.openMaster):
                if not isinstance(val, str) and val.fileName != '':
                    min_list.append(min(val.signalDict['plotDist']))
                    max_list.append(max(val.signalDict['plotDist']))
        else:
            for i, val in enumerate(self.openMaster):
                if not isinstance(val, str) and val.fileName != '':
                    min_list.append(min(val.signalDict['plotTime']))
                    max_list.append(max(val.signalDict['plotTime']))

        if not min_list:
            min_list = [0.0]
        self.horizLowerEntry.setText(str(min(min_list)))

    def horiz_upper_auto_set(self):
        max_list = []
        if self.bottomRadio.isChecked():
            for i, val in enumerate(self.openMaster):
                if not isinstance(val, str) and val.fileName != '':
                    max_list.append(max(val.signalDict['plotDist']))
        else:
            for i, val in enumerate(self.openMaster):
                if not isinstance(val, str) and val.fileName != '':
                    max_list.append(max(val.signalDict['plotTime']))
        if not max_list:
            max_list = [1.0]
        self.horizUpperEntry.setText(str(max(max_list)))

    def vert_lower_auto_set(self, input_axis):
        min_list = []
        for item in self.signalsMaster:
            if not isinstance(item, str):
                if item.fileSelect.currentText() != '':
                    file = int(item.fileSelect.currentText())
                    signal = item.signalSelect.currentText()
                    if item.radio1.isChecked() and input_axis == 1:
                        min_list.append(min(self.openMaster[file].signalDict[signal]))
                    elif item.radio2.isChecked() and input_axis == 2:
                        min_list.append(min(self.openMaster[file].signalDict[signal]))
                    elif item.radio3.isChecked() and input_axis == 3:
                        min_list.append(min(self.openMaster[file].signalDict[signal]))

        if not min_list:
            min_list = [0.0]

        if input_axis == 1:
            self.vertUnoLowerEntry.setText(str(min(min_list)))
        elif input_axis == 2:
            self.vertDosLowerEntry.setText(str(min(min_list)))
        elif input_axis == 3:
            self.vertTresLowerEntry.setText(str(min(min_list)))

    def vert_upper_auto_set(self, input_axis):
        max_list = []
        for item in self.signalsMaster:
            if not isinstance(item, str):
                if item.fileSelect.currentText() != '':
                    file = int(item.fileSelect.currentText())
                    signal = item.signalSelect.currentText()
                    if item.radio1.isChecked() and input_axis == 1:
                        max_list.append(max(self.openMaster[file].signalDict[signal]))
                    elif item.radio2.isChecked() and input_axis == 2:
                        max_list.append(min(self.openMaster[file].signalDict[signal]))
                    elif item.radio3.isChecked() and input_axis == 3:
                        max_list.append(min(self.openMaster[file].signalDict[signal]))

        if not max_list:
            max_list = [1.0]

        if input_axis == 1:
            self.vertUnoUpperEntry.setText(str(max(max_list)))
        elif input_axis == 2:
            self.vertDosUpperEntry.setText(str(max(max_list)))
        elif input_axis == 3:
            self.vertTresUpperEntry.setText(str(max(max_list)))

    def pad_axes(self, *input_set):
        lower_axes = [self.horizLowerEntry, self.vertUnoLowerEntry, self.vertDosLowerEntry, self.vertTresLowerEntry]
        upper_axes = [self.horizUpperEntry, self.vertUnoUpperEntry, self.vertDosUpperEntry, self.vertTresUpperEntry]
        if len(input_set) > 0:
            if input_set[0] == 'horiz':
                spanmin = 0
                spanmax = 1
            elif input_set[0] == 'all':
                spanmin = 0
                spanmax = 4
        else:
            spanmin = 1
            spanmax = 4
        for i in range(spanmin, spanmax):
            if not lower_axes[i].text() == '0.0' and not upper_axes[i].text() == '1.0':
                if lower_axes[i].text() == upper_axes[i].text():
                    if float(lower_axes[i].text()) > 0:
                        lower_axes[i].setText(str(0.9 * float(lower_axes[i].text())))
                        upper_axes[i].setText(str(1.1 * float(upper_axes[i].text())))
                    elif float(lower_axes[i].text()) < 0:
                        lower_axes[i].setText(str(1.1 * float(lower_axes[i].text())))
                        upper_axes[i].setText(str(0.9 * float(upper_axes[i].text())))
                    else:
                        lower_axes[i].setText('0.0')
                        upper_axes[i].setText('1.0')
                else:
                    upper_axes[i].setText(str(float(upper_axes[i].text()) +
                                              0.1 * (float(upper_axes[i].text()) -
                                                     float(lower_axes[i].text()))))
                    lower_axes[i].setText(str(float(lower_axes[i].text()) -
                                              0.1 * (float(upper_axes[i].text()) -
                                                     float(lower_axes[i].text()))))
