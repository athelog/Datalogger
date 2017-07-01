#!/usr/bin/python

# Script to set Raspberry Unix clock from RTC chip 1302
# The scripts its intended to be called by /etc/rc.local to autoexecute when RPi boots

  
##############IMPORTS############################################
import RTC_DS1302
import os


#############FUNCT DEF###########################################

###read datetime from RTC chip and set server datetime accordingly
def SetServerDatetime():

	# Create an instance of the RTC class.
	ThisRTC = RTC_DS1302.RTC_DS1302()
	
	# Functions to read from the RTC chip.
	Data = ThisRTC.ReadRAM()
	print("Message: " + Data)
	
	DateTime = { "Year":0, "Month":0, "Day":0, "DayOfWeek":0, "Hour":0, "Minute":0, "Second":0 }
	Data = ThisRTC.ReadDateTime(DateTime) #read chip data
		
	Year=format(DateTime["Year"] + 2000, "04d")
	Month=format(DateTime["Month"], "02d")
	Day=format(DateTime["Day"], "02d")
	DayOfWeek=ThisRTC.DOW[DateTime["DayOfWeek"]]
	Hour=format(DateTime["Hour"], "02d")
	Minute=format(DateTime["Minute"], "02d")
	Second=format(DateTime["Second"], "02d")
		
	#setting system date thru unix command
	command_string="sudo date -s '"+Year+"-"+Month+"-"+Day+" "+Hour+":"+Minute+":"+Second+"'"
	print "command_string="+command_string
	os.system(command_string)

	print("Date/Time: " + Data)
	print("Year: " + Year)
	print("Month: " + Month)
	print("Day: " + Day)
	print("DayOfWeek: " + DayOfWeek)
	print("Hour: " + Hour)
	print("Minute: " + Minute)
	print("Second: " + Second)
	
	# Finish with the Raspberry Pi GPIO pins.
	ThisRTC.CloseGPIO()

#############END OF FUNCT DEF####################################

#############SCRIPT EXECUTION####################################
SetServerDatetime()




