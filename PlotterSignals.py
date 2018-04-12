from PySide import QtGui, QtCore

#Creates and manages the signal elements


class Signals(QtGui.QWidget):
    def __init__(self, bgcolor, fgcolor, number, main_window):
        super(Signals, self).__init__()
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor
        self.number = number
        self.main_window = main_window
        self.selectList = ['None Selected']
        self.isActive = True
        self.activeAxis = 1
        if self.number == 0:
            pass
        else:
            self.build_signals()
            self.build_plot_items()

    def build_signals(self):
        self.numberButton = QtGui.QPushButton(str(self.number) + ':')
        self.signalSelect = QtGui.QComboBox()
        self.signalSelect.addItems(self.selectList)
        self.signalSelect.currentIndexChanged.connect(
            lambda: self.normalize_signal_boxes(self.signalSelect.currentIndex()))
        self.signalSelect.setMaxVisibleItems(22)
        self.signalValue = QtGui.QLabel()
        self.radio1 = QtGui.QRadioButton()
        self.radio2 = QtGui.QRadioButton()
        self.radio3 = QtGui.QRadioButton()
        self.radioGroup = QtGui.QButtonGroup()
        self.radioGroup.addButton(self.radio1, 1)
        self.radioGroup.addButton(self.radio2, 2)
        self.radioGroup.addButton(self.radio3, 3)
        self.radio1.released.connect(lambda: self.normalize_axes(1))
        self.radio2.released.connect(lambda: self.normalize_axes(2))
        self.radio3.released.connect(lambda: self.normalize_axes(3))
        self.fileSelect = QtGui.QComboBox()
        self.fileSelect.currentIndexChanged.connect(self.change_file)

        self.numberButton.setStyleSheet('background-color: ' + str(self.bgcolor) + ';' +
                                        'color: ' + str(self.fgcolor) + ';')
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

        self.main_window.signalLayout.addWidget(self.numberButton, self.number + 1, 0)
        self.main_window.signalLayout.addWidget(self.signalSelect, self.number + 1, 1)
        self.main_window.signalLayout.addWidget(self.signalValue, self.number + 1, 2)
        self.main_window.signalLayout.addWidget(self.radio1, self.number + 1, 3)
        self.main_window.signalLayout.addWidget(self.radio2, self.number + 1, 4)
        self.main_window.signalLayout.addWidget(self.radio3, self.number + 1, 5)
        self.main_window.signalLayout.addWidget(self.fileSelect, self.number + 1, 6)

    def num_butt_toggle(self):
        if self.isActive:
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
            self.main_window.signalLayout.addWidget(self.signalSelect, self.number + 1, 1)
            self.main_window.leftPlotLayout.addWidget(self.signalCombo, 2 * self.number + 1, 0, 1, 4)

    def build_plot_items(self):
        # self.plotLayout = QtGui.QGridLayout()
        self.activeCheck = QtGui.QCheckBox(str(self.number))
        self.activeCheck.setChecked(True)
        self.activeCheck.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.activeCheck.stateChanged.connect(self.num_butt_toggle)
        self.fileCombo = QtGui.QComboBox()
        self.axisCombo = QtGui.QComboBox()
        self.axisCombo.addItems(['1', '2', '3'])
        self.axisCombo.currentIndexChanged.connect(lambda: self.normalize_axes(self.axisCombo.currentText()))
        self.signalCombo = QtGui.QComboBox()
        self.signalCombo.addItems(self.selectList)
        self.signalCombo.currentIndexChanged.connect(
            lambda: self.normalize_signal_boxes(self.signalCombo.currentIndex()))
        # self.signalCombo.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.signalCombo.setStyleSheet('background-color: ' + str(self.bgcolor) + ';' +
                                       'color: ' + str(self.fgcolor) + ';')
        self.plotLabel = QtGui.QLabel()
        # self.plotLabel.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        # self.plotLabel.setStyleSheet('background-color: ' + str(self.bgcolor)+';'+'color: '+ str(self.fgcolor)+';')
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

        self.main_window.leftPlotLayout.addWidget(self.activeCheck, 2 * self.number, 0)
        self.main_window.leftPlotLayout.addWidget(self.fileCombo, 2 * self.number, 1)
        self.main_window.leftPlotLayout.addWidget(self.axisCombo, 2 * self.number, 2)
        self.main_window.leftPlotLayout.addWidget(self.plotLabel, 2 * self.number, 3)
        self.main_window.leftPlotLayout.addWidget(self.signalCombo, 2 * self.number + 1, 0, 1, 4)

    def normalize_signal_boxes(self, index):
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
            self.axisCombo.setCurrentIndex(index - 1)

        plotFrame.build_plot()
