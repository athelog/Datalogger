#!/usr/bin/env python
import cgi
import cgitb
import sys
from common_functs import *


#####debugging##############
cgitb.enable()
###########################

########################################SCRIPT CONST########################



########################################SCRIPT VARS#########################

script_status="STD" #STD=standard view



########################################FUNCT DEFINITION####################

###print html links  
def PrintLinks2():

	Report_link="<a href='/cgi-bin/report.py' title='Report'><img width='70' height='70' border='0' alt='Report' src='./html_common/report_icon.png'></a>"
	Products_link="<a href='/cgi-bin/products.py?state=SHOW_PRODUCT_CONFIG' title='Products'><img width='70' height='70' border='0' alt='Products' src='./html_common/products_icon.png'></a>"
	Users_link="<a href='/cgi-bin/users.py?state=START' title='Users'><img width='70' height='70' border='0' alt='Users' src='./html_common/users_icon.png'></a>"
	Manual_link="<a href='/cgi-bin/docs/manual.pdf' title='Manual'><img width='70' height='70' border='0' alt='Manual' src='./html_common/manual_icon.png'></a>"
	Log_link="<a href='/cgi-bin/log.py?state=START' title='Log'><img width='70' height='70' border='0' alt='Log' src='./html_common/log_icon.png'></a>"
	About_link="<a href='/cgi-bin/about.py?state=START' title='About'><img width='70' height='70' border='0' alt='About' src='./html_common/about_icon.png'></a>"
	Stations_link="<a href='/cgi-bin/stations.py?state=START' title='Stations'><img width='70' height='70' border='0' alt='About' src='./html_common/stations_icon.png'></a>"

	print "<table border='1'>"
	print "<tr><td><b>Link</b></td><td><b>Descripcion</b></td></tr>"
	print "<tr><td>"+Report_link+"</td><td>Generar reportes</td></tr>"
	print "<tr><td>"+Products_link+"</td><td>Edit product name/code</td></tr>"
	print "<tr><td>"+Users_link+"</td><td>Add/Edit users</td></tr>"
	print "<tr><td>"+Manual_link+"</td><td>User manual</td></tr>"
	print "<tr><td>"+Stations_link+"</td><td>Stations</td></tr>"
	print "<tr><td>"+Log_link+"</td><td>Server log</td></tr>"
	print "<tr><td>"+About_link+"</td><td>About info</td></tr>"
	print "</table>"

	#print "<img src='sas_banner_1.png'>"
	#print "<img src='./html_common/sas_banner_1.png'>"

####main
def Main():

	PrintLinks()
	#print "<br>Datalogger - SAS.SA 2015"

#######################################END OF FUNCT DEF######################


##########################################SCRIPT EXECUTION####################


#######HTML FORMS
print "Content-type: text/html\n\n"
print "<body style='background-color:white'>"
PrintDefaultLinks()
print "<hr>"
if(language=="SP"):print "<h2>Principal</h2>"
else:print "<h2>Main</h2>"

Main()


