#!/usr/bin/python

#######1.IMPORTS###################################

import RPi.GPIO as GPIO
import time

#######END OF IMPORTS############################


######2.SCRIPT CONST###############################

LCD_RS=18
LCD_E=23
LCD_D4=24
LCD_D5=25
LCD_D6=4
LCD_D7=17
LCD_WIDTH=16
LCD_CHR=True
LCD_CMD=False
LCD_LINE_1=0x80
LCD_LINE_2=0xC0
E_PULSE=0.0005
E_DELAY=0.0005

#######END OF SCRIPT CONST######################

#######3.FUNCT DEFINITON##########################

###main
def main():
	GPIO.setwarnings(False)
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(LCD_E,GPIO.OUT)#E
	GPIO.setup(LCD_RS,GPIO.OUT)#RS
	GPIO.setup(LCD_D4,GPIO.OUT)#D4
	GPIO.setup(LCD_D5,GPIO.OUT)#D5
	GPIO.setup(LCD_D6,GPIO.OUT)#D6
	GPIO.setup(LCD_D7,GPIO.OUT)#D7

	lcd_init()

	while True:

		#testing
		lcd_string("Datalogger v1.0",LCD_LINE_1)
		lcd_string("SAS.SA - 2015",LCD_LINE_2)
		time.sleep(3) #delay in seconds	

		#send some text
		lcd_string("Status=online",LCD_LINE_1)
		lcd_string("System running",LCD_LINE_2)
		time.sleep(3) #delay in seconds				

	#end of while

###initializating LCD
def lcd_init():
	lcd_byte(0x33,LCD_CMD)
	lcd_byte(0x32,LCD_CMD)
	lcd_byte(0x06,LCD_CMD)
	lcd_byte(0x0C,LCD_CMD)
	lcd_byte(0x28,LCD_CMD)
	lcd_byte(0x01,LCD_CMD)
	time.sleep(E_DELAY)

###print data
def lcd_byte(bits,mode):

	GPIO.output(LCD_RS,mode)

	#sending hight bits
	GPIO.output(LCD_D4,False)
	GPIO.output(LCD_D5,False)
	GPIO.output(LCD_D6,False)
	GPIO.output(LCD_D7,False)
	if bits&0x10==0x10:GPIO.output(LCD_D4,True)
	if bits&0x20==0x20:GPIO.output(LCD_D5,True)
	if bits&0x40==0x40:GPIO.output(LCD_D6,True)
	if bits&0x80==0x80:GPIO.output(LCD_D7,True)
	lcd_toggle_enable()

	GPIO.output(LCD_D4,False)
	GPIO.output(LCD_D5,False)
	GPIO.output(LCD_D6,False)
	GPIO.output(LCD_D7,False)
	if bits&0x01==0x01:GPIO.output(LCD_D4,True)
	if bits&0x02==0x02:GPIO.output(LCD_D5,True)
	if bits&0x04==0x04:GPIO.output(LCD_D6,True)
	if bits&0x08==0x08:GPIO.output(LCD_D7,True)
	lcd_toggle_enable()
	

###toggle enable
def lcd_toggle_enable():
	time.sleep(E_DELAY)
	GPIO.output(LCD_E,True)
	time.sleep(E_PULSE)
	GPIO.output(LCD_E,False)
	time.sleep(E_DELAY)	

###print string in LCD
def lcd_string(message,line):
	message=message.ljust(LCD_WIDTH," ")
	lcd_byte(line,LCD_CMD)

	for i in range(LCD_WIDTH):
		lcd_byte(ord(message[i]),LCD_CHR)

#######END OF FUNCT DEFINITION##################

#######SCRIPT EXECUTION#########################

if __name__=='__main__':

	try:main()
	except KeyboardInterrupt:pass
	finally:
		lcd_byte(0x01,LCD_CMD)
		lcd_string("Bye!",LCD_LINE_1)
		GPIO.cleanup()			













