import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.cm as cm
import numpy as np

def plotZones(latitudes, longitudes, xd, yinterp):
    zones = len(latitudes)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title('Tremor Zones')

    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')

    colors = cm.rainbow(np.linspace(0, 1, zones))
    for z in range(0, zones):
        ax.scatter(longitudes[z], latitudes[z], color=colors[z])

    ax.plot(xd, yinterp(xd), color='k', linestyle='-', linewidth=3)

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