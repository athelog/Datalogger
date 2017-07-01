#!/usr/bin/env python
import cgi
import cgitb
import sys
from common_functs import *



#####debugging##############
cgitb.enable()
###########################

########################################SCRIPT CONST########################

language="SP" #SP=spanish, otherwise english

########################################SCRIPT VARS#########################

script_status="STD" #STD=standard view



########################################FUNCT DEFINITION####################


####main
def Main():

	#print "<br>Datalogger - SAS.SA 2015"
	if(language=="SP"):print "<br>Bajo desarrollo"

#######################################END OF FUNCT DEF######################


##########################################SCRIPT EXECUTION####################


#######HTML FORMS
print "Content-type: text/html\n\n"
print "<body style='background-color:white'>"
PrintDefaultLinks()
print "<hr>"

if(language=="SP"):print "<h2>Estaciones</h2>"
else:print "<h2>Stations</h2>"

Main()


