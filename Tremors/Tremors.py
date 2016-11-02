import glob
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import pandas as pd
import os 
import datetime as dt
import random
import modules.analysis as analysis

pattern = "%Y/%m/%d %H:%M:%S"
os.environ['TZ'] = 'UTC'

dates = []
latitudes = []
longitudes = []
depths = []
magnitudes = []
types = []

# For debug, just do the following number of lines
LINECOUNT = 30000

for file in glob.glob('JMA*.txt'):
    count = 0
    with open(file, 'r') as f:
        for line in f:
            if count < LINECOUNT:
                if line[0] == '#':
                    continue

                line = line.split()
                
                #Check if in bounding box
                if float(line[2]) < 26 or float(line[3]) < 123 or float(line[2]) > 48 or float(line[3]) > 154:
                    continue
                
                dates += [line[0] + " " + line[1][:-3]]
                latitudes += [float(line[2])]
                longitudes += [float(line[3])]
                depths += [float(line[4])]
                magnitudes += [float(line[5])]
                if len(line) >= 7:
                    types += [float(line[6])]
                else:
                    types += [0]

                count += 1
                if count % 1000 == 0:
                    os.system('cls')
                    print(line[0], "processed") 
            else:
                break

# Observed Data            
dates = np.array(dates)
datesFunc = np.vectorize(lambda d: dt.datetime.strptime(d, '%Y/%m/%d %H:%M:%S'))
dates = datesFunc(dates)

latitudes = np.array(latitudes)
longitudes = np.array(longitudes)

depths = np.array(depths)
magnitudes = np.array(magnitudes)
types = np.array(types)

xd = np.linspace(125, 153, 7)
yinterp = interp1d(longitudes, latitudes)

geoLines = []
for x in xd:
    if x != xd[-1]:
        x1 = x  
        y1 = yinterp(x1).tolist()
        x2 = xd[np.where(xd==x1)[0][0] + 1]
        y2 = yinterp(x2).tolist()
        geoLine = analysis.Line(x1, y1, x2, y2)
        geoLines += [geoLine]

# Calculated Data
distances = [[] for x in range(0, len(geoLines))]
eventDates = [[] for x in range(0, len(geoLines))]
eventLatitudes = [[] for x in range(0, len(geoLines))]
eventLongitudes = [[] for x in range(0, len(geoLines))]
eventDepths = [[] for x in range(0, len(geoLines))]
eventTypes = [[] for x in range(0, len(geoLines))]
eventMagnitudes = [[] for x in range(0, len(geoLines))]
inf = np.inf

for i in range(0, len(latitudes)):
    shortestDistance = inf
    closestLine = 0
    for l in geoLines:
        dist = l.distance(longitudes[i], latitudes[i])
        if abs(dist) < abs(shortestDistance):
            shortestDistance = dist
            closestLine = geoLines.index(l)

    if abs(shortestDistance) < 5:
        distances[closestLine] += [shortestDistance]
        eventDates[closestLine] += [dates[i]]
        eventLatitudes[closestLine] += [latitudes[i]]
        eventLongitudes[closestLine] += [longitudes[i]]
        eventDepths[closestLine] += [depths[i]]
        eventTypes[closestLine] += [types[i]]
        eventMagnitudes[closestLine] += [magnitudes[i]]

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title('Tremor Zones')
ax.set_xlabel('Longitude (°)')
ax.set_ylabel('Latitude (°)')

#distanceKTSeries = pd.Series(distancesKT, dates)
#distancesKTRollingMean = distanceKTSeries.rolling(center=False, window=1400).mean()
#distancesKTExpRollingMean = distanceKTSeries.ewm(span=1400).mean()

#plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d %H:%M:%S'))
#plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))

#plt.scatter(dates, distancesKT)
#plt.scatter(dates, distancesKTRollingMean)
#plt.scatter(dates, distancesKTExpRollingMean)
#plt.scatter(longitudes, latitudes)
#plt.scatter(eventLongitudes[1], eventLatitudes[1])
colors = cm.rainbow(np.linspace(0, 1, len(geoLines)))
for l in range(0, len(geoLines)):
    ax.scatter(eventLongitudes[l], eventLatitudes[l], color = colors[l])

ax.plot(xd, yinterp(xd), color='k', linestyle='-', linewidth=3)

#plt.gcf().autofmt_xdate()
plt.show()
