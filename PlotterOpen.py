from PySide import QtGui, QtCore
import numpy as np

# Contains the class to give the GUI the ability to open files


class OpenFile(QtGui.QFrame):
    def __init__(self, number, main_window):
        super(OpenFile, self).__init__()
        self.number = number
        self.main_window = main_window
        self.isActive = False
        self.fileName = ''
        self.offset = 0.0
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

        self.main_window.openTabLayout.addWidget(self, self.openRow, self.openCol)

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
        self.openIndex = QtGui.QLabel('   ' + str(self.number))
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

        # self.fileLabel.setAlignment(QtCore.Qt.AlignBottom | QtCore.Qt.RightToLeft | QtCore.Qt.AlignJustify)
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

        self.openLayout.addWidget(self.openIndex, 0, 0, 1, 2)
        # self.openLayout.addWidget(self.radioSelect,0,1,1,1)
        self.openLayout.addWidget(self.openButton, 0, 2, 1, 1)
        # self.openLayout.addWidget(self.headerButton,0,3,1,1)
        # self.openLayout.addWidget(self.scheduleButton,0,4,1,1)
        self.openLayout.addWidget(self.clearButton, 1, 0, 1, 2)
        self.openLayout.addWidget(self.fileLabel, 1, 2, 1, 4)
        self.openLayout.addWidget(self.offsetLabel, 2, 2, 1, 1)
        self.openLayout.addWidget(self.offsetEntry, 2, 3, 1, 3)
        # self.openLayout.addWidget(self.bottomSpace,3,0,1,1)

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
        self.fileDialog = QtGui.QFileDialog()
        self.fileNameOld = self.fileName
        try:
            self.fileName = QtGui.QFileDialog.getOpenFileName(self.fileDialog, 'Open File', '/')[0]
        except NameError:
            pass
        if self.fileName == '':
            self.fileName = self.fileNameOld
        elif self.fileName != self.fileNameOld:
            self.fileLabel.setText(self.fileName)
            self.isActive = True
            self.initial_read()

    def initial_read(self):
        with open(self.fileName, 'r') as self.f:
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
            if str.isdigit(line[0]) or line[0] == '-':
                self.signalDict['None Selected'].append(0.0)
                for i, val in enumerate(line.strip().split(',')):
                    try:
                        self.signalDict[self.signalList[i]].append(float(val))
                    except NameError:
                        self.signalDict[self.signalList[i]] = [float(val)]
            else:
                self.signalList.append(line.strip())
        self.signalDict['Weld Time, sec'] = []
        for i, val in enumerate(self.signalDict['None Selected']):
            self.signalDict['Weld Time, sec'].append(float(i) / self.sampleRate)
        for i, val in enumerate(self.signalDict.keys()):
            self.signalDict[val] = np.asanyarray(self.signalDict[val])
        self.signalList.insert(0, 'None Selected')
        self.signalDict['plotTime'] = self.signalDict['Weld Time, sec']
        if 'Weld Distance, in' in self.signalList:
            self.signalDict['plotDist'] = self.signalDict['Weld Distance, in']
        if 'Weld Distance, mm' in self.signalList:
            self.signalDict['plotDist'] = self.signalDict['Weld Distance, mm']

        # print(len(self.signalDict['plotTime']))
        # print(len(self.signalDict['Weld Time, sec']))
        # print(len(self.signalDict['None Selected']))
        # print(len(self.signalDict[self.signalList[12]]))
        self.main_window.add_active_files(self.number)

    def weld_data_read(self):
        self.f.readline()
        for line in self.f:
            if line.strip() == 'Data' or 'Data:' in line or '=====' in line:
                break
            self.schedule.append(line.strip())

        for i in range(len(self.schedule) - 1, 0, -1):
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
        self.offset = 0.0
        self.schedule = []
        self.header = []
        self.signalDict = {}
        self.signalList = []
        self.fileLabel.setText(self.fileName)
        self.headerButton.setParent(None)
        self.scheduleButton.setParent(None)
        self.main_window.remove_active_files(str(self.number))

    def disp_header(self):
        self.headerPanel = QtGui.QWidget()
        self.headerPanelLayout = QtGui.QVBoxLayout()
        self.headerPanel.setLayout(self.headerPanelLayout)
        self.headerPanel.setWindowTitle('File ' + str(self.number) + ' Header Info')
        self.headerText = ''
        for item in self.header:
            self.headerText += item + '\n'
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
        self.scheduleListBox.setColumnWidth(0, 400)
        for i, val in enumerate(self.schedule):
            self.scheduleListBox.setItem(i, 0, QtGui.QTableWidgetItem(str(val)))
        self.scheduleClearButton.released.connect(self.scheduleListBox.clearSelection)
        self.scheduleCopyButton.released.connect(lambda: self.copy_to_clipboard(self.schedule))
        self.schedulePanelButtonsLayout.addWidget(self.scheduleCopyButton)
        self.schedulePanelButtonsLayout.addWidget(self.scheduleClearButton)
        self.schedulePanelListsLayout.addWidget(self.scheduleListBox)
        self.schedulePanel.show()

    def copy_to_clipboard(self, item):
        #  self.fileName to make it non-static eligible
        if type(item) is list and self.fileName:
            tempstring = ''
            for val in item:
                tempstring += val + '\r\n'
            pyperclip.copy(tempstring[:-1])
        else:
            pyperclip.copy(str(item))
