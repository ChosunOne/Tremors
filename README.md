# Tremors
Detect Tremor migrations automatically

This program is designed to automatically detect the migration of seismic tremors in a given dataset.  

# Dependencies
The SciPy stack is required in order to run this script.  A full list of dependencies is in the requirements.txt file.

# Usage
Simply call the "tremors" function and specify the data file, start and end year, start and end date, the pattern to parse the data into dates, how many segments you want for the data, how many sections you want to split each segment into, and the number of tremor events to consider at one time for automatic migration detection.

# Output
The script will generate an "images" folder with the output of the processing.  Inside you will find two directories and an image.  The "zone map.png" file shows you the lines of fit used in migration detection, with the "parallel" directory being the result of considering the distance to the parallel line of fit for each zone, and the "perpendicular" directory being the result of considering the distance to the line perpendicular to the line of fit for each zone.  

Inside either directory you will find two additional directories, a "distances" and "migrations" folder.  The "distances" folder stores the raw distance data for each tremor event in the designated zone.  You can compare the output here with the output in the migrations folder to verify the accuracy of the migration detection.
Inside the migrations folder you will find another directory for each zone generated. Each zone folder contains two additional directories, a "geographic" and "linear" folder, as well as a graph showing the linear distance to the line of fit (or line perpendicular to it) of each tremor event, with each dot colored to represent the migration it belongs to.  

Inside the "geographic" folder you will find first a geographic projection of all tremor events in that zone, colored by which migration each event belongs to.  The color also represents the progression in time of the migrations, starting with purple and progressing through the rainbow to red.  The other image files are the geographic projections of each individual migration, with each tremor event colored by time, starting at purple and ending in red.  

Inside the "linear" folder you will find the linear distances to the line of fit (or line perpendicular to it) of each tremor event in the migration for each migration in the zone.  

