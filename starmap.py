
import svgwrite
import random 
import math

PI = 3.141592

#Stars declination and hour data file "Yale Bright Star Catalog 5"
file = "ybsc5.txt"
file2 = "stardata.txt"

background_color = "rgb(45,59,98)"
background_color = "rgb(0,0,0)"
line_color = "rgb(255,255,255)"

#ISO 8601 standard 
#2017-06-30T09:46:13+00:00

#Date & Time
time ='21.09.2017 23.59'

utc = +2 #Coordinated Universal Time CUT?
summertime = False

#error bias in time
correction = -16.7
utc += correction

#Coordinates
northern,eastern = 45.28,11.08



#placetext for leftdown corner
place = 'HELSINKI'

#Size of poster in mm
width = 200
height = 200

#Smaller the star bigger the magnitude
magnitude_limit = 4.5
aperture = 0.2 

animation = False
amplification = width*0.015

def weekday(date_time,lang):

	month_day_add = [0,3,3,6,1,4,6,2,5,0,3,5]
	days_en = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
	days_fi = ['Maanantai','Tiistai','Keskiviikko','Torstai','Perjantai','Lauantai','Sunnuntai']

	day = int(date_time[0:2])
	month = int(date_time[3:5])
	year = int(date_time[6:10])

	print(day,month,year)
	
	#		vuosi		karkausvuosi	paiva 	kuukausi					lauantai
	add = (	year-2000 +(year-2000)//4 + day-1 + month_day_add[month-1] + 	6) % 7

	#karkausvuosi specialcase
	if year % 4 == 0 and month < 3:
		add -= 1

	print(days_fi[add])

def mm_to_px(mm):
	px = mm*96/25.4
	return px

#read data from file to nested list
def read_star_coordinate_file(file):
	data = []
	with open(file, 'rt') as f:
		for line in f:
			if (',' in line): 
				data.append([ n for n in line.strip().split(',')])
	return data

#change polar coordinates to cartesian coordinates
def polar_to_cartesian(radius,angle,centerx,centery):
	return [centerx + radius*math.cos(angle), centery + radius*math.sin(angle)]


# Generates random star shape to given coordinate and magnitude and color
def star_generator(x,y,mag,color):

	# randomize the points of star
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

	#animation
	if(animation):
		stars.add(image.animateTransform("rotate","transform",id="star",from_="0 "+ str(half_x)+ " "+ str(half_y), to="360 "+ str(half_x)+ " "+ str(half_y),dur="60s",begin="0s",repeatCount="indefinite"))

def dot_generator(x,y,mag,color):
	image.add(image.circle((x,y),mag,id ='dot',stroke="none",fill=color))

#date to days
def date_and_time_to_rad(date_time):

	days_in_year = 365 # days in normal year
	months = [31,28,31,30,31,30,31,31,30,31,30,31] #Array of days in months
	year = int(date_time[6:10])
	
	#Leap year
	if(year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)):
		months[1] = 29 
		days_in_year = 366

	#TODO yearly mistake epoch
	degree = -(year-2000)*360/26000
	

	days  = sum(months[0:int(date_time[3:5])-1])	#month to days
	days += int(date_time[0:2])-1					#days

	#calculate degree from days
	degree += (days)*360.0/days_in_year

	minutes  = float(date_time[11:13])*60  			#hour
	minutes += float(date_time[14:16])	  			#minute

	#Summertime
	if(summertime):
		minutes -= 60

	#UTC
	minutes -= 60*utc

	#calculate degree from minutes
	degree += (minutes*360/(24*60-4)) % 360

	return math.radians(degree)


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
    delta_ra = ra_angle - east
    x = math.cos(dec_angle) * math.sin(delta_ra)
    y = math.sin(dec_angle) * math.cos(north) - math.cos(dec_angle) * math.cos(delta_ra) * math.sin(north)
    return x * 300 ,y * 300


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
		magn = 0.7
		radius = distance_between(N,E,declination,ascension)
		x,y = rad_to_xy(N,E,declination,ascension)

		if (radius < (90*PI/180.0)):
			dot_generator(half_x+x,half_y+y,magn*aperture,line_color)

def generate_starmap(northern_N,eastern_E,date_time):

	data = read_star_coordinate_file(file2)
	N = math.radians(northern_N)
	E = math.radians(eastern_E)


	for line in data:
		if(float(line[2]) < magnitude_limit):
		# if(float(line[5]) < magnitude_limit):

			#star position from datafile
			# ascension = right_ascension_to_rad(hours_to_decimal(line[0]))
			ascension = right_ascension_to_rad(float(line[0]))+ date_and_time_to_rad(date_time)
			declination = declination_to_rad(line[1])

			x,y = rad_to_xy(N,E,declination,ascension)
			radius = distance_between(N,E,declination,ascension)

			#magnitude of star
			magn = float(line[2])
			# print magn
			magn = 6 - 2.5*math.log(2+magn,10)



			if (radius < 89*PI/180.0):
				if (magn < 3):
					dot_generator(half_x+x,half_y+y,0.4*aperture,line_color)
				else:
					star_generator(half_x+x,half_y+y,magn*aperture,line_color)

				#North Star 
				if(declination > 89.1*PI/180.0):
				 	star_generator(half_x+x,half_y+y,magn*aperture,"red")



if __name__ == '__main__':

	half_x = mm_to_px(width/2)
	half_y = mm_to_px(height/2)
	weekday(time,'fi')
	#Svgfile 
	image = svgwrite.Drawing('tahtikartta.svg',size=(str(width)+'mm',str(height)+'mm'))

	#Background
	image.add(image.rect(insert=(0, 0),size=('100%', '100%'), rx=None, ry=None, fill=background_color))
	
	#draw guides
	generate_guides(northern,eastern)
	#Stars generation
	generate_starmap(northern,eastern,time)

	#Text in bottom corner
	font_style = "font-size:10px; letter-spacing:0.7px; font-family:sans-serif; stroke-width:5;font-weight:bold;"
	image.add(image.text(place, insert=("20mm", str(height-21)+'mm'), fill=line_color, style=font_style))
	image.add(image.text(str(northern)+" N "+str(eastern)+" E " , insert=("20mm", str(height-17)+'mm'), fill=line_color, style=font_style))
	image.add(image.text(time, insert=("20mm", str(height-13)+'mm'), fill=line_color, style=font_style))


	image.save()

