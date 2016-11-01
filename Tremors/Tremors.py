import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

# Line from Kumamoto to Osaka
geoLine = analysis.Line(32.8031, 130.7079, 34.6937, 135.5022)


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

# Calculated Data
distances = []
for i in range(0, len(latitudes)):
    d = geoLine.distance(latitudes[i], longitudes[i])
    
    # Remove extreme outliers that are not in the area of interest
    if d > 10 or d < -10:
        d = 0
    distances += [d]

distanceSeries = pd.Series(distances, dates)
distancesRollingMean = distanceSeries.rolling(center=False, window=1400).mean()
distancesExpRollingMean = distanceSeries.ewm(span=1400).mean()

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d %H:%M:%S'))
plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))

#plt.scatter(dates, distances)
#plt.scatter(dates, distancesRollingMean)
plt.scatter(dates, distancesExpRollingMean)

plt.gcf().autofmt_xdate()
plt.show()
