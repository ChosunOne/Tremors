import os 
import datetime as dt
import random
import numpy as np
from scipy.interpolate import interp1d
import analysis

def readTremorData(startTime, endTime, file):
    pattern = "%Y/%m/%d %H:%M:%S"
    os.environ['TZ'] = 'UTC'

    dates = []
    latitudes = []
    longitudes = []
    depths = []
    magnitudes = []
    types = []

    with open(file, 'r') as f:
        for line in f:
            if line[0] == '#':
                    continue
            
            line = line.split()

            #Check if in bounding box
            if float(line[2]) < 26 or float(line[3]) < 123 or float(line[2]) > 48 or float(line[3]) > 154:
                continue
    
            date = line[0] + " " + line[1][:-3]
            date = dt.datetime.strptime(date, pattern)

            if date < startTime:
                continue
            elif date > endTime:
                break
            
            dates += [date]
            latitudes += [float(line[2])]
            longitudes += [float(line[3])]
            depths += [float(line[4])]
            magnitudes += [float(line[5])]
            if len(line) >= 7:
                types += [float(line[6])]
            else:
                types += [0]

            if random.randint(1, 1000) <= 1:
                    os.system('cls')
                    print(line[0], "read") 
    
    dates = np.array(dates)
    latitudes = np.array(latitudes)
    longitudes = np.array(longitudes)
    depths = np.array(depths)
    magnitudes = np.array(magnitudes)
    types = np.array(types)

    return {"dates":dates, "latitudes":latitudes, "longitudes":longitudes, "depths":depths, "magnitudes":magnitudes, "types":types}

def createGeoLines(segments, sections, data):
    xd = np.linspace(125, 153, segments)
    yinterp = interp1d(data["longitudes"], data["latitudes"])
    geoLines = []
    for x1 in xd:
        x2 = xd[np.where(xd==x1)[0][0] + 1]
        xs = np.linspace(x1, x2, sections)
        line = analysis.Line(x1, yinterp(x1), x2, yinterp(x2))
        for xSection1 in xs:
            if xSection1 != xs[-1]:
                xSection2 = xs[np.where(xs==xSection1)[0][0] + 1]
                geoLine = analysis.Line(xSection1, line.y(xSection1), xSection2, line.y(xSection2))
                geoLines += [geoLine]

    return geoLines

def processTremorData(data, geoLines):
    length = len(geoLines)
    eventParaDist = [[] for x in range(0, length)]
    eventPerpDist = [[] for x in range(0, length)]
    eventDates = [[] for x in range(0, length)]
    eventLatitudes = [[] for x in range(0, length)]
    eventLongitudes = [[] for x in range(0, length)]
    eventDepths = [[] for x in range(0, length)]
    eventMagnitudes = [[] for x in range(0, length)]
    eventTypes = [[] for x in range(0, length)]
    inf = np.inf

    perpGeoLines = []
    for line in geoLines:
        length = ((line.x2 - line.x1)**2 + (line.y2 - line.y1)**2)**.5
        