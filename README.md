# starmap-svg
for generating svg starmaps from selected coordinates and time 

## Requirements 
	Python > 3.2 
	pip3 install svgwrite

## Usage
	python -coord [northern,eastern] -time [hour.minute.second] -date [day.month.year] -utc [utc]

	optional parameters
		-o = starmap.svg. Output file name
		-width = 200. Width in mm
		-height = 200. Height in mm
		-magnitudelimit = 4.5.Magnitude limit is from 0-7.0. 0 is brightest, 7.0 dimmest
		-backgroundcolor = rgb(45,59,98).  rgb(r,g,b)
		-starcolor = rgb(255,255,255), rgb(r,g,b)
		-infotext = HELSINKI NIGHT SKY, Text that is displayed in the corner of the image

## Example
	 python starmap.py -coord 45.28,11.08 -time 12.30.30 -date 12.01.2011 -utc +2


## Info
	#Stars declination and hour data file "Yale Bright Star Catalog 5"

## TODO
	Planets and Moon implementations