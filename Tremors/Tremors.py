import glob
import numpy as np
import matplotlib.pyplot as plt
import os 
import time
import random

pattern = "%Y/%m/%d %H:%M:%S"
os.environ['TZ'] = 'UTC'

dates = []
latitudes = []
longitudes = []
depths = []
magnitudes = []
types = []

def getEpoc(s):
    if random.randint(0, 1000) == 500:
        os.system('cls')
        print(s.split()[0], "processed")

    return int(time.mktime(time.strptime(s, pattern)))

for file in glob.glob('*.txt'):
    count = 0
    with open(file, 'r') as f:
        for line in f:
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
            
dates = np.array(dates)
dates = np.vectorize(getEpoc)(dates)
latitudes = np.array(latitudes)
longitudes = np.array(longitudes)
depths = np.array(depths)
magnitudes = np.array(magnitudes)
types = np.array(types)

plt.scatter(dates, depths)
plt.show()

pass
