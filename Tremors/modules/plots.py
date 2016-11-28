import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import numpy as np

def plotZones(latitudes, longitudes, geoLines, perpGeoLines):
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

    fig.savefig("../images/zone map.png")
    plt.close(fig)

def plotZone(dates, distances, magnitudes, zones, zone, title):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    
    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Distance ')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))

    colors = cm.rainbow(np.linspace(0, 1, zones))
    ax.scatter(dates, distances, color = colors[zone])

    fig.savefig("../images/" + title + ".png")
    plt.close(fig)

def plotMigrations(migrations, title):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    ax.set_title(title)
    ax.set_xlabel('Date')
    ax.set_ylabel('Distance')

    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y/%m/%d %H:%M:%S'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator(interval=7))
    colors = cm.rainbow(np.linspace(0, 1, len(migrations)))

    for migration in migrations:
        ax.scatter(migration.eventDates, migration.eventDistances, color = colors[migrations.index(migration)])

    fig.savefig("../images/migrations/" + title +".png")
    plt.close(fig)