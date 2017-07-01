

#LCD interface for Datalogger.
#Intented to autoexecute after booting.


##########IMPORTS###########################################
import time
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

#########SCRIPT CONST#######################################

# Raspberry Pi hardware SPI config:
DC = 3 #DC = 23
RST = 2 #RST = 24
SPI_PORT = 0
SPI_DEVICE = 0

# Raspberry Pi software SPI config:
# SCLK = 4
# DIN = 17
# DC = 23
# RST = 24
# CS = 8

# Beaglebone Black hardware SPI config:
# DC = 'P9_15'
# RST = 'P9_12'
# SPI_PORT = 1
# SPI_DEVICE = 0

# Beaglebone Black software SPI config:
# DC = 'P9_15'
# RST = 'P9_12'
# SCLK = 'P8_7'
# DIN = 'P8_9'
# CS = 'P8_11'

#########################################################################################

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

# Software SPI usage (defaults to bit-bang SPI interface):
#disp = LCD.PCD8544(DC, RST, SCLK, DIN, CS)

# Initialize library.
disp.begin(contrast=60)

# Clear display.
disp.clear()
disp.display()


#########FUNCT DEF########################################################

def Test():
	# Create blank image for drawing.
	# Make sure to create image with mode '1' for 1-bit color.
	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	
	# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)
	
	# Draw a white filled box to clear the image.
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
	
	# Load default font.
	font = ImageFont.load_default()

	#########logo screen a

	image = Image.open('logo_screen_a.png').resize((LCD.LCDWIDTH, LCD.LCDHEIGHT), Image.ANTIALIAS).convert('1')
	draw = ImageDraw.Draw(image)
	disp.image(image)
	disp.display()

	#clear screen	
	time.sleep(1.0)
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

	#########logo screen b

	image = Image.open('logo_screen_b.png').resize((LCD.LCDWIDTH, LCD.LCDHEIGHT), Image.ANTIALIAS).convert('1')
	draw = ImageDraw.Draw(image)
	disp.image(image)
	disp.display()

	#clear screen	
	time.sleep(1.0)
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

	#########logo screen c

	image = Image.open('logo_screen_c.png').resize((LCD.LCDWIDTH, LCD.LCDHEIGHT), Image.ANTIALIAS).convert('1')
	draw = ImageDraw.Draw(image)
	disp.image(image)
	disp.display()

	#clear screen	
	time.sleep(1.0)
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

	#########logo screen d

	image = Image.open('logo_screen_d.png').resize((LCD.LCDWIDTH, LCD.LCDHEIGHT), Image.ANTIALIAS).convert('1')
	draw = ImageDraw.Draw(image)
	disp.image(image)
	disp.display()

	#clear screen	
	time.sleep(4.0)
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

	######### credits screen #1 
	draw.text((8,5), 'Smart', font=font)
	draw.text((8,15), 'Automation', font=font)
	draw.text((8,25), 'Solutions', font=font)
	draw.text((8,35), '2016', font=font)

	# Display image.
	disp.image(image)
	disp.display()

	#clear screen	
	time.sleep(3.0)
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
	
	######### credits screen #2 
	draw.text((8,10), 'Datalogger', font=font)
	draw.text((8,20), 'v1.0', font=font)

	# Display image.
	disp.image(image)
	disp.display()

	#clear screen	
	time.sleep(3.0)
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

	######### credits screen #3 
	draw.text((8,10), 'System', font=font)
	draw.text((8,20), 'starting...', font=font)
	disp.image(image)
	disp.display()
	time.sleep(3.0)
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)


	######### status screen

	draw.text((3,10), 'Status=online', font=font)
	disp.image(image)
	disp.display()	

	#########

#####print credits
def PrintCredits():

	# Create blank image for drawing.
	# Make sure to create image with mode '1' for 1-bit color.
	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))

	# Get drawing object to draw on image.
	draw = ImageDraw.Draw(image)

	font = ImageFont.load_default()
	draw.text((8,30), 'SAS.SA', font=font)
	# Display image.
	disp.image(image)
	disp.display()

############END OF FUNCT TEST########################################################

#PrintCredits()
Test()

print 'Press Ctrl-C to quit.'
while True:
	time.sleep(1.0)
