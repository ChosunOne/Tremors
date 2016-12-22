import modules.analysis as analysis
import modules.plots as plots
import modules.processing as processing
import datetime as dt
import os

def tremors(pattern = "%Y/%m/%d %H:%M:%S", segments = 7, sections = 3, windowSize = 10, startyear = "2004", startdate = "/01/01", 
    endyear = "2004", enddate = "/12/31", datafile = ""):

    startTime = dt.datetime.strptime(startyear + startdate + " 00:00:00", pattern)
    endTime = dt.datetime.strptime(endyear + enddate + " 00:00:00", pattern)

    print("Reading raw tremor data")
    data = processing.readTremorData(startTime, endTime, datafile, "%Y-%m-%d %H:%M")

    geoLines = processing.createGeoLines(segments, sections, data)
    perpGeoLines = processing.createPerpGeoLines(geoLines)
    procData = processing.processTremorData(data, geoLines, perpGeoLines)

    if not os.path.exists("../Tremors/images"):
        os.makedirs("../Tremors/images")

    plots.plotZones(procData["perpendicular"]["latitudes"], procData["perpendicular"]["longitudes"], geoLines, perpGeoLines)
    zones = len(procData["perpendicular"]["dates"])
    for i in range(0, zones):
        print("Finding perpendicular migrations in zone " + str(i))
        migrations = processing.findMigrations(procData, "perpendicular", windowSize, i)
        #locations = processing.locateMigrations(migrations, .01)

        if not os.path.exists("../Tremors/images/perpendicular/migrations/zone " + str(i)):
            os.makedirs("../Tremors/images/perpendicular/migrations/zone " + str(i))

        if not os.path.exists("../Tremors/images/perpendicular/migrations/zone " + str(i) + "/geographic"):
            os.makedirs("../Tremors/images/perpendicular/migrations/zone " + str(i) + "/geographic")

        if not os.path.exists("../Tremors/images/perpendicular/migrations/zone " + str(i) + "/linear"):
            os.makedirs("../Tremors/images/perpendicular/migrations/zone " + str(i) + "/linear")

        if not os.path.exists("../Tremors/images/perpendicular/distances"):
            os.makedirs("../Tremors/images/perpendicular/distances")

        plots.plotMigrations(migrations, "Perpendicular Tremor Migrations Zone " + str(i), 
            savePath = "../Tremors/images/perpendicular/migrations/zone " + str(i) + "/Perpendicular Tremor Migrations Zone " + str(i) + ".png")
        plots.plotMigrationsGeo(migrations, "Geographic Perpendicular Tremor Migrations Zone " + str(i),
            savePath = "../Tremors/images/perpendicular/migrations/zone " + str(i) + "/geographic/Geographic Perpendicular Tremor Migrations Zone " + str(i) + ".png")

        for migration in migrations:
            plots.plotMigrations([migration], "Perpendicular Zone " + str(i) + " Migration " + str(migrations.index(migration)), 
                savePath = "../Tremors/images/perpendicular/migrations/zone " + str(i) + "/linear/Migration " + str(migrations.index(migration)) + ".png")
            plots.plotMigration(migration, "Geographic Perpendicular Zone " + str(i) + " Migration " + str(migrations.index(migration)), 
                savePath = "../Tremors/images/perpendicular/migrations/zone " + str(i) + "/geographic/Migration " + str(migrations.index(migration)) + ".png")

        plots.plotZone(procData["perpendicular"]["dates"][i], procData["perpendicular"]["distances"][i], 
            procData["perpendicular"]["magnitudes"][i], zones, i, "Perpendicular Tremor Distances Zone " + str(i),
            "../Tremors/images/perpendicular/distances/Perpendicular Tremor Distances Zone " + str(i) + ".png")

    zones = len(procData["parallel"]["dates"])
    for i in range(0, zones):
        print("Finding parallel migrations in zone " + str(i))
        migrations = processing.findMigrations(procData, "parallel", windowSize, i)

        if not os.path.exists("../Tremors/images/parallel/migrations/zone " + str(i)):
            os.makedirs("../Tremors/images/parallel/migrations/zone " + str(i))

        if not os.path.exists("../Tremors/images/parallel/migrations/zone " + str(i) + "/geographic"):
            os.makedirs("../Tremors/images/parallel/migrations/zone " + str(i) + "/geographic")

        if not os.path.exists("../Tremors/images/parallel/migrations/zone " + str(i) + "/linear"):
            os.makedirs("../Tremors/images/parallel/migrations/zone " + str(i) + "/linear")

        if not os.path.exists("../Tremors/images/parallel/distances"):
            os.makedirs("../Tremors/images/parallel/distances")

        plots.plotMigrations(migrations, "Parallel Tremor Migrations Zone " + str(i),
            savePath = "../Tremors/images/parallel/migrations/zone " + str(i) + "/Parallel Tremor Migrations Zone " + str(i) + ".png")
        plots.plotMigrationsGeo(migrations, "Geographic Parallel Tremor Migrations Zone " + str(i),
            savePath = "../Tremors/images/parallel/migrations/zone " + str(i) + "/geographic/Geographic Parallel Tremor Migrations Zone " + str(i) + ".png")

        for migration in migrations:
            plots.plotMigrations([migration], "Parallel Zone " + str(i) + " Migration " + str(migrations.index(migration)),
                savePath = "../Tremors/images/parallel/migrations/zone " + str(i) + "/linear/Migration " + str(migrations.index(migration)) + ".png")
            plots.plotMigration(migration, "Geographic Parallel Zone " + str(i) + " Migration " + str(migrations.index(migration)), 
                savePath = "../Tremors/images/parallel/migrations/zone " + str(i) + "/geographic/Migration " + str(migrations.index(migration)) + ".png")

        plots.plotZone(procData["parallel"]["dates"][i], procData["parallel"]["distances"][i], 
            procData["parallel"]["magnitudes"][i], zones, i, "Parallel Tremor Distances Zone " + str(i), 
            "../Tremors/images/parallel/distances/Parallel Tremor Distances Zone " + str(i) + ".png")

tremors(datafile = "2004_Nankai.csv", startdate = '/05/03')




































#import glob
#import numpy as np
#from scipy.interpolate import interp1d
#import matplotlib.pyplot as plt
#import matplotlib.dates as mdates
#import matplotlib.cm as cm
#import pandas as pd
#import os 
#import datetime as dt
#import random

#import modules.analysis as analysis
#import modules.plots as plots

#pattern = "%Y/%m/%d %H:%M:%S"
#os.environ['TZ'] = 'UTC'

#dates = []
#latitudes = []
#longitudes = []
#depths = []
#magnitudes = []
#types = []

## For debug, just do the following number of lines
#LINECOUNT = 90000

#for file in glob.glob('JMA*.txt'):
#    count = 0
#    with open(file, 'r') as f:
#        for line in f:
#            if count < LINECOUNT:
#                if line[0] == '#':
#                    continue

#                line = line.split()
                
#                #Check if in bounding box
#                if float(line[2]) < 26 or float(line[3]) < 123 or float(line[2]) > 48 or float(line[3]) > 154:
#                    continue
                
#                dates += [line[0] + " " + line[1][:-3]]
#                latitudes += [float(line[2])]
#                longitudes += [float(line[3])]
#                depths += [float(line[4])]
#                magnitudes += [float(line[5])]
#                if len(line) >= 7:
#                    types += [float(line[6])]
#                else:
#                    types += [0]

#                count += 1
#                if count % 1000 == 0:
#                    os.system('cls')
#                    print(line[0], "processed") 
#            else:
#                break

## Observed Data            
#dates = np.array(dates)
#datesFunc = np.vectorize(lambda d: dt.datetime.strptime(d, '%Y/%m/%d %H:%M:%S'))
#dates = datesFunc(dates)

#latitudes = np.array(latitudes)
#longitudes = np.array(longitudes)

#depths = np.array(depths)
#magnitudes = np.array(magnitudes)
#types = np.array(types)

#xd = np.linspace(125, 153, 7)
#yinterp = interp1d(longitudes, latitudes)

#geoLines = []
#segments = 5
#for x1 in xd:
#    if x1 != xd[-1]:  
#        x2 = xd[np.where(xd==x1)[0][0] + 1]
#        xs = np.linspace(x1, x2, segments)
        
#        for xSegment1 in xs:
#            if xSegment1 != xs[-1]:
#                xSegment2 = xs[np.where(xs==xSegment1)[0][0] + 1]
#                y1 = yinterp(xSegment1).tolist()
#                y2 = yinterp(xSegment2).tolist()
#                geoLine = analysis.Line(xSegment1, y1, xSegment2, y2)
#                geoLines += [geoLine]

## Calculated Data
#distances = [[] for x in range(0, len(geoLines))]
#eventDates = [[] for x in range(0, len(geoLines))]
#eventLatitudes = [[] for x in range(0, len(geoLines))]
#eventLongitudes = [[] for x in range(0, len(geoLines))]
#eventDepths = [[] for x in range(0, len(geoLines))]
#eventTypes = [[] for x in range(0, len(geoLines))]
#eventMagnitudes = [[] for x in range(0, len(geoLines))]
#inf = np.inf

#for i in range(0, len(latitudes)):
#    shortestDistance = inf
#    closestLine = 0
#    for l in geoLines:
#        dist = l.distance(longitudes[i], latitudes[i])
#        if abs(dist) < abs(shortestDistance):
#            shortestDistance = dist
#            closestLine = geoLines.index(l)

#    if abs(shortestDistance) < 5:
#        distances[closestLine] += [shortestDistance]
#        eventDates[closestLine] += [dates[i]]
#        eventLatitudes[closestLine] += [latitudes[i]]
#        eventLongitudes[closestLine] += [longitudes[i]]
#        eventDepths[closestLine] += [depths[i]]
#        eventTypes[closestLine] += [types[i]]
#        eventMagnitudes[closestLine] += [magnitudes[i]]


##Output data to files
#s = pd.Series(distances[1])
#s.to_csv('zone1_distances.csv')


#plots.plotZones(eventLatitudes, eventLongitudes, len(geoLines), xd, yinterp)

#for z in range(0, len(geoLines)):
#    plots.plotZone(eventDates[z], distances[z], magnitudes[z], len(geoLines), z)
