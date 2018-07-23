
import svgwrite
import random 
import math
import argparse

############ DEFAULT VALUES AND CONSTS ####################################

PI = 3.141592

font_style = "font-size:10px; letter-spacing:0.7px; font-family:sans-serif; stroke-width:5;font-weight:bold;"

background_color = "rgb(45,59,98)"
line_color = "rgb(255,255,255)"

output_file = 'starmap.svg'

#Date & Time
date = '01.01.2000' 
time = '12.00'
utc = 0
summertime = False

#Coordinates
coord = "60.186,24.959"
coord = "52.00,1.0"


#placetext for leftdown corner
info = 'HELSINKI NIGHT SKY'

#Size of poster in mm
width = 200
height = 200

def mm_to_px(mm):
	px = mm*96/25.4
	return px

#Smaller the star bigger the magnitude
magnitude_limit = 3.5
aperture = 0.4 
amplification = width*0.045

############ STARDATAFILE ################################################

#Stars declination and hour data file "Yale Bright Star Catalog 5"
file = "datafiles/ybsc5.txt"
file = "datafiles/stardata.txt"

#read data from file to nested list
def read_star_coordinate_file(file):
	data = []
	with open(file, 'rt') as f:
		for line in f:
			if (',' in line): 
				data.append([ n for n in line.strip().split(',')])
	return data

data = read_star_coordinate_file(file)

############ ARGPARSER ###################################################

parser = argparse.ArgumentParser(description='Generate starmap svg file')
parser.add_argument('-coord','--coord', help='coordinates in format northern,eastern',default=coord )
parser.add_argument('-time','--time', help='time in format hour.minute.second',default=time)
parser.add_argument('-date','--date', help='date in format day.month.year', default=date)
parser.add_argument('-utc','--utc',nargs='?', help='utc of your coord -12 to +12', type=int , default=utc)

parser.add_argument('-o','--output', help='output filename.svg',default='starmap.svg' )
parser.add_argument('-width','--width',nargs='?', help='width in mm',type=int, default=width)
parser.add_argument('-height','--height',nargs='?', help='height in mm',type=int, default=height)
parser.add_argument('-magn','--magn',nargs='?', help='magnitude limit',type=int, default=magnitude_limit)

args = parser.parse_args()

coord = args.coord
time = args.time
date = args.date
utc = args.utc

output_file = args.output

height = args.height
width = args.width

print(coord)
print(date)
print(time)

northern,eastern = map(float,coord.split(','))

########## DRAWING FUNCTIONS  ###########################################

# Generates random star shape to given coordinate and magnitude and color
def star_generator(x,y,mag,color):

	# randomize the number of points in star
	points = random.randint(4,8)
	points = points * 2
	angle = 2*PI/(points)

	# generate the path
	path = []
	for point in range(0,points,2):
		#point of star
		path.append(polar_to_cartesian(mag,angle*point,x,y))
		#point between two star points
		path.append(polar_to_cartesian(mag/2,angle*(point+1),x,y))
	
	#add object to svg
	stars = image.add(image.polygon(path,id ='star',stroke="none",fill=color))


def dot_generator(x,y,mag,color):
	image.add(image.circle((x,y),mag,id ='dot',stroke="none",fill=color))


########## TIME CALCULATION  ###########################################

#date to days
def date_and_time_to_rad(date,time):

	days_in_year = 365 # days in normal year
	months = [31,28,31,30,31,30,31,31,30,31,30,31] #Array of days in months

	year = int(date[6:10])
	#Leap year
	if(year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
		months[1] = 29 
		days_in_year = 366

	days  = sum(months[0:int(date[3:5])-1])	#month to days
	days += int(date[0:2])-1				#days

	minutes  = float(time[0:2])*60  		#hour
	minutes += float(time[3:5])	  			#minute
	
	#Summertime
	if(summertime):
		minutes -= 60
	#UTC
	minutes += 60*utc

	#TODO yearly mistake epoch
	#Epoch J2000 12.00

	#calculatr degree from years -EPOCH 2000 year
	degree = -(year-2000)*360/26000
	
	print(degree)
	#calculate degree from days
	degree -= (days)*360.0/days_in_year
	print(degree)
	#calculate degree from minutes -EPOCH 12 hour
	degree -= ((minutes-12*60)*360/(24*60-4)) % 360
	print(degree)

	return math.radians(degree)


########## POSITION CALCULATION  ###########################################

#change polar coordinates to cartesian coordinates
def polar_to_cartesian(radius,angle,centerx,centery):
	return [centerx + radius*math.cos(angle), centery + radius*math.sin(angle)]


def distance_between(north,east,dec_angle,ra_angle):
	delta_ra = ra_angle - east
	rad = math.acos(math.cos(delta_ra)*math.cos(north)*math.cos(dec_angle) + math.sin(north)*math.sin(dec_angle))
	return rad 

def hours_to_decimal(ra):

	seconds  = float(ra[0:2])*3600 		#hour
	seconds += float(ra[2:4])*60	  	#minute
	seconds += float(ra[4:6])		  	#seconds
	return seconds/(3600.0)

def right_ascension_to_rad(ra):

	return PI * 2.0 * ra / 24.0

def declination_to_rad(dec):

    return math.radians(float(dec))

def rad_to_xy(north,east, dec_angle, ra_angle):
    delta_ra = ra_angle-east
    x = math.cos(dec_angle) * math.sin(delta_ra)
    y = math.sin(dec_angle) * math.cos(north) - math.cos(dec_angle) * math.cos(delta_ra) * math.sin(north)
    return x * 300 ,y * 300




########## STAR AND GUIDE GENERATION  ########################################

def generate_guides(northern_N,eastern_E):

	N = math.radians(northern_N)
	E = math.radians(eastern_E)


	draw_guides = []
	for angle_test in range(0,240):
		for decl_test in range(-3,3):
			draw_guides.append([decl_test*30,angle_test/10.0])
	for angle_test in range(0,24):
		for decl_test in range(-160,160):
			draw_guides.append([decl_test/2.0,angle_test])

	for line in draw_guides:

		declination = declination_to_rad(line[0])
		ascension = right_ascension_to_rad(line[1])
		
		#magnitude of dot
		magn = 1.1
		radius = distance_between(N,E,declination,ascension)
		x,y = rad_to_xy(N,E,declination,ascension)

		if (radius < (90*PI/180.0)):
			dot_generator(half_x-x,half_y-y,magn*aperture,line_color)

def generate_starmap(northern_N,eastern_E,date,time):

	
	N = math.radians(northern_N)
	E = math.radians(eastern_E)

	raddatetime = date_and_time_to_rad(date,time)

	for line in data:
		if(float(line[2]) < magnitude_limit):

			#star position from datafile
			# ascension = right_ascension_to_rad(hours_to_decimal(line[0]))
			ascension = right_ascension_to_rad(float(line[0]))+raddatetime
			declination = declination_to_rad(line[1])

			x,y = rad_to_xy(N,E,declination,ascension)
			radius = distance_between(N,E,declination,ascension)

			#magnitude of star
			magn = float(line[2])
			# print magn
			magn = 6 - 2.5*math.log(2+magn,10)


			if (radius < 90*PI/180.0):
				if (magn < 3):
					dot_generator(half_x-x,half_y-y,0.4*aperture,line_color)
				else:
					star_generator(half_x-x,half_y-y,magn*aperture,line_color)

				#North Star 
				if(declination > 89.1*PI/180.0):
				 	star_generator(half_x-x,half_y-y,magn*aperture,"red")

				if len(line) > 3:
					image.add(image.text('x', insert=(half_x-x,half_y-y), fill=line_color, style=font_style))





########## MAIN FUNCTION  ###########################################


if __name__ == '__main__':

	half_x = mm_to_px(width/2)
	half_y = mm_to_px(height/2)

	# weekday(date,'fi')

	#Svgfile 
	image = svgwrite.Drawing(output_file,size=(str(width)+'mm',str(height)+'mm'))

	#Background
	image.add(image.rect(insert=(0, 0),size=('100%', '100%'), rx=None, ry=None, fill=background_color))
	
	#draw guides
	generate_guides(northern,eastern)
	#Stars generation
	generate_starmap(northern,eastern,date,time)

	#Text in bottom corner

	image.add(image.text(info, insert=("20mm", str(height-21)+'mm'), fill=line_color, style=font_style))
	image.add(image.text(str(northern)+" N "+str(eastern)+" E " , insert=("20mm", str(height-17)+'mm'), fill=line_color, style=font_style))
	image.add(image.text(date +" "+ time, insert=("20mm", str(height-13)+'mm'), fill=line_color, style=font_style))


	image.save()
	print(output_file ," generated")

