#!/usr/bin/env python

##########README##########################################
#LCD interface for Datalogger.
#Intented to autoexecute after booting.


##########IMPORTS###########################################
import time
import Adafruit_Nokia_LCD as LCD
import Adafruit_GPIO.SPI as SPI
import PIL
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
import os
import glob
import multiprocessing as mp
import tty
import termios
import sys

#########SCRIPT CONST - USER CAN MODIFY #######################################

Debug_Flag="DEEP"
masterfile_path="../database/" #masterfile relative path
MainLoopDelay=60 #amount in seconds of main loop 


# Raspberry Pi hardware SPI config:
DC = 3 #DC = 23
RST = 2 #RST = 24
SPI_PORT = 0
SPI_DEVICE = 0


#########SCRIPT CONST - DON'T TOUCH############################################

# Hardware SPI usage:
disp = LCD.PCD8544(DC, RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=4000000))

menu_status="default" #menu control var
toggle="False"

#########FUNCT DEF########################################################

####prepare LCD
def LCDInit():

	
	global disp
	
	# Initialize library.
	disp.begin(contrast=60)
	
	# Clear display.
	disp.clear()
	disp.display()


####starting screen in LCD
def PrintCredits():
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

	image = Image.open('/usr/lib/cgi-bin/lcd/content/logo_screen_a.png').resize((LCD.LCDWIDTH, LCD.LCDHEIGHT), Image.ANTIALIAS).convert('1')
	draw = ImageDraw.Draw(image)
	disp.image(image)
	disp.display()

	#clear screen	
	time.sleep(1.0)
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

	#########logo screen b

	image = Image.open('/usr/lib/cgi-bin/lcd/content/logo_screen_b.png').resize((LCD.LCDWIDTH, LCD.LCDHEIGHT), Image.ANTIALIAS).convert('1')
	draw = ImageDraw.Draw(image)
	disp.image(image)
	disp.display()

	#clear screen	
	time.sleep(1.0)
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

	#########logo screen c

	image = Image.open('/usr/lib/cgi-bin/lcd/content/logo_screen_c.png').resize((LCD.LCDWIDTH, LCD.LCDHEIGHT), Image.ANTIALIAS).convert('1')
	draw = ImageDraw.Draw(image)
	disp.image(image)
	disp.display()

	#clear screen	
	time.sleep(1.0)
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

	#########logo screen d

	image = Image.open('/usr/lib/cgi-bin/lcd/content/logo_screen_d.png').resize((LCD.LCDWIDTH, LCD.LCDHEIGHT), Image.ANTIALIAS).convert('1')
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

####printing latest product data in LCD. list_to_print=[Product,Code,IP,Date,Time]
def PrintLatestData(list_to_print):
	
	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	draw = ImageDraw.Draw(image)

	#clearing screen
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

	font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf',10)
	draw.text((3,0), '--Latest data--', font=font)
	font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
	draw.text((0,10), 'Code='+list_to_print[1], font=font)
	draw.text((0,18), 'IP='+list_to_print[2], font=font)
	draw.text((0,26), 'Date='+list_to_print[3], font=font)
	draw.text((0,34), 'Time='+list_to_print[4], font=font)

	# Display image.
	disp.image(image)
	disp.display()

####printing system online screen and menu
def PrintSysOnline():

	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	draw = ImageDraw.Draw(image)

	#clearing screen
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

	font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf',11)
	draw.text((3,0), 'Server online', font=font)
	font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',10)
	draw.text((3,20), 'Press <ENTER>', font=font)	
	draw.text((3,30), 'for Menu', font=font)	

	# Display image.
	disp.image(image)
	disp.display()	

#####returns index of latest masterfile. In case of error returns -1.
def GetMasterfileIndex():

	index = -1 #default value
	if (Debug_Flag=="DEEP"):print "<br><br><b>Executting Function GetMasterfileIndex. Debug_Flag=</b>"+Debug_Flag

	#checking that database path exists
  	if (os.path.isdir(masterfile_path)==True):

		if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br>--Database path is valid="+masterfile_path
	else:
		if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br>--ERROR:Database path is invalid="+masterfile_path

	#storing masterfiles names in list
	filenames_list=glob.glob(masterfile_path+"*.csv")
	#if (Debug_Flag=="DEEP"):print "<br>--Masterfiles="+str(filenames_list)

	#checking if database folder is empty. If so, return 0
	if not filenames_list:
		if (Debug_Flag=="DEEP" or Debug_Flag=="NORMAL"):print "<br>--Folder is empty. Created masterfile 0."
		index=0

	###for-checking the masterfiles
	for masterfile in filenames_list:
		
		split_list = masterfile.split("_") #segregating the masterfile number
		#if (Debug_Flag=="DEEP"):print "<br>--For masterfile="+masterfile+ the index is="+split_list[1]	

		if (int(split_list[1])>index):index=int(split_list[1])

	###end of for	

	if (Debug_Flag=="DEEP"):print "<br><b>Finished Function GetMasterfileIndex. Debug_Flag=</b>"+Debug_Flag+". Return="+str(index)
	return index

######get latest sample/IP/datetime to show in LCD. Returns a list with the tokens expected, otherwise return empty list
def GetLatestData(filenumber):
	
	return_list=[]
	split_list=[]
	global masterfile_path
	command_string="tail -n1 "+masterfile_path+"masterfile_"+str(filenumber)+"_.csv"
	if (Debug_Flag=="DEEP"): print "<br>--Command string="+command_string
	command = os.popen(command_string)
	command_result=command.read() 
	if (Debug_Flag=="DEEP"): print "<br>--Command execution result="+command_result

	#check integrity of data
	if (command_result!=""):

		split_list=command_result.split(",")
	
		#latest info arrived to dB
		Product="NA"
		Code=split_list[3]		
		Date=split_list[7]
		Time=split_list[8]
		IP=split_list[9].strip()
		return_list.append(Product)
		return_list.append(Code)
		return_list.append(IP)
		return_list.append(Date)
		return_list.append(Time)

	return return_list

###printing main menu. The argument represents the highlighted item
def PrintMain(item):

	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	draw = ImageDraw.Draw(image)

	#clearing screen
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

	font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf',10)
	draw.text((3,0), 'Main menu', font=font)

	if (item=="about"):	
	
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-BoldItalic.ttf',9)
		draw.text((3,10), '>About', font=font)	
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)	
		draw.text((3,20), 'Advanced', font=font)
		draw.text((3,30), 'Show last data', font=font)
		draw.text((3,40), 'Back', font=font)

	elif(item=="advanced"):	

		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
		draw.text((3,10), 'About', font=font)	
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-BoldItalic.ttf',9)	
		draw.text((3,20), '>Advanced', font=font)
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
		draw.text((3,30), 'Show last data', font=font)
		draw.text((3,40), 'Back', font=font)	

	elif(item=="show_last_data"):	

		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
		draw.text((3,10), 'About', font=font)
		draw.text((3,20), 'Advanced', font=font)	
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-BoldItalic.ttf',9)
		draw.text((3,30), '>Show last data', font=font)
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
		draw.text((3,40), 'Back', font=font)

	elif(item=="back"):	

		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
		draw.text((3,10), 'About', font=font)
		draw.text((3,20), 'Advanced', font=font)
		draw.text((3,30), 'Show last data', font=font)	
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-BoldItalic.ttf',9)
		draw.text((3,40), '>Back', font=font)		

	#end of if/else 	

	# Display image.
	disp.image(image)
	disp.display()	

###print about info
def PrintAbout():

	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	draw = ImageDraw.Draw(image)

	#clearing screen
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

	font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf',10)
	draw.text((3,0), '--About--', font=font)
	font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
	draw.text((3,10), 'Datalogger v1.0', font=font)
	draw.text((3,20), 'SAS.SA - 2016', font=font)
	draw.text((3,30), 'www.SASSA.com', font=font)
	font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-BoldItalic.ttf',9)
	draw.text((3,30), 'www.SASSA.com', font=font)

	# Display image.
	disp.image(image)
	disp.display()	

####print Advanced Menu
def PrintAdvanced(option):

	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

	font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf',10)
	draw.text((3,0), 'Advanced', font=font)

	if (option=="restart"):

		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-BoldItalic.ttf',9)
		draw.text((3,10), '>Restart', font=font)
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
		draw.text((3,20), 'Shutdown', font=font)
		draw.text((3,30), 'Back', font=font)

	elif (option=="shutdown"):

		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
		draw.text((3,10), 'Restart', font=font)
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-BoldItalic.ttf',9)
		draw.text((3,20), '>Shutdown', font=font)
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
		draw.text((3,30), 'Back', font=font)

	elif (option=="back"):

		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
		draw.text((3,10), 'Restart', font=font)
		draw.text((3,20), 'Shutdown', font=font)
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-BoldItalic.ttf',9)
		draw.text((3,30), '>Back', font=font)

	else:
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf',9)
		draw.text((3,20), 'ERROR:', font=font)
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
		draw.text((3,30), 'Invalid input', font=font)	

	# Display image.
	disp.image(image)
	disp.display()	



###print Advanced Menu
def PrintAdvancedEnterPin(N):

	#preparing screen
	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	draw = ImageDraw.Draw(image)
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

	if (N=="0"):
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf',10)
		draw.text((3,10), 'Enter pin:', font=font)

	elif (N=="1"):
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf',10)
		draw.text((3,10), 'Enter pin:', font=font)	
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
		draw.text((3,20), '*', font=font)

	elif (N=="2"):
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf',10)
		draw.text((3,10), 'Enter pin:', font=font)	
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
		draw.text((3,20), '**', font=font)

	elif (N=="3"):
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf',10)
		draw.text((3,10), 'Enter pin:', font=font)	
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
		draw.text((3,20), '***', font=font)

	elif (N=="4"):
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf',10)
		draw.text((3,10), 'Enter pin:', font=font)	
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
		draw.text((3,20), '****', font=font)	

	else:
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf',10)
		draw.text((3,10), 'DEBUG. ERROR 2115', font=font)	
		font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
		draw.text((3,20), 'Invalid input', font=font)		

	# Display image.
	disp.image(image)
	disp.display()	

###if pin in invalid in advanced screen
def PrintAdvancedInvalidPin():

	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	draw = ImageDraw.Draw(image)

	#clearing screen
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)

	font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf',10)
	draw.text((3,10), 'ERROR:', font=font)	
	font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Regular.ttf',9)
	draw.text((3,20), 'Wrong Pin!', font=font)
	font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-BoldItalic.ttf',9)
	draw.text((3,30), '>Back', font=font)

	# Display image.
	disp.image(image)
	disp.display()

###restarting screen
def PrintRestarting():

	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	draw = ImageDraw.Draw(image)

	#clearing screen
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
	font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf',10)
	draw.text((3,20), 'Restarting...', font=font)
	
	# Display image.
	disp.image(image)
	disp.display()	

####shutdown message
def PrintShuttingDown():

	image = Image.new('1', (LCD.LCDWIDTH, LCD.LCDHEIGHT))
	draw = ImageDraw.Draw(image)

	#clearing screen
	draw.rectangle((0,0,LCD.LCDWIDTH,LCD.LCDHEIGHT), outline=255, fill=255)
	font= ImageFont.truetype('/usr/share/fonts/truetype/droid/DroidSerif-Bold.ttf',10)
	draw.text((3,15), 'Shutting', font=font)
	draw.text((3,25), 'down...', font=font)
	
	# Display image.
	disp.image(image)
	disp.display()	

#####default screen, showing latest sample and then status
def PrintDefaultScreen():

	PrintSysOnline()


###shutdown Rasperry Pi
def Shutdown():
	command_string="sudo halt"

###restart Raspberry Pi
def Restart():
	command_string="sudo reboot"
	os.system(command_string)	

####key control for menu status
def KeyControl():

	global menu_status
	GetKey=str(getKey())
	if (GetKey=="\n"):GetKey="ENTER"

		#############LCD menu control - user var #############################
	if (menu_status=="default"):		
		if (GetKey=="ENTER"):
			menu_status="main_about"

	elif (menu_status=="main_about"):
		if (GetKey=="ENTER"):menu_status="about"
		elif (GetKey=="2"):menu_status="main_advanced"
		elif (GetKey=="8"):menu_status="main_back"
			 	
	elif (menu_status=="about"):
		if (GetKey=="ENTER"):menu_status="main_about"
	
	elif (menu_status=="main_advanced"):
		if (GetKey=="ENTER"):menu_status="advanced_enter_pin0"
		elif (GetKey=="2"):menu_status="main_show_last_data"
		elif (GetKey=="8"):menu_status="main_about"
	
	elif (menu_status=="advanced_enter_pin0"):
		if (GetKey=="1"):menu_status="advanced_enter_pin1"
		elif (GetKey=="2"):menu_status="advanced_enter_pin1"
		elif (GetKey=="3"):menu_status="advanced_enter_pin1"
		elif (GetKey=="4"):menu_status="advanced_enter_pin1"
		elif (GetKey=="5"):menu_status="advanced_enter_pin1"
		elif (GetKey=="6"):menu_status="advanced_enter_pin1"
		elif (GetKey=="7"):menu_status="advanced_enter_pin1"	
		elif (GetKey=="8"):menu_status="advanced_enter_pin1"

	elif (menu_status=="advanced_enter_pin1"):
		if (GetKey=="1"):menu_status="advanced_enter_pin2"
		elif (GetKey=="2"):menu_status="advanced_enter_pin2"
		elif (GetKey=="3"):menu_status="advanced_enter_pin2"
		elif (GetKey=="4"):menu_status="advanced_enter_pin2"
		elif (GetKey=="5"):menu_status="advanced_enter_pin2"
		elif (GetKey=="6"):menu_status="advanced_enter_pin2"
		elif (GetKey=="7"):menu_status="advanced_enter_pin2"	
		elif (GetKey=="8"):menu_status="advanced_enter_pin2"

	elif (menu_status=="advanced_enter_pin2"):
		if (GetKey=="1"):menu_status="advanced_enter_pin3"
		elif (GetKey=="2"):menu_status="advanced_enter_pin3"
		elif (GetKey=="3"):menu_status="advanced_enter_pin3"
		elif (GetKey=="4"):menu_status="advanced_enter_pin3"
		elif (GetKey=="5"):menu_status="advanced_enter_pin3"
		elif (GetKey=="6"):menu_status="advanced_enter_pin3"
		elif (GetKey=="7"):menu_status="advanced_enter_pin3"	
		elif (GetKey=="8"):menu_status="advanced_enter_pin3"

	elif (menu_status=="advanced_enter_pin3"):
		if (GetKey=="1"):menu_status="advanced_enter_pin4"
		elif (GetKey=="2"):menu_status="advanced_enter_pin4"
		elif (GetKey=="3"):menu_status="advanced_enter_pin4"
		elif (GetKey=="4"):menu_status="advanced_enter_pin4"
		elif (GetKey=="5"):menu_status="advanced_enter_pin4"
		elif (GetKey=="6"):menu_status="advanced_enter_pin4"
		elif (GetKey=="7"):menu_status="advanced_enter_pin4"	
		elif (GetKey=="8"):menu_status="advanced_enter_pin4"

	elif (menu_status=="advanced_enter_pin4"):
		if (1==1):menu_status="advanced_restart"

	elif (menu_status=="advanced_invalid_pin"):
		if (GetKey=="ENTER"):menu_status="main_advanced"

	elif (menu_status=="advanced_restart"):
		if (GetKey=="ENTER"):menu_status="restart"
		elif (GetKey=="2"):menu_status="advanced_shutdown"
		elif (GetKey=="8"):menu_status="advanced_back"

	elif (menu_status=="advanced_shutdown"):
		if (GetKey=="ENTER"):menu_status="shutdown"
		elif (GetKey=="2"):menu_status="advanced_back"
		elif (GetKey=="8"):menu_status="advanced_restart"

	elif (menu_status=="advanced_back"):
		if (GetKey=="ENTER"):menu_status="main_about"
		elif (GetKey=="2"):menu_status="advanced_restart"
		elif (GetKey=="8"):menu_status="advanced_shutdown"

	elif (menu_status=="restart"):
		menu_status="restarting"
		Restart()

	elif (menu_status=="shutdown"):
		menu_status="shuttingdown"
		ShutDown()

	elif (menu_status=="main_show_last_data"):
		if (GetKey=="ENTER"):menu_status="show_last_data"
		elif (GetKey=="8"):menu_status="main_advanced"
		elif (GetKey=="2"):menu_status="main_back"

	elif (menu_status=="show_last_data"):
		if (GetKey=="ENTER"):menu_status="main_about"

	elif (menu_status=="main_back"):
		if (GetKey=="ENTER"):menu_status="default"
		elif (GetKey=="8"):menu_status="main_show_last_data"
		elif (GetKey=="2"):menu_status="main_about"

	else: menu_status="default"

	print "Executing KeyControl. GetKey="+GetKey+". status="+menu_status
	return GetKey	

#############LCD menu control - function call #############################
def PrintMenuControl():

	global menu_status
	print "Debug. Executing PrintMenuControl. menu_status="+menu_status

	if (menu_status=="default"):
		PrintDefaultScreen()		

	elif (menu_status=="main_about"):
		PrintMain("about")
			 	
	elif (menu_status=="about"):
		PrintAbout()
	
	elif (menu_status=="main_advanced"):
		PrintMain("advanced")	

	elif (menu_status=="advanced_enter_pin0"):
		PrintAdvancedEnterPin("0")

	elif (menu_status=="advanced_enter_pin1"):
		PrintAdvancedEnterPin("1")

	elif (menu_status=="advanced_enter_pin2"):
		PrintAdvancedEnterPin("2")

	elif (menu_status=="advanced_enter_pin3"):
		PrintAdvancedEnterPin("3")

	elif (menu_status=="advanced_enter_pin4"):
		PrintAdvancedEnterPin("4")

	elif (menu_status=="advanced_invalid_pin"):
		PrintAdvancedInvalidPin()

	elif (menu_status=="advanced_restart"):
		PrintAdvanced("restart")

	elif (menu_status=="advanced_shutdown"):
		PrintAdvanced("shutdown")

	elif (menu_status=="advanced_back"):
		PrintAdvanced("back")

	elif (menu_status=="restart"):
		PrintRestarting()
		Restart()

	elif (menu_status=="shutdown"):
		PrintShuttingDown()
		Shutdown()	

	elif (menu_status=="main_show_last_data"):
		PrintMain("show_last_data")

	elif (menu_status=="show_last_data"):
		info_list=[]
		MasterFileIndex=GetMasterfileIndex()	
		if (Debug_Flag=="DEEP"):print "Debug. MasterFileIndex="+str(MasterFileIndex)
		info_list=GetLatestData(MasterFileIndex)
		PrintLatestData(info_list)

	elif (menu_status=="main_back"):
		PrintMain("back")

	else: menu_status="default"

###capture key

def getKey():
	fd=sys.stdin.fileno()
	old=termios.tcgetattr(fd)
	new=termios.tcgetattr(fd)
	new[3]=new[3] & ~termios.ICANON & ~termios.ECHO
	new[6][termios.VMIN]=1
	new[6][termios.VTIME]=0
	termios.tcsetattr(fd,termios.TCSANOW,new)
	key=new

	try:
		key=os.read(fd,3)
	finally:
		termios.tcsetattr(fd,termios.TCSAFLUSH,old)

	return key

###
def Loop():

	while True:
		print "Debug. Looping!"
		time.sleep(60)

	


#####main
def main():
	
	global menu_status,toggle

	#info_list=[]
	#MasterFileIndex=GetMasterfileIndex()	
	#if (Debug_Flag=="DEEP"):print "Debug. MasterFileIndex="+str(MasterFileIndex)
	#info_list=GetLatestData(MasterFileIndex)

	looping=True

	print "status="+menu_status

	PrintMenuControl()

	###########################################menu control thread#########################
	menu_process=mp.Process(target=Loop)
	menu_process.start()	
	
	while True:
		toggle=KeyControl()
		if (toggle!="False"):PrintMenuControl()
		toggle="False"

	PrintMenuControl()
	print "alive="+ str(menu_process.is_alive())
	#if (menu_process.is_alive()==True):menu_process.run()
	#menu_process.terminate()


############END OF FUNCT TEST########################################################

LCDInit()
PrintCredits()
main()


