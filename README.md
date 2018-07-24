# starmap-svg
for generating svg starmaps from selected coordinates and time 

## Requirements 
	Python > 3.2 
	pip3 install svgwrite

## Usage
	python starmap.py -h

	-h, --help            show this help message and exit

	-coord COORD, --coord COORD
	                    coordinates in format northern,eastern
	-time TIME, --time TIME
	                    time in format hour.minute.second
	-date DATE, --date DATE
	                    date in format day.month.year
	-utc [UTC], --utc [UTC]
	                    utc of your location -12 to +12
	-o OUTPUT, --output OUTPUT
	                    output filename.svg
	-width [WIDTH], --width [WIDTH]
	                    width in mm
	-height [HEIGHT], --height [HEIGHT]
	                    height in mm
	-magn [MAGN], --magn [MAGN]
	                    magnitude limit

## Example
	python starmap.py -coord 60.186,24.959 -time 12.00.00 -date 01.01.2000 -utc +2

![image](https://github.com/skeletor-git/starmap-svg/blob/master/example/bitmap.png)

## Info
	Stars declination and hour data file "Yale Bright Star Catalog 5"

## TODO
	Planets and Moon implementations