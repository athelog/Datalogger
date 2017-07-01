#!/usr/bin/env python
import cgi
import cgitb
import sys
import os
import os.path
import glob
import csv
import string
import urllib
import time
import datetime
cgitb.enable()

############1)SCRIPT VARS - USERS CAN TOUCH######################################
Debug_Flag="DEEP" #activate debug messages (=NORMAL/DEEP/DISABLE)
masterfile_path="./logs/" #masterfile relative path
masterfile_maxlines = 100 #max size in lines of masterfile

###---1.1) stations ips/urls configuration for Response method
station_response_url="/cgi/tests/"
station_response_script="station_response.py"

############2)SCRIPT VARS - DONT TOUCH##########################################
arg1 = "default"
arg2 = "default"
arg3 = "default"
arg4 = "default"
arg5 = "default"
arg6 = "default"
arg7 = "default"
arg8 = "default"
time="0.0"

current_masterfile_index = -1

############FUNCT DEF##########################################################

#####reading args##
def GetUrlArgs():

	global arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,time

	if (Debug_Flag=="DEEP"):print "<br><b>Executting Function GetUrlArgs. Debug_Flag=</b>"+Debug_Flag

	form = cgi.FieldStorage()
	arg1 = form.getvalue('N')
	arg2 = form.getvalue('Op')
	arg3 = form.getvalue('id')
	arg4 = form.getvalue('ErrorCode')
	#arg5 = form.getvalue('Weight')
	#arg6 = form.getvalue('Status')
	#arg7 = form.getvalue('ErrorCode')
	#arg8 = form.getvalue('Datetime')
	time=str(datetime.datetime.now().date())

	if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):
		print "<br>"
		print "<br><b>--Received args</b>"
		print "<br>N (Operation number)="+arg1
		print "<br>Op (Operation type)="+arg2
		print "<br>Id (Station id)="+arg3
		print "<br>ErrorCode (Server error code)="+arg4
		#print "<br>Weight (Product weight)="+arg5
		#print "<br>Status (server status) ="+arg6
		#print "<br>ErrorCode (station error code) ="+arg7
		#print "<br>Datetime ="+arg8

	if (Debug_Flag=="DEEP"):print "<br><b>Finished Function GetUrlArgs. Debug_Flag=</b>"+Debug_Flag


#####returns index of latest masterfile. In case of error returns -1.
def GetMasterfileIndex():

	index = -1 #default value
	if (Debug_Flag=="DEEP"):print "<br><br><b>Executing Function GetMasterfileIndex. Debug_Flag=</b>"+Debug_Flag

	#checking that database path exists
  	if (os.path.isdir(masterfile_path)==True):

		if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br>--Database path is valid="+masterfile_path
	else:
		if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br>--ERROR:Database path is invalid="+masterfile_path

	#storing masterfiles names in list
	filenames_list=glob.glob(masterfile_path+"*.csv")
	if (Debug_Flag=="DEEP"):print "<br>--Masterfiles="+str(filenames_list)

	#checking if database folder is empty. If so, create the masterfile_0_.csv file
	if not filenames_list:
		CreateFile(masterfile_path+"masterfile_0_.csv")		
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

###store data in masterfile
def StoreData2(filename, data):

	global current_masterfile_index
	if (Debug_Flag=="DEEP"):print "<br><b>Executting Function StoreData. Debug_Flag=</b>"+Debug_Flag
	
	#check number of lines in file
	with open(filename) as file:
		count = sum(1 for line in file)
	if (Debug_Flag=="DEEP"):print "<br>--Number of lines in masterfile="+filename+" is="+str(count)

	#if number of lines is still under the limit, can save into file. Otherwise, create new masterfile
	if (count<masterfile_maxlines):
		if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br>--Storing data into masterfile="+filename
		os.system('echo "'+data+'">>'+filename)

	else:
		new_masterfile_string=masterfile_path+"masterfile_"+str(current_masterfile_index+1)+"_.csv"	
		if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br>--Creating new masterfile="+new_masterfile_string			
		CreateFile(new_masterfile_string)	

	if (Debug_Flag=="DEEP"):print "<br><b>Finished Function StoreData. Debug_Flag=</b>"+Debug_Flag

def StoreInLog(data):

	command_string="echo "+data+" >>log.txt"
	os.system(command_string)


###create new file. Returns True if succesful, otherwise returns False 
def CreateFile(filename):

	if (Debug_Flag=="DEEP"):print "<br><b>Executting Function CreateFile. Debug_Flag=</b>"+Debug_Flag	
	
	#check that file doesnt already exist, create it and add the header/data
	if (os.path.isfile(filename)==False):
	
		command_string = 'echo "N,Op,Id,Code,Weight,Status,ErrorCode,Datetime" >'+filename
		if (Debug_Flag=="DEEP"):print "<br>--Command string="+command_string+". Debug_Flag="+Debug_Flag
		os.system(command_string)
		#command_string = 'Server data received >> '+filename
		command_string = 'echo "'+arg1+","+arg2+","+arg3+","+arg4+","+arg5+","+arg6+","+arg7+","+arg8+'">> '+filename
		if (Debug_Flag=="DEEP"):print "<br>--Command string="+command_string+". Debug_Flag="+Debug_Flag
		os.system(command_string)
		if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br>--Mastefile succesfully created="+filename
		if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br><b>Finished Function CreateFile. Debug_Flag=</b>"+Debug_Flag	
		return True
	else:	
		if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br>--ERROR:Masterfile already exists="+filename
		if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br><b>Finished Function CreateFile. Debug_Flag=</b>"+Debug_Flag	
		return False

#response to stations
def Response(station_id, data):
	
	if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br><b>Responding to station</b>"
	#send_data(station_id, data)
	
	if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br><b>Responding to station</b>"

####Main funct##
def main():

	global current_masterfile_index
	current_masterfile_index = GetMasterfileIndex() #getting latest masterfile number

	if (Debug_Flag=="DEEP"):print "<br><br><b>Executting Function Main. Debug_Flag=</b>"+Debug_Flag

	GetUrlArgs() #capturing url args
	
	current_masterfile_string = "masterfile_"+ str(current_masterfile_index)+"_.csv"
	if (Debug_Flag=="DEEP" or Debug_Flag=="NORMAL"):print "<br>--Masterfile Index ="+ str(current_masterfile_index)
	data_string=time+". Server data received="+arg1+","+arg2+","+arg3+","+arg4	
	#data_string=arg1+","+arg2+","+arg3+","+arg4+","+arg5+","+arg6+","+arg7+","+arg8
	if (Debug_Flag=="DEEP"):print "<br>--Asking to sore Data string ="+data_string+" in log="+masterfile_path+current_masterfile_string,data_string
	#StoreData(masterfile_path+current_masterfile_string,data_string)
	StoreInLog(data_string)
		
	if (Debug_Flag=="DEEP"): print "<br><br><b>Finished Function Main. Debug_Flag=</b>"+Debug_Flag

##########END OF FUNC DEF#####################################################



###########SCRIPT FLOW########################################################

########HTML CONTENT#######
print "Content-type: text/html\n\n"
print "<h2>Check args module</h2>"

main()


###########END OF SCRIPT FLOW#################################################





