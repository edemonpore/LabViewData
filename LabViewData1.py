# LabViewData1
# Latest: 12/2018

import os
import time as pause
import numpy as np
import math
import csv
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from tkinter import *
from tkinter import filedialog

# Establish plotly credentials and/or settings
plotly.tools.set_credentials_file(username='e@demonpore.com', api_key='7HOIUl4yTmgPyY5AA2aI')
# plotly.tools.set_config_file(world_readable=False, sharing='private')

# Get the data input file
root = Tk()
root.withdraw()
root.update()
filename = filedialog.askopenfilename(initialdir="C:\\Users\\User\\Desktop\\Demonpore\\Data\\Data\\Feedback",
                                      title="Select Data File",
                                      filetypes=(("Excel csv", "*.csv"), ("all files", "*.*")))
root.destroy()

DataFile = csv.reader(open(filename))

# Data categories established by Tomi's software
time = []
xsetpoint = []
ysetpoint = []
zsetpoint = []
x = []
y = []
z = []

# Skip header, then read data
next(DataFile, None)
n = 0
for row in DataFile:
    time.append(n)
    n = n + 10
    xsetpoint.append(float(row[1]))
    ysetpoint.append(float(row[2]))
    zsetpoint.append(float(row[3]))
    x.append(float(row[4]))
    y.append(float(row[5]))
    z.append(float(row[6]))

# Data processing and DFT
Fs = 10000
Ts = (time[2] - time[1]) / Fs;
n = len(time)
t = np.arange(0, n / Fs, Ts)
k = np.arange(n)
T = n / Fs
frq = k / T
frq = frq[range(n // 2)]

X = np.fft.fft(x) / n
X = X[range(n // 2)]
Y = np.fft.fft(y) / n
Y = Y[range(n // 2)]

# Scaling, Offsets etc.
timeoffset = 0
xscale = []
yscale = []
xmin = []
ymin = []
xcounter = 0
ycounter = 0

for i in range(n):
    if xsetpoint[i] == 0 and xcounter >= timeoffset and xcounter <= 2 * timeoffset:
        xcounter = xcounter + 1
        xmin.append(x[i])
        xscale.append(1)  # In case no x values are being set
    elif xsetpoint[i] != 0 and xcounter >= timeoffset and xcounter <= 2 * timeoffset:
        xcounter - xcounter + 1
        xscale.append(xsetpoint[i].real / x[i].real)
    else:
        xcounter = 0
    if ysetpoint[i] == 0 and ycounter >= timeoffset and ycounter <= 2 * timeoffset:
        ycounter = ycounter + 1
        ymin.append(y[i])
        yscale.append(1)  # In case no y values are being set
    elif ysetpoint[i] != 0 and ycounter >= timeoffset and ycounter <= 2 * timeoffset:
        ycounter = ycounter + 1
        yscale.append(ysetpoint[i].real / y[i].real)
    else:
        ycounter = 0

for i in range(n):
    x[i] = (x[i] - np.average(xmin)) * np.average(xscale)
    y[i] = (y[i] - np.average(ymin)) * np.average(xscale)

print("Average minimum of x = " + str(np.average(xmin)))
print("Average scale of x position = " + str(np.average(xscale)))
print("Average minimum of y = " + str(np.average(ymin)))
print("Average scale of y position = " + str(np.average(yscale)))

# Plot raw data
trace1 = go.Scattergl(x=time, y=xsetpoint, line=dict(color=('rgb(128,0,0)'), width=1), opacity=.5, name='x-setpoint')
trace2 = go.Scattergl(x=time, y=ysetpoint, line=dict(color=('rgb(0,128,0)'), width=1), opacity=.5, name='y-setpoint')
trace3 = go.Scattergl(x=time, y=zsetpoint, line=dict(color=('rgb(0,0,128)'), width=1), opacity=.5, name='z-setpoint')
trace4 = go.Scattergl(x=time, y=x, line=dict(color=('rgb(255,0,0)'), width=1), name='x')
trace5 = go.Scattergl(x=time, y=y, line=dict(color=('rgb(0,255,0)'), width=1), name='y')
trace6 = go.Scattergl(x=time, y=z, line=dict(color=('rgb(0,0,255)'), width=1), name='z')

data = [trace1, trace2, trace3, trace4, trace5, trace6]

plotly.offline.plot({"data": data, "layout":
    go.Layout(title=os.path.split(filename)[1],
              xaxis=dict(title='Time (ms)',
                         titlefont=dict(family='Courier New, monospace', size=16, color='rgb(0,0,0)')),
              yaxis=dict(title='Setpoints vs. Measured Positions',
                         titlefont=dict(family='Courier New, monospace', size=16, color='rgb(0,0,0)'))
              )
                     })

pause.sleep(1)  # Apparently necessary pause to get plotly to work with both url graphs

# Plot setpoint and position feedback differences
xdiff = []
ydiff = []
for i in range(n):
    xdiff.append(xsetpoint[i] - x[i])
    ydiff.append(ysetpoint[i] - y[i])

trace1 = go.Scattergl(x=frq, y=xdiff, line=dict(color=('rgb(255,0,0)'), width=1), name='x-setpoint')
trace2 = go.Scattergl(x=frq, y=ydiff, line=dict(color=('rgb(0,255,0)'), width=1), name='y-setpoint')

data = [trace1, trace2]

plotly.offline.plot({"data": data, "layout":
    go.Layout(title="Setpoint-Position:   " + os.path.split(filename)[1],
              xaxis=dict(title='Time (ms)',
                         titlefont=dict(family='Courier New, monospace', size=16, color='rgb(0,0,0)')),
              yaxis=dict(title='Setpoint - Measured Position',
                         titlefont=dict(family='Courier New, monospace', size=16, color='rgb(0,0,0)'))
              )
                     })

pause.sleep(1)

# Plot DFT's
trace1 = go.Scattergl(x=frq, y=abs(X).real, line=dict(color=('rgb(255,0,0)'), width=1), name='DFT of x')
trace2 = go.Scattergl(x=frq, y=abs(Y).real, line=dict(color=('rgb(0,255,0)'), width=1), name='DFT of y')

data = [trace1, trace2]

plotly.offline.plot({"data": data, "layout":
    go.Layout(title="DFT:   " + os.path.split(filename)[1],
              xaxis=dict(title='Frequency (Hz)',
                         titlefont=dict(family='Courier New, monospace', size=16, color='rgb(55,55,55)')),
              yaxis=dict(title='DFT',
                         titlefont=dict(family='Courier New, monospace', size=16, color='rgb(0,0,0)'))
              )
                     })
