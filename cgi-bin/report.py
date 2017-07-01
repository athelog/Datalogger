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
cgitb.enable()


#######################################SCRIPT CONSTS##########################
masterfile_path = "./database/" #where the masterfiles are stored - relative path
report_path="./report/" #where the reports are stored - relative path
report_name="report.csv" #report name in unix
table_max_cells=10 #max number of cells to print in 
Debug_Flag = "NONE" #DEEP,NONE
Url="192.168.10.104/cgi-bin/report.py" #basic url of script

print_table_ignore_list = [2,6,7] #tokens from report we don't want to show to user
					#2=operation code, 6=status, 7=Error										

table_print_client_tokens="TRUE" #if TRUE, ignores the N,Op,Status tokens
language="SP";#SP=spanish, ENG=english

########################################SCRIPT VARS - DON'T TOUCH#############
number_of_pages=-1 # number of pages in table
current_page=-1	#current page to show in table
initial_date_value=""
final_date_value=""
script_status="START"
##############FUNCT DEFINITION########

###########redirecting url
def redirectUrl(url):
	#print "Content-Type: text/pain"
	#print "Refresh: 0; url=%s" % url
	#print "Redirecting..."	
	print "Location:hello.y"

#####used to force refresh. state=state of script where u want to redirect
def RedirectToUrl(state):

	print "<head><meta http-equiv='refresh' content='0;report.py?STATE="+state+"'/></head>"


##########checking date input fields. Return 1 if valid, othwerwise -1
def ValidateDate(date):
	
	try:
		datetime.datetime.strptime(date,'%Y-%m-%d')
		return 1
	except ValueError:
		return -1


#########checking both date fields consistency. returns 1 if succesfull and -1 otherwise
def CheckDateFields():

	global initial_date_value
	global final_date_value
	global button_form

	initial_date_value=button_form.getvalue('initial_date')
	final_date_value=button_form.getvalue('final_date')
	
	if (initial_date_value):
		if (ValidateDate(initial_date_value)==-1):
			if(language=="SP"):print "<b><br><font color='red'>ERROR - Formato de fecha inicial valida!</font></b>"
			else:print "<b><br><font color='red'>ERROR - invalid initial date format!</font></b>"
			return -1
	else:
		if(language=="SP"):print "<br><b><font color='blue'>Por favor digite una fecha inicial valida</font></b>"
		else:print "<br><b><font color='blue'>Please enter valid initial date</font></b>"
		return -1

	if (final_date_value):
		if (ValidateDate(final_date_value)==-1):
			print "<br><b><font color='red'>ERROR - invalid final date format!</font></b>"
			return -1
	else:
		if(language=="SP"):print "<br><b><font color='blue'>Por favor digite una fecha final valida</font></b>"
		else:print "<br><b><font color='blue'>Please enter valid final date</font></b>"
		return -1
	
	if (initial_date_value and final_date_value and ValidateDate(initial_date_value)==1 and ValidateDate(final_date_value)==1):
		if (initial_date_value>final_date_value):
			if(language=="SP"):print "<br><b><font color='red'>ERROR - La fecha final debe ser igual o posterior a la inicial</font></b>"
			else:print "<br><b><font color='red'>ERROR - Final date must be older than initial date or equal</font></b>"
			return -1
		else:
			return 1

	else:
		return -1


##########extract data from masterfiles. Returns 1 is succesful, otherwise -1
def GenerateReportPerDate():
	
	if (Debug_Flag=="DEEP"):print "<br><b>Executting GenerateReportPerDate()</b>"			

	global  initial_date_value
	global final_date_value
	grep_path = masterfile_path+"*" 

	initial_date =datetime.datetime.strptime(initial_date_value,'%Y-%m-%d').date()
	final_date = datetime.datetime.strptime(final_date_value,'%Y-%m-%d').date()
 	
	if (Debug_Flag=="DEEP"):
		print "<br>--Final date="+str(final_date)
		print "<br>--Initial date="+str(initial_date)
		print "<br>--Date range="+str(final_date-initial_date)

	#deleting old report file if exists
	if (os.path.isfile(report_path+report_name)==True):
		if (Debug_Flag=="DEEP"):print "<br>--Deleting old report file="+report_path+report_name
		os.remove(report_path+report_name) #delete old report files
	else:
		if (Debug_Flag=="DEEP"):print "<br>--Unable to find old report file="+report_path+report_name
	
	#printing header into new report file
	if(language=="SP"):new_header_command_string = 'echo "N,Op,Id,Codigo,Peso,Status,ErrorCode,Fecha,Hora,Estacion IP" >'+report_path+report_name
	else:new_header_command_string = 'echo "N,Op,Id,Code,Weight,Status,ErrorCode,Datetime" >'+report_path+report_name
		
	
	if (Debug_Flag=="DEEP"):print "<br>--Creating header in new report file="+report_path+report_name
	os.system(new_header_command_string)

	#checking if report file was succesfully created
	if (os.path.isfile(report_path+report_name)==True):
		if (Debug_Flag=="DEEP"):print "<br>--New report file="+report_path+report_name+" was created"
	else:
		if (Debug_Flag=="DEEP"):print "<br>--ERROR: Unable to create new report file="+report_path+report_name
		return -1					
	
	for n in range(int((final_date-initial_date).days)+1):

		grep_command_string = "grep -h "+str(initial_date+datetime.timedelta(days=n))+" "+masterfile_path+"*.* >>"+report_path+report_name		
		if (Debug_Flag=="DEEP"):
			#print str(initial_date+datetime.timedelta(days=n))+","
			print "<br>--Grep command="+grep_command_string
		os.system(grep_command_string)
		

	#end for


########print report table
def PrintTable():

	count=0	#counting number lines

	print "<table border='1'>"
	#print "<tr><td>count</td><td>N</td><td>Op</td><td>Id</td><td>Code</td><td>Weight</td><td>Status</td><td>ErrorCode</td><td>Datetime</td>"

	print "<tr><td>Count</td><td>Codigo</td><td>Peso</td><td>Fecha</td><td>Hora</d>"	


	for line in open(report_path+report_name):

		count+=1
		list=line.split(",")
		print "<tr>"
		
		print "<td>"+str(count)+"</td>"
		for i in list:
			print "<td>"+i+"</td>"
		print "</tr>"
	
	print "</table>"

#######get number of pages in report and store in global 
def GetNumPages():
	
	if (Debug_Flag=="DEEP"):print "<br><b>Executing function GetNumPages()</b>" 

	global number_of_pages
	count=0	#counting number lines in report

	for line in open(report_path+report_name):
		count+=1

	#calculating total of pages	
	if (count%table_max_cells==0):
		number_of_pages = int(count/table_max_cells)
	else:
		number_of_pages = int(count/table_max_cells)+1

	if (Debug_Flag=="DEEP"):print "<br>--Number of Pages()="+str(count)+"/"+str(table_max_cells)+"="+str(number_of_pages) 
	if (Debug_Flag=="DEEP"):print "<br><b>Finished function GetNumPages()</b>" 

#####to print table first time
def AdjustCurrPage():

	global current_page
	global number_of_pages
		
	if (current_page==-1 and number_of_pages>0):
		current_page=1
	

######print table in cell range
def PrintTableRange(start,end):

	global table_max_cells
	global current_page
	global Url
	global report_path, report_name
	count=0 #number of lines in report file
	
	if(language=="SP"):print "<br><b>Reporte</b>"
	elif(language=="ENG"):print "<br><b>Report</b>"
	
	if (current_page>1):
		if(language=="SP"):print "<b>- Pagina actual="+str(current_page)+" de "+str(number_of_pages)+"</b>"
		else:print "<b>- Current Page="+str(current_page)+" of "+str(number_of_pages)+"</b>"
		

	print "<table border='1'>"
	#FIXME:dead code #print "<tr><td>count</td><td>N</td><td>Op</td><td>Id</td><td>Code</td><td>Weight</td><td>Status</td><td>ErrorCode</td><td>Date</td><td>Time</td><td>StationIP</td>"
	
	if(language=="SP"):
		print "<tr><td>Count</td><td>Codigo</td><td>Peso</td><td>Fecha</td><td>Hora</d><td>Estacion IP</d>"
	elif(language=="SP"):
		print "<tr><td>Count</td><td>Code</td><td>Weight</td><td>Date</td><td>Time</d><td>Station IP</d>"

	for line in open(report_path+report_name):
		count +=1
		list=line.split(",")	
		column_count=0 #to discriminate which columns not to print	

		#will ignore first line of report to avoid duplicate header in table
		if (count>=int(start) and count<=int(end) and count!=1):
			print "<tr>"
			print "<td>"+str(count)+"</td>"
			for i in list:			
					
				#---logic to skip non required columns from report
				column_count=column_count+1
				if(Debug_Flag=="DEEP"):

					#original
					#print "<td>"+"(column count="+str(column_count)+")"+i+"</td>"

					if(column_count==4 or column_count==5 or column_count==8 or column_count==9 or column_count==10):
						#print "<td>"+"(column count="+str(column_count)+")"+i+"</td>"
						print "<td>"+i+"</td>"
	
					#else:
					#	print "<td>"+i+"</td>" 

					#not wotking
					#if column_count not in print_table_ignore_list:
					#if (1==1):
					#	"<td>"+"(column count="+str(column_count)+")"+i+"</td>"
				else:
			
					#FIXME: add to a list the print valid columns=4,5,8,9,10 > count,code, weight,date,time,station ip
					if(column_count==4 or column_count==5 or column_count==8 or column_count==9 or column_count==10):
						#print "<td>"+"(column count="+str(column_count)+")"+i+"</td>"
						print "<td>"+i+"</td>"					
				
			print "</tr>"
	#end of for
		
	print "</table>" #closing table	
 
	#printing links if number of pages>1
	if (number_of_pages>1):
		
		if(language=="SP"):print "<br>Paginas:"
		elif(language=="ENG"):print "<br>Pages:"
		
		for i in range(1,number_of_pages+1):
			url_string="?CurrPage="+str(i)+"&NumPages="+str(number_of_pages)
			print "<a href="+url_string+">"+str(i)+"</a> "


	if (Debug_Flag=="DEEP"):print "<br>Number of pages in table="+str(number_of_pages)

	#download report link
	if(language=="SP"):print "<br><br><a href="+report_path+report_name+"><img src='./html_common/excel_icon.png' width='70' height='70' title='Descargar reporte'><br>Descargar reporte</a>"	
	elif(language=="ENG"):print "<br><br><a href="+report_path+report_name+"><img src='./html_common/excel_icon.png' width='70' height='70' title='Download Report'><br>Download report</a>"


########capture url args
########expected in format: url?CurrPage=2&NumPages=8
def GetUrlArgs():
	
	global current_page
	global number_of_pages
	form = cgi.FieldStorage()
	CurrPage = form.getvalue('CurrPage')
	NumPages = form.getvalue('NumPages')

	if CurrPage:
		current_page=CurrPage
	else:
		current_page=-1

	if NumPages:
		number_of_pages=NumPages
	else:
		number_of_pages=-1	

	if(Debug_Flag=="DEEP"):print "<br>--current page="+str(current_page)

###print default links

#FIXME:this is not longer required
#def PrintDefaultLinks2():

#	print "<a href='/cgi-bin/index.py'>Index</a>"
#	print "<a href='/cgi-bin/report.py'>Report</a>"
#	print "<a href='/cgi-bin/config.py?state=START'>Products</a>"
#	print "<a href='/cgi-bin/users.py?state=START'>Users</a>"
#	print "<a href='/cgi-bin/manual.py?state=START'>Manual</a>"
#	print "<a href='/cgi-bin/log.py?state=START'>Log</a>"
#	print "<a href='/cgi-bin/about.py?state=START'>About</a>"

########main function
def Main():

	global current_page
	global table_max_cells
	global number_of_pages

	GetUrlArgs()
	GetNumPages()
	AdjustCurrPage()

	#checking date input
	if ((generate_action=="generate_report" and language=="ENG") or (generate_action=="Generar reporte" and language=="SP")):
		if (CheckDateFields()==1):
			GenerateReportPerDate()
			print "<br>" 
			RedirectToUrl("NONE")
			
			if(Debug_Flag=="DEEP"):PrintTable() #print full table for debug purposes

	#print table just if 
	if (number_of_pages>=1):	
		print_start_record=table_max_cells*(int(current_page)-1)+1
		print_final_record=table_max_cells*int(current_page)
		PrintTableRange(print_start_record,print_final_record)

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

if (language=="ENG"): print "<h2>REPORT GENERATION</h2>"
elif (language=="SP"): print "<h2>GENERACION DE REPORTES</h2>"

print "<br>"
#print "<form action='/cgi-bin/report.py?S="+initial_date_action+"&F="+final_date_action+"' method='POST'>"
print "<form action='/cgi-bin/report.py' method='POST'>"
print "<table border='1'>"
print "<tr>"

if (language=="ENG"):
	print "<td><input type='text' name='initial_date'><br><b>Initial Date YYYY-MM-DD</b></td>"
	print "<td><input type='text' name='final_date'><br><b>Final Date YYYY-MM-DD</b></td>"
elif (language=="SP"):
	print "<td><input type='text' name='initial_date'><br><b>Fecha inicial AAAA-MM-DD</b></td>"
	print "<td><input type='text' name='final_date'><br><b>Fecha final AAAA-MM-DD</b></td>"

print "</tr>"
print "</table>" 
print "<br>"
print "<input type='hidden' name='download_to_usb' value='full_report_to_USB'>"
print "<input type='hidden' name='download_to_computer' value='full_report_to_computer'>"

if(language=="SP"):print "<input type='submit' name='generate' value='Generar reporte'>"
else:print "<input type='submit' name='generate' value='generate_report'>"

#print "<input type='submit' value='Download full report to Raspberry USB'>"
#print "<input type='submit' value='Download full report to computer'>"		
print "</form>"



##########END OF FORMS #######################################################

##########BUTTON HANDLERS####################################################

#button handlers
action=button_form.getvalue('download_to_usb')
action=button_form.getvalue('download_to_computer')
generate_action=button_form.getvalue('generate')
print "<br>"

##########END OF BUTTON HANDLERS##############################################

Main()

#print "<br>"
#print "DEBUG ONLY = USB download capture value="+str(action)+"<br>"
#print "DEBUG ONLY = Computer download capture value="+str(action)






