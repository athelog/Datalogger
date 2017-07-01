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


#plt.rcdefaults()
#import numpy as np
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



def ScatterPlot():

	#imports
	import matplotlib.pyplot as plt	

	y=[5,6,8,5,7,8,9,10,5,7]
	x=[1,2,3,4,5,6,7,8,9,10]	
	plt.scatter(x,y)
	#plt.show() #this popups a window with popup window
	plt.savefig("/usr/lib/cgi-bin/tests/graphic_analysis/aaa") #save img to file


	
#end of ScatterPlot()

def BarPlot():

	#imports
	import matplotlib.pyplot as plt	

	y=[1,2,3,4,5]
	x=[10,20,15,35,60]	
	plt.bar(x,y)
	#plt.show() #this popups a window with popup window
	plt.savefig("/usr/lib/cgi-bin/tests/graphic_analysis/bbb") #save img to file
	plt.close()
	
#end of BarPlot()

#bar grpahic
def BarPlot2():

	#imports
	from  pylab import *	

	y=[10,20,35,40,25]
	x=[1,2,3,4,5] # position of x labels (yticks)
	yticks(x,('T1','T2','T3','T4','J'))
	barh(x,y, align='center')
	#plt.show() #this popups a window with plot
	plt.savefig("/usr/lib/cgi-bin/tests/graphic_analysis/bar20") #save img to file
	plt.close()
	
#end of BarPlot2()

#bar graphic
def BarPlot3():

	#imports
	from  pylab import *	

	y=[10,20,35,40,25]
	x=[1,2,3,4,5] # position of x labels (yticks)
	xticks(x,('Ramiro','Esteban','Julian','Elle','Sophie'))
	bar(x,y, align='center')
	#plt.show() #this popups a window with plot
	plt.savefig("/usr/lib/cgi-bin/tests/graphic_analysis/bar3") #save img to file
	plt.close()
	
#end of BarPlot3()

#histogram plot
def HistogramPlot_():

	
	#imports
	#import numpy as np
	import scipy.stats as stats
	#import pylab as pl
	
	import matplotlib.pyplot as plt
	import numpy as np
	#import plotly.plotly as py
	

	values=sorted([10,11,11,10,19,20,15,20,21,16,11,40,15,8,7,9,10,12,13,13,8,7,25,26,31,18,20,21,19,30,25])

	fit=stats.norm.pdf(values,np.mean(values),np.std(values))
	
	#pl.plot(values,fit,'-o')
	plt.hist(values)
	plt.savefig("/usr/lib/cgi-bin/tests/graphic_analysis/hist") #save img to file
	#pl.show()
	pl.close()

#end of HistogramPlot():

#histogram plot
def HistogramPlot():

	
	import scipy.stats as stats	
	import matplotlib.pyplot as plt
	import numpy as np

	print "Executing HistogramPlot"

	values=sorted([10,11,11,10,19,20,15,20,21,16,11,40,15,8,7,9,10,12,13,13,8,7,25,26,31,18,20,21,19,30,25])

	#values=[10,11,11,10,19,20,15,20,21,16,11,40,15,8,7,9,10,12,13,13,8,7,25,26,31,18,20,21,19,30,25]

	fit=stats.norm.pdf(values,np.mean(values),np.std(values))
	
	bins = np.linspace(-10,10,100)
	
	plt.hist(values,bins)

	#pl.plot(values,fit,'-o')
	plt.hist(values)
	#plt.savefig("/usr/lib/cgi-bin/tests/graphic_analysis/hist") #save img to file
	plt.show()
	#plt.close()

#end of HistogramPlot():

def HistogramPlot3():

	import matplotlib.pyplot as plt
	import numpy as np
	#import plotly.plotly as py

	gaussian=np.random.rand(1000)
	plt.hist(gaussian)
	plt.savefig("/usr/lib/cgi-bin/tests/graphic_analysis/hist")
	#plt.show()
	plt.close()
	
def HistogramPlot4():

	import matplotlib.pyplot as plt
	import numpy as np
	#import plotly.plotly as py
	values=np.random.normal(15,5,50)

	gaussian=sorted([1,1,1,2,2,2,2,3,3,3,4,4,4,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,10,11,11,11,12,12,12,12,13,13,13,14,14,15,15,15,16,16,17,17,18,18,19,19,20])
	#plt.hist(gaussian)
	plt.hist(values)
	plt.savefig("/usr/lib/cgi-bin/tests/graphic_analysis/hist2")
	plt.close()

def HistogramPlot5():

	import matplotlib.pyplot as plt
	import numpy as np
	#import plotly.plotly as py
	values=np.random.normal(15,5,50)

	gaussian=sorted([1,1,1,2,2,2,2,3,3,3,4,4,4,5,5,5,5,5,6,6,6,6,6,7,7,7,7,7,8,8,8,8,9,9,9,9,10,10,10,10,10,11,11,11,12,12,12,12,13,13,13,14,14,15,15,15,16,16,17,17,18,18,19,19,20])
	#plt.hist(gaussian)
	plt.hist(values,hisstype='step')
	plt.savefig("/usr/lib/cgi-bin/tests/graphic_analysis/hist2")
	plt.close()

def PiePlot():

	import matplotlib.pyplot as plt
	sizes=[15,30,45,10]
	colors=['Green','Yellow','Blue']
	explode = (0,0.1,0,0)

	plt.pie(sizes,explode=explode,colors=colors,autopct='%1.1f',shadow=True,startangle=70)
	plt.savefig("/usr/lib/cgi-bin/tests/graphic_analysis/pie")
	plt.close()

##############

#print "date time="+str(datetime.datetime())
#main()

PiePlot() #WORKs
#HistogramPlot5() 
#HistogramPlot4() #works
#HistogramPlot3() #works !!!
#BarPlot3() #works!!
BarPlot2() #works!!!
#BarPlot() #works!!
ScatterPlot()#works!!




