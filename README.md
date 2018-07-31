# starmap-svg
for generating svg starmaps from selected coordinates and time 

## Requirements 
	Python > 3.2 
	pip install svgwrite

## Usage
	python starmap.py -h

	optional arguments:
	  -h, --help            show this help message and exit

	  -coord COORD, --coord COORD
	                        coordinates in format northern,eastern
	  -time TIME, --time TIME
	                        time in format hour.minute.second
	  -date DATE, --date DATE
	                        date in format day.month.year
	  -utc [UTC], --utc [UTC]
	                        utc of your location -12 to +12
	  -magn [MAGN], --magn [MAGN]
	                        magnitude limit 0.1-12.0
	  -summertime [SUMMERTIME], --summertime [SUMMERTIME]
	                        if it is summertime on the date of the starchart
	  -guides [GUIDES], --guides [GUIDES]
	                        draw guides True/False
	  -constellation [CONSTELLATION], --constellation [CONSTELLATION]
	                        show constellation True/False
	  -o OUTPUT, --output OUTPUT
	                        output filename.svg
	  -width [WIDTH], --width [WIDTH]
	                        width in mm
	  -height [HEIGHT], --height [HEIGHT]
	                        height in mm
	  -info INFO, --info INFO
	                        Info text example eame of the place




## Example 1
	python starmap.py -coord 60.186,24.959 -time 12.00.00 -date 01.01.2000 -utc +2 -constellation True

![image](https://github.com/skeletor-git/starmap-svg/blob/master/example/starmap.png)

## Example 2
	python starmap.py -coord 35.684,139.728 -time 20.00.00 -date 15.07.2018 -utc +9 -info TOKYO -guides True -magn 10.0 -width 150 -height 220

![image](https://github.com/skeletor-git/starmap-svg/blob/master/example/starmap2.png)


## Info

Stars data: "Yale Bright Star Catalog ver5"
http://tdc-www.harvard.edu/catalogs/bsc5.html

## TODO
	Planets and Moon orbits, Automated summertime.