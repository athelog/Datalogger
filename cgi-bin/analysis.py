#!/usr/bin/env python
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
from common_functs import *
from common_vars import *
#from rtf import *

from docx import Document
 
cgitb.enable()
  

#######################################SCRIPT CONSTS##########################
masterfile_path = "./database/" #where the masterfiles are stored - relative path
report_path="./report/" #where the reports are stored - relative path
report_name="report.csv" #report name in unix
table_max_cells=10 #max number of cells to print in 
Debug_Flag = "NONE" #DEEP,NONE
Url="192.168.10.104/cgi-bin/report.py" #basic url of script					
script_valid_status = ['START','bars','pie','hist','control','pareto','help']
table_print_client_tokens="TRUE" #if TRUE, ignores the N,Op,Status tokens
language="SP";#SP=spanish, ENG=english

########################################SCRIPT VARS - DON'T TOUCH#############
number_of_pages=-1 # number of pages in table
current_page=-1	#current page to show in table
initial_date_value=""
final_date_value=""
script_status="START"

report_code = "UNKNOWN"
##############FUNCT DEFINITION########













def CheckReportFolder(report_code):

	return "True"

	
########capture url args
########expected in format: url?CurrPage=2&NumPages=8
def GetUrlArgs():
	
	global script_status,report_code
	form = cgi.FieldStorage()
	StateQuery=form.getvalue('state')
	ReportQuery = form.getvalue('report')

	if StateQuery:
		script_status=StateQuery
	else:
		script_status="UNKNOWN"
		return "False"

	if ReportQuery:
		report_code=ReportQuery
	else:
		report_code="UNKNOWN"
		return "False"

	#debug
	if(Debug_Flag=="DEEP"): print "<br>(Debug DEEP) - Retrieved args="+script_status+","+report_code


	#validating queries
	if(script_status in script_valid_status and CheckReportFolder(report_code)=="True"):return "True"
	else:return "False"
			

	if(Debug_Flag=="DEEP"):print "<br>--current page="+str(current_page)

####print BarsPlot

###prints html bars plot in page
def BarsPlot():

	print "<form>"
	print "<table border='1'>"

	if(language=="SP"):
		print "<tr><td>Grafico de barras</td></tr>"
		print "<tr><td><img src='"+analysis_basefolder+report_code+"/"+bars_plot_filename+"_"+report_code+".png"+"' width='"+plot_width+"' height='"+plot_height+"' title='Download Report'></td></tr>"

	if(language=="SP"):
		print "<tr><td><input type='submit' name='download_partial_analysis' value='Descargar seccion'></td>"
		print "<td><input type='submit' name='download_full_analysis' value='Descargar todo'></td></tr>"
		
	print "</table></form>"

#end of funct

###Generate word doc for any section or full
#args=bars, pie, etc or full
def GenerateWordDoc(section):



	return "True"

#end of funct

########main function
def Main():

	global current_page
	global table_max_cells
	global number_of_pages

	if(GetUrlArgs()=="False"):
		if(language=="SP"):print "<br><b>ERROR - Argumentos no validos. Por favor recarge la pagina"
		else:print "<br><b>ERROR - Args not valid. Please reload page"

	if (script_status=="bars"):BarsPlot()


##############END OF FUNCT DEF########

##############HTML SECTION#######################


#redirectUrl("ddd")
print "Content-type: text/html\n\n"


reader = csv.reader("out.csv")
button_form=cgi.FieldStorage()

download_action="" #what to do if dowload button are clicked
table_string = ""

###########FORMS###############################################################

initial_date_action="MM/DD/YYYY"
final_date_action="MM/DD/YYYY"
print "<body style='background-color:white'>"
PrintDefaultLinks()
print "<hr>"

if (language=="ENG"): print "<h2>REPORT ANALYSIS</h2>"
elif (language=="SP"): print "<h2>ANALISIS DE REPORTE</h2>"

if(GetUrlArgs()=="True"):

	bars_url = "/cgi-bin/analysis.py?state=bars"+"&report="+report_code
	pie_url = "/cgi-bin/analysis.py?state=pie"+"&report="+report_code
	hist_url = "/cgi-bin/analysis.py?state=hist"+"&report="+report_code
	pareto_url = "/cgi-bin/analysis.py?state=pareto"+"&report="+report_code
	help_url = "/cgi-bin/analysis.py?state=help"+"&report="+report_code

	if(language=="SP"):
		print "<table border='1'>"
		print "<tr>"
		print "<td><a href="+bars_url+">Barras</a></td>"
		print "<td><a href="+pareto_url+">Pareto</a></td>"
		print "<td><a href="+pie_url+">Pastel</a></td>"
		print "<td><a href="+hist_url+">Histograma</a></td>"
		print "<td><a href="+help_url+">Ayuda</a></td>"		
		print "</table>"


#download analysis link
if(language=="SP"):print "<br><br><a href="+report_path+report_name+"><img src='./html_common/excel_icon.png' width='70' height='70' title='Descargar reporte'><br>Descargar analisis</a>"	
elif(language=="ENG"):print "<br><br><a href="+report_path+report_name+"><img src='./html_common/excel_icon.png' width='70' height='70' title='Download Report'><br>Download analysis</a>"



##########END OF FORMS #######################################################

##########BUTTON HANDLERS####################################################

#button handlers
action=button_form.getvalue('download_to_usb')
action=button_form.getvalue('download_to_computer')
generate_action=button_form.getvalue('generate')
print "<br>"

##########END OF BUTTON HANDLERS##############################################

Main()







