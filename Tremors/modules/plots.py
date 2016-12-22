import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import numpy as np

def plotZones(latitudes, longitudes, geoLines, perpGeoLines, savePath = ""):
    if savePath == "":
        savePath = "../Tremors/images/zone map.png"
    zones = len(latitudes)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('Tremor Zones')

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_aspect('equal')

    colors = cm.rainbow(np.linspace(0, 1, zones))
    for z in range(0, zones):
        ax.scatter(longitudes[z], latitudes[z], color=colors[z])
        xd = [geoLines[z].x1, geoLines[z].x2]
        yd = [geoLines[z].y1, geoLines[z].y2]
        ax.plot(xd, yd, color='k', linestyle='-', linewidth=3)

        xpd = [perpGeoLines[z].x1, perpGeoLines[z].x2]
        ypd = [perpGeoLines[z].y1, perpGeoLines[z].y2]
        ax.plot(xpd, ypd, color='k', linestyle='-', linewidth=3)

    fig.savefig(savePath)
    plt.close(fig)

def plotZone(dates, distances, magnitudes, zones, zone, title, savePath = ""):
    if savePath == "":
        savePath = "../Tremors/images/" + title + ".png"
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Distance ')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14))

    colors = cm.rainbow(np.linspace(0, 1, zones))
    ax.scatter(dates, distances, color = colors[zone])
    
    plt.gcf().autofmt_xdate()
    plt.rcParams["figure.figsize"] = [30.0, 9.0] 
    fig.savefig(savePath)
    plt.close(fig)

def plotMigrations(migrations, title, savePath = ""):
    if savePath == "":
        savePath = "../Tremors/images/migrations/" + title + ".png"
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Distance')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=14))

    colors = cm.rainbow(np.linspace(0, 1, len(migrations)))

    for migration in migrations:
        ax.scatter(migration.eventDates, migration.eventDistances, color = colors[migrations.index(migration)])

    plt.gcf().autofmt_xdate()
    plt.rcParams["figure.figsize"] = [30.0, 9.0] 
    fig.savefig(savePath)
    plt.close(fig)

def plotMigration(migration, title, minLongitude, minLatitude, maxLongitude, maxLatitude, savePath = "",):
    if savePath == "":
        savePath = "../Tremors/images/migrations/" + title + ".png"
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_title(title)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_aspect('equal')

    colors = cm.rainbow(np.linspace(0, 1, len(migration.eventLongitudes)))
    for x in range(0, len(migration.eventLongitudes)):
        ax.scatter(migration.eventLongitudes[x], migration.eventLatitudes[x], color = colors[x])
    plt.ylim(minLatitude, maxLatitude)
    plt.xlim(minLongitude, maxLongitude)
    fig.savefig(savePath)
    plt.close(fig)

def plotMigrationsGeo(migrations, title, savePath = ""):
    if savePath == "":
        savePath = "../Tremors/images/migrations/" + title + ".png"
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_title(title)
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_aspect('equal')

    colors = cm.rainbow(np.linspace(0, 1, len(migrations)))

    minLongitude = 999
    minLatitude = 999
    maxLongitude = 0
    maxLatitude = 0

    for migration in migrations:
        if migration.minLongitude < minLongitude:
            minLongitude = migration.minLongitude
        if migration.minLatitude < minLatitude:
            minLatitude = migration.minLatitude
        if migration.maxLongitude > maxLongitude:
            maxLongitude = migration.maxLongitude
        if migration.maxLatitude > maxLatitude:
            maxLatitude = migration.maxLatitude

        ax.scatter(migration.eventLongitudes, migration.eventLatitudes, color = colors[migrations.index(migration)])

    fig.savefig(savePath)
    plt.close(fig)
    return (minLongitude, minLatitude, maxLongitude, maxLatitude)