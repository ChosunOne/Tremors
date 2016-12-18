import os 
import datetime as dt
import random
import numpy as np
from numpy import poly1d
import modules.analysis as analysis
from modules.migration import Migration

def readTremorData(startTime, endTime, file, pattern):
    os.environ['TZ'] = 'UTC'

    dates = []
    latitudes = []
    longitudes = []
    depths = []
    magnitudes = []
    types = []

    with open(file, 'r') as f:
        lines = f.readlines()[3:]
        slines = lines
        # Find starting point
        if ".csv" in file:
            startLine = lines[0].split(",")
        else:
            startLine = lines[0].split()
        date = dt.datetime.strptime(startLine[0] + " " + startLine[1][:-3], pattern)
        index = 0
        while abs((date - startTime)) > dt.timedelta(1):
            if date < startTime:
                slines = slines[index:]
                index = int(len(slines) / 2)
                if ".csv" in file:
                    startLine = slines[index].split(",")
                else:
                    startLine = slines[index].split()
                date = dt.datetime.strptime(startLine[0] + " " + startLine[1][:-3], pattern)
            else:
                slines = slines[:index]
                index = int(len(slines) / 2)
                if ".csv" in file:
                    startLine = slines[index].split(",")
                else:
                    startLine = slines[index].split()
                date = dt.datetime.strptime(startLine[0] + " " + startLine[1][:-3], pattern)
                
        lines = lines[lines.index(slines[index]):]

        for line in lines:
            if line[0] == '#':
                    continue
            
            if ".csv" in file:
                line = line.split(",")
            else:
                line = line.split()
            
            if len(line) != 9:
                continue

            #Check if in bounding box
            if float(line[2]) < 26 or float(line[3]) < 123 or float(line[2]) > 48 or float(line[3]) > 154:
                continue
    
            date = line[0] + " " + line[1][:-3]
            date = dt.datetime.strptime(date, pattern)

            if random.randint(1, 1000) <= 1:
                os.system('cls')
                print(line[0], "read") 

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
    
    dates = np.array(dates)
    latitudes = np.array(latitudes)
    longitudes = np.array(longitudes)
    depths = np.array(depths)
    magnitudes = np.array(magnitudes)
    types = np.array(types)

    return {"dates":dates, "latitudes":latitudes, "longitudes":longitudes, "depths":depths, "magnitudes":magnitudes, "types":types}

def createGeoLines(segments, sections, data):
    xmin = min(data["longitudes"])
    xmax = max(data["longitudes"])
    xd = np.linspace(xmin, xmax, segments + 1)
    #yfit = poly1d(np.polyfit(data["longitudes"], data["latitudes"], 6))
    geoLines = []
    for x1 in xd:
        if x1 != xd[-1]:
            x2 = xd[np.where(xd==x1)[0][0] + 1]
            xs = np.linspace(x1, x2, sections)
            sectionX = []
            sectionY = []
            for x in range(0, len(data["longitudes"])):
                if data["longitudes"][x] >= x1 and data["longitudes"][x] <= x2:
                    sectionX += [data["longitudes"][x]]
                    sectionY += [data["latitudes"][x]]
            yfit = poly1d(np.polyfit(sectionX, sectionY, 1))

            y1 = yfit(x1).tolist()
            y2 = yfit(x2).tolist()
            line = analysis.Line(x1, y1, x2, y2)
            for xSection1 in xs:
                if xSection1 != xs[-1]:
                    xSection2 = xs[np.where(xs==xSection1)[0][0] + 1]
                    geoLine = analysis.Line(xSection1, line.y(xSection1), xSection2, line.y(xSection2))
                    geoLines += [geoLine]

    return geoLines

def createPerpGeoLines(geoLines):
    perpGeoLines = []
    for line in geoLines:
        length = ((line.x2 - line.x1)**2 + (line.y2 - line.y1)**2)**.5

        lineUnitVector = ((line.x2 - line.x1) / length, (line.y2 - line.y1) / length)
        perpLineUnitVector = (lineUnitVector[1] * -1, lineUnitVector[0])

        midpoint = ((line.x2 + line.x1) / 2, (line.y2 + line.y1) / 2)
        dist = length / 2.

        perpLineX = (midpoint[0] + -dist * perpLineUnitVector[0], midpoint[0] + dist * perpLineUnitVector[0]) 
        perpLineY = (midpoint[1] + -dist * perpLineUnitVector[1], midpoint[1] + dist * perpLineUnitVector[1])

        perpLine = analysis.Line(perpLineX[0], perpLineY[0], perpLineX[1], perpLineY[1])
        perpGeoLines += [perpLine]

    return perpGeoLines

def processTremorData(data, geoLines, perpGeoLines):
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

        if random.randint(1, 1000) <= 1:
            os.system('cls')
            print(data["dates"][i], "processed") 

    procData = {"parallel": {"distances":eventParaDist, "dates":eventParaDates, "latitudes":eventParaLatitudes, "longitudes":eventParaLongitudes, "depths":eventParaDepths, "types":eventParaTypes, "magnitudes":eventParaMagnitudes},
                "perpendicular": {"distances":eventPerpDist, "dates":eventPerpDates, "latitudes":eventPerpLatitudes, "longitudes":eventPerpLongitudes, "depths":eventPerpDepths, "types":eventPerpTypes, "magnitudes":eventPerpMagnitudes}}

    return procData
    
def findMigrations(procData, dataset, windowSize, zone, residualThreshold = .05, eventThreshold = 20, fixedWindowSize = 10):

    migrationDistances = []
    migrationDates = []
    migrationLongitudes = []
    migrationLatitudes = []
    migrationMagnitudes = []
    migrations = []

    dates = procData[dataset]["dates"][zone]
    distances = procData[dataset]["distances"][zone]
    longitudes = procData[dataset]["longitudes"][zone]
    latitudes = procData[dataset]["latitudes"][zone]
    magnitudes = procData[dataset]["magnitudes"][zone]

    for date in dates:
    
        if date == dates[-1]:
            break

        window = {"dates":[], "distances":[]}
        index = dates.index(date)

        for x in range(0, fixedWindowSize):
            if dates[index] - date < dt.timedelta(days = windowSize):
                window["dates"] += [dates[index]]
                window["distances"] += [distances[index]]
            else:
                continue

            if dates[index + 1] == dates[-1]:
                break
            else:  
                index += 1
            
        fit = np.polyfit([x.timestamp() for x in window["dates"]], window["distances"], 1, full=True)
        residual = fit[1]

        if residual < residualThreshold and len(window["dates"]) == fixedWindowSize:
            i = dates.index(date)

            migrationDistances += [distances[i]]
            migrationDates += [date]
            migrationLatitudes += [latitudes[i]]
            migrationLongitudes += [longitudes[i]]
            migrationMagnitudes += [magnitudes[i]]

        elif (residual >= residualThreshold and len(migrationDistances) > eventThreshold):
            migrations += [Migration(migrationDates, migrationDistances, migrationLatitudes, migrationLongitudes, migrationMagnitudes)]
            
            migrationDistances = []
            migrationDates = []
            migrationLatitudes = []
            migrationLongitudes = []
            migrationMagnitudes = []

        else:
            if len(migrationDistances) > eventThreshold:
                migration = Migration(migrationDates, migrationDistances, migrationLatitudes, migrationLongitudes, migrationMagnitudes)
                if migration.duration > dt.timedelta(days=1):
                    migrations += [migration]

            migrationDistances = []
            migrationDates = []
            migrationLatitudes = []
            migrationLongitudes = []
            migrationMagnitudes = []
        
    return migrations
        