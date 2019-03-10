# LabViewData1
# Latest: 3/2019

import os

import sys
import numpy as np
import csv
import pyqtgraph
from PyQt5 import QtWidgets, uic

class LDApp(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_LD = uic.loadUiType("LabViewData.ui")[0]
        self.ui = Ui_LD()
        self.ui.setupUi(self)

        # Signals to slots
        self.ui.actionOpen.triggered.connect(self.FileDialog)
        self.ui.actionExit.triggered.connect(self.close)
        self.ui.actionScreenshot.triggered.connect(self.Screenshot)

        # Set up plotting widgets
        self.xData = self.ui.xData.addPlot()
        self.yData = self.ui.yData.addPlot()
        self.zData = self.ui.zData.addPlot()

        # Data categories established by Tomi's software
        self.t = []
        self.xsetpoint = []
        self.ysetpoint = []
        self.zsetpoint = []
        self.x = []
        self.y = []
        self.z = []

    # Open File Dialog
    def FileDialog(self):
        # Data categories established by Tomi's software
        self.t.clear()
        self.xsetpoint.clear()
        self.ysetpoint.clear()
        self.zsetpoint.clear()
        self.x.clear()
        self.y.clear()
        self.z.clear()
        self.xData.clear()
        self.yData.clear()
        self.zData.clear()
        self.filename = QtWidgets.QFileDialog.getOpenFileName(self,
                                                              'Open file',
                                                              'C:\\Users\\User\\Desktop\\Demonpore\\Data',
                                                              "Data Files (*.csv)")[0]
        self.setWindowTitle(os.path.split(self.filename)[1])
        self.DataFile = csv.reader(open(self.filename))
        next(self.DataFile, None) # Skip header, then read data
        n = 0
        for row in self.DataFile:
            self.t.append(n)
            n = n + 10
            self.xsetpoint.append(float(row[1])*5/65535)
            self.ysetpoint.append(float(row[2])*5/65535)
            self.zsetpoint.append(float(row[3])*5/65535)
            self.x.append(float(row[4])*5/65535)
            self.y.append(float(row[5])*5/65535)
            self.z.append(float(row[6])*5/65535)
        self.n = len(self.t)

        # Scaling, Offsets etc.
        self.timeoffset = 0
        self.xscale = []
        self.yscale = []
        self.xmin = []
        self.ymin = []
        self.xcounter = 0
        self.ycounter = 0

 #       self.Calibrate()
        self.Plot()

    def Calibrate(self):
        for i in range(self.n):
            if self.xsetpoint[i] == 0 and self.xcounter >= self.timeoffset and self.xcounter <= 2 * self.timeoffset:
                self.xcounter = self.xcounter + 1
                self.xmin.append(self.x[i])
                self.xscale.append(1)  # In case no x values are being set
            elif self.xsetpoint[i] != 0 and self.xcounter >= self.timeoffset and self.xcounter <= 2 * self.timeoffset:
                self.xcounter - self.xcounter + 1
                self.xscale.append(self.xsetpoint[i].real / self.x[i].real)
            else:
                self.xcounter = 0
            if self.ysetpoint[i] == 0 and self.ycounter >= self.timeoffset and self.ycounter <= 2 * self.timeoffset:
                self.ycounter = self.ycounter + 1
                self.ymin.append(self.y[i])
                self.yscale.append(1)  # In case no y values are being set
            elif self.ysetpoint[i] != 0 and self.ycounter >= self.timeoffset and self.ycounter <= 2 * self.timeoffset:
                self.ycounter = self.ycounter + 1
                self.yscale.append(self.ysetpoint[i].real / self.y[i].real)
            else:
                self.ycounter = 0

        for i in range(self.n):
            self.x[i] = (self.x[i] - np.average(self.xmin)) * np.average(self.xscale)
            self.y[i] = (self.y[i] - np.average(self.ymin)) * np.average(self.xscale)

        print("Average minimum of x = " + str(np.average(self.xmin)))
        print("Average scale of x position = " + str(np.average(self.xscale)))
        print("Average minimum of y = " + str(np.average(self.ymin)))
        print("Average scale of y position = " + str(np.average(self.yscale)))

    def Plot(self):

        # x-axis Data
        self.xData.addLegend()
        self.xData.plot(self.t, self.x, pen=(0, 127, 255), linewidth=.05, name='Feedback')
        self.xData.plot(self.t, self.xsetpoint, pen=(255, 0, 0), linewidth=.05, name='Setpoint')
        self.xData.showGrid(x=True, y=True, alpha=.8)
        self.xData.setLabel('left', 'Potential (V)')
        self.xData.setLabel('bottom', 'Time (ms)')
        # y-axis Data
        self.yData.addLegend()
        self.yData.plot(self.t, self.y, pen=(0, 255, 127), linewidth=.05, name='Feedback')
        self.yData.plot(self.t, self.ysetpoint, pen=(255, 0, 0), linewidth=.05, name='Setpoint')
        self.yData.showGrid(x=True, y=True, alpha=.8)
        self.yData.setLabel('left', 'Potential (V)')
        self.yData.setLabel('bottom', 'Time (ms)')
        # z-axis Data
        self.zData.addLegend()
        self.zData.plot(self.t, self.z, pen=(63, 63, 63), linewidth=.05, name='Feedback')
        self.zData.plot(self.t, self.zsetpoint, pen=(255, 0, 0), linewidth=.05, name='Setpoint')
        self.zData.showGrid(x=True, y=True, alpha=.8)
        self.zData.setLabel('left', 'Potential (V)')
        self.zData.setLabel('bottom', 'Time (ms)')

    def Screenshot(self):
        p = QtWidgets.QApplication.primaryScreen().grabWindow(self.winId())
        filename = QtWidgets.QFileDialog.getSaveFileName(self,
                                                          'Save file',
                                                          'C:\\'+os.path.splitext(self.filename)[0],
                                                          "JPEG Image (*.jpg)")[0]
        p.save(filename, 'jpg')


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LDApp()
    window.show()
    sys.exit(app.exec_())