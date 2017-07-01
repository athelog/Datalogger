import cgi
import cgitb
import sys
import os
import csv
import string
import urllib
import time
import datetime
import math
import shutil
import subprocess
import fileinput
#from common_functs import *

import io

import matplotlib.pyplot as plt
plt.rcdefaults()
import numpy as np
#import matplotlib.pyplot as plt

####enabling debugging#######################################################

#cgitb.enable()

#######################################SCRIPT CONSTS##########################

Debug_Flag = "NONE" #DEEP,NONE
Url="192.168.10.104/cgi-bin/products.py" #basic url of script
language = "SP" #SP=spanish, ENG=english
report_dir="/usr/lib/cgi-bin/report/" #FIXME: move this to general settings file
report_filename="report.csv"

########################################SCRIPT VARS - DON'T TOUCH#############

	
	



########################################

###BarPlot(): function to create bar graphic
def BarPlot():	

	people	= ('Ramiro','Allan','Jose','Herminildo')
	y_pos = np.arange=(len(people))
	performance=3+10*np.random.rand(len(people))	
	error=np.random.rand(len(people))

	plt.barh(y_pos,performance,xerr=error,align='center',alpha=0.4)
	#plt.yticks(y_pos,people)
	#plt.xlabel('Performance')	
	#plt.title('Example of bar plot')
	#plt.show()


###end of BarPlot()

def main():

	#Read values
	data=[1,2,3,4,5]
	dates=[1,2,3,4,5]

	
	matplotlib.rcParams['timezone'] = 'US/Eastern'	

	#set up plot
	fig, ax = plt.subplots(figsize=(6,5))
	ax.plot_date(dates,data,ls='-',color='red')
	#ax.xaxis.set_major_formatter(DateFormatter('))

	#read the number of hours argument and set xlim
	arg=cgi.FieldStorage()	
	
	try:
		h=int(arg.getvalue('hrs','-1'))
	except:
		h=-1
	if h>0:
		ax.set_xlim(matplotlib.dates.epoch2num(data[-1,0]-h*3600),ax.get_xlim()[1])

	#Finish plot

	ax.set_ylabel('Temperature')
	#for label in ax.get_xticklabels():
	#	label.set_rotation(60)
	plt.tight_layout()

	#save image to buffer
	buf=io.BytesIO()		
	fig.savefig(buf, format='png')
	out=buf.getvalue()
	buf.close()
	print 'Content-Type: image/png\n'
	print out


##############

#print "date time="+str(datetime.datetime())
#main()
BarPlot()





