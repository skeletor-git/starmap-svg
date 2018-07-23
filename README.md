# starmap-svg
for generating svg starmaps from selected coordinates and time 

## Requirements 
	Python > 3.2 
	pip3 install svgwrite

## Usage
	python -coord [northern,eastern] -time [hour.minute.second] -date [day.month.year] -utc [utc]

	optional parameters
		-o 
		-width = 200. width in mm
		-height = 200. height in mm
		-magnitudelimit = 4.5 from 0-7.0
		-backgroundcolor = rgb(45,59,98) rgb(r,g,b)
		-starcolor = rgb(255,255,255)
		-infotext = HELSINKI NIGHT SKY

## Example
	 python starmap.py -coord 45.28,11.08 -time 12.30.30 -date 12.01.2011 -utc +2


## Info
	#Stars declination and hour data file "Yale Bright Star Catalog 5"

## TODO
	Planets and Moon implementations