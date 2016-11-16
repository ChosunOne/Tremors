import os 
import datetime as dt
import random
import numpy as np
from scipy.interpolate import interp1d
import modules.analysis

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

    return geoLines, xd, yinterp

def processTremorData(data, geoLines):
    length = len(geoLines)
    eventParaDist = [[] for x in range(0, length)]
    eventPerpDist = [[] for x in range(0, length)]

    eventParaDates = [[] for x in range(0, length)]
    eventPerpDates = [[] for x in range(0, length)]

    eventParaLatitudes = [[] for x in range(0, length)]
    eventPerpLatitudes = [[] for x in range(0, length)]

    eventParaLongitudes = [[] for x in range(0, length)]
    eventPerpLongitudes = [[] for x in range(0, length)]

    eventParaDepths = [[] for x in range(0, length)]
    eventPerpDepths = [[] for x in range(0, length)]

    eventParaMagnitudes = [[] for x in range(0, length)]
    eventPerpMagnitudes = [[] for x in range(0, length)]

    eventParaTypes = [[] for x in range(0, length)]
    eventPerpTypes = [[] for x in range(0, length)]
    inf = np.inf

    perpGeoLines = []
    for line in geoLines:
        length = ((line.x2 - line.x1)**2 + (line.y2 - line.y1)**2)**.5
        lineUnitVector = ((line.x2 - line.x1) / length, (line.y2 - line.y1) / length)
        perpLineUnitVector = (lineUnitVector[1] * -1, lineUnitVector[0])
        midpoint = ((line.x2 - line.x1) / 2, (line.y2 - line.y1) / 2)
        perpLineX = (midpoint[0] + -1. * length / 2. * perpLineUnitVector, midpoint[0] + length / 2. * perpLineUnitVector) 
        perpLineY = (midpoint[1] + -1. * length / 2. * perpLineUnitVector, midpoint[1] + length / 2. * perpLineUnitVector)
        perpLine = analysis.Line(perpLineX[0], perpLineY[0], perpLineX[1], perpLineY[1])
        perpGeoLines += [perpLine]

    for i in range(0, len(data["latitudes"])):
        shortestParaDist = inf
        shortestPerpDist = inf
        closestParaLine = 0
        closestPerpLine = 0
        for l in geoLines:
            dist = l.distance(data["longitudes"][i], data["latitudes"][i])
            if abs(dist) < abs(shortestParaDist):
                shortestParaDist = dist
                closestParaLine = geoLines.index(l)

        for l in perpGeoLines:
            dist = l.distance(data["longitudes"][i], data["latitudes"][i])
            if abs(dist) < abs(shortestPerpDist):
                shortestPerpDist = dist
                closestPerpLine = perpGeoLines.index(l)

        if abs(shortestParaDist) < 5 or abs(shortestPerpDist) < 5:
            eventParaDist[closestParaLine] += [shortestParaDist]
            eventPerpDist[closestPerpLine] += [shortestPerpDist]
            
            eventParaDates[closestParaLine] += [data["dates"][i]]
            eventPerpDates[closestPerpLine] += [data["dates"][i]]

            eventParaLatitudes[closestParaLine] += [data["latitudes"][i]]
            eventPerpLatitudes[closestPerpLine] += [data["latitudes"][i]]

            eventParaLongitudes[closestParaLine] += [data["longitudes"][i]]
            eventPerpLongitudes[closestPerpLine] += [data["longitudes"][i]]

            eventParaDepths[closestParaLine] += [data["depths"][i]]
            eventPerpDepths[closestPerpLine] += [data["depths"][i]]

            eventParaTypes[closestParaLine] += [data["types"][i]]
            eventPerpTypes[closestPerpLine] += [data["types"][i]]

            eventParaMagnitudes[closestParaLine] += [data["types"][i]]
            eventPerpMagnitudes[closestPerpLine] += [data["types"][i]]

    procData = {"parallel": {"distances":eventParaDist, "dates":eventParaDates, "latitudes":eventParaLatitudes, "longitudes":eventParaLongitudes, "depths":eventParaDepths, "types":eventParaTypes, "magnitudes":eventParaMagnitudes},
                "perpendicular": {"distances":eventPerpDist, "dates":eventPerpDates, "latitudes":eventPerpLatitudes, "longitude":eventPerpLongitudes, "depths":eventPerpDepths, "types":eventPerpTypes, "magnitudes":eventPerpMagnitudes}}

    return procData
    
        