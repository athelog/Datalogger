#!/usr/bin/env python

###########HISTORY###############################################################
#last edit:Dec 7, 2015 - chaging ResponseToStation()


###########IMPORTS################################################################

import cgi
import cgitb
import sys
import os
import os.path
import glob
import csv
import string
import urllib
import urllib2
import time
import datetime
import commands

############DEBUGGING ENABLE

cgitb.enable()

############1)SCRIPT VARS - USERS CAN TOUCH######################################
Debug_Flag="DEEP" #activate debug messages (=NORMAL/DEEP/DISABLE)
masterfile_path="./database/" #masterfile relative path
masterfile_maxlines = 5 #max size in lines of masterfile

###---1.1) stations ips/urls configuration for Response method
station_response_url="/cgi-bin/tests/"
station_response_simulator_script="station_simulator_response.py"
configfiles_path = "./config_files/" #where the config files are stored - relative path
product_config_filename="product_config.csv" #product config  name in unix

############2)SCRIPT VARS - DONT TOUCH##########################################
arg1 = "default"
arg2 = "default"
arg3 = "default"
arg4 = "default"
arg5 = "default"
arg6 = "default"
arg7 = "default"
arg8 = "default"
arg9 = "default"
station_ip="default"

current_masterfile_index = -1

############FUNCT DEF##########################################################

#####reading args##
def GetUrlArgs():

	global arg1,arg2,arg3,arg4,arg5,arg6,arg7,arg8,arg9,station_ip

	if (Debug_Flag=="DEEP"):print "<br><b>Executting Function GetUrlArgs. Debug_Flag=</b>"+Debug_Flag

	form = cgi.FieldStorage()
	arg1 = form.getvalue('N')
	arg2 = form.getvalue('Op')
	arg3 = form.getvalue('id')
	arg4 = form.getvalue('Code')
	arg5 = form.getvalue('Weight')
	arg6 = form.getvalue('Status')
	arg7 = form.getvalue('ErrorCode')
	#arg8 = form.getvalue('Datetime')
	arg8=str(datetime.datetime.now().date())
	arg9=str(datetime.datetime.now().time())[:-7]
	station_ip=os.environ["REMOTE_ADDR"]

	if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):
		print "<br>"
		print "<br><b>--Received args</b>"
		print "<br>N (Operation number)="+arg1
		print "<br>Op (Operation type)="+arg2
		print "<br>Id (Station id)="+arg3
		print "<br>Code (Product code)="+arg4
		print "<br>Weight (Product weight)="+arg5
		print "<br>Status (server status) ="+arg6
		print "<br>ErrorCode (station error code) ="+arg7
		print "<br>Date ="+arg8
		print "<br>Time ="+arg9
		print "<br>Station ip="+station_ip

	if (Debug_Flag=="DEEP"):print "<br><b>Finished Function GetUrlArgs. Debug_Flag=</b>"+Debug_Flag


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
def StoreData(filename, data):

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

###create new file. Returns True if succesful, otherwise returns False 
def CreateFile(filename):

	if (Debug_Flag=="DEEP"):print "<br><b>Executting Function CreateFile. Debug_Flag=</b>"+Debug_Flag	
	
	#check that file doesnt already exist, create it and add the header/data
	if (os.path.isfile(filename)==False):
	
		command_string = 'echo "N,Op,Id,Code,Weight,Status,ErrorCode,Date,Time,IP" >'+filename
		if (Debug_Flag=="DEEP"):print "<br>--Command string="+command_string+". Debug_Flag="+Debug_Flag
		os.system(command_string)
		command_string = 'echo "'+arg1+","+arg2+","+arg3+","+arg4+","+arg5+","+arg6+","+arg7+","+arg8+","+arg9+","+station_ip+'">> '+filename
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
def ResponseToStation():
	
	global arg1, arg2, arg3, arg4, station_ip, configfiles_path, product_config_filename

	#keep as a reference
	#arg1 = form.getvalue('N')
	#arg2 = form.getvalue('Op')
	#arg3 = form.getvalue('id')
	#arg4 = form.getvalue('Code')
	
	if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br><b>Starting Function Responding to station</b>"


	#station_url="http://"+station_ip+station_response_url+station_response_simulator_script
	station_url="http://"+station_ip
	#station_url=
	
	#use station simulator script in server to store response in log. See ./tests/log folder for details
	if(arg2=="sim_store_data"):
		#query_string={'N':arg1,'Op':'sim_ack','id':arg3,'ErrorCode':'None'}
		#query_data=urllib.urlencode(query_string)
		#if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br>--Response url="+station_url+", response type=sim_ack, query string="+str(query_data)
		#request=urllib2.Request(station_url,query_data)
		#response=urllib2.urlopen(request).read()
		#print response
		station_response_string='N='+arg1+'&Op=sim_ack'+'&id='+arg3+'&ErrorCode=None'
		if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br>--Response to station="+station_response_string
		print "<br>"+station_response_string




	#respond with server stats and product details, so that station can represent in LCD the product features
	elif(arg2=="store_data"):

		split_list=[]
		command_string="grep "+arg4+" "+configfiles_path+product_config_filename
		if (Debug_Flag=="DEEP"):print "<br>--Command string="+command_string
		response_string=str(commands.getstatusoutput(command_string))		
		split_list=response_string.split(",")		
		print "<br>--"+str(commands.getstatusoutput(command_string))+". Split="+str(split_list)+".Execution return="+str(split_list[0]).strip("(") #debug purposes			

		#checking that command returned 0(success) or 256 (fail)
		if (str(split_list[0]).strip("(")!="256"):

			Product_Token=split_list[2].strip("'").strip("(").strip("')")
			Code_Token=split_list[3].strip("'").strip("(").strip("')")

			#response to be read by station
			print "<br>&Op=@ack@+&Code=@"+arg4+"@&Error=@None@"            
		else:
			#response to station in case of code not found
			print "<br>&Op=@ack@&product_desc=@ERROR@&Error=@Unknown_Code@"

		#FIXME - add other error codes, as not having space in server
			


	
	elif(arg2=="prod_request"):
		
		#station just wants to confirm code/product name in produc configuration file, before samplig

		if (Debug_Flag=="DEEP"):print "<br>--Station requesting to check that this code is valid in conf file - Op="+arg2

		split_list=[]
		command_string="grep "+arg4+" "+configfiles_path+product_config_filename
		if (Debug_Flag=="DEEP"):print "<br>--Command string="+command_string
		response_string=str(commands.getstatusoutput(command_string))		
		split_list=response_string.split(",")		
		print "<br>--"+str(commands.getstatusoutput(command_string))+". Split="+str(split_list)+".Execution return="+str(split_list[0]).strip("(") #debug purposes			
		#MaxWeight_Token="15%"#tolerance for max weight - FIXME:add to conf product file
		#MinWeight_Token="5%"#tolerance for min weight- FIXME:add to conf product file
		#TargetWeight_Token=150 #expected weight units grams- FIXME:add to conf product file
		
		#checking that command returned 0(success) or 256 (fail)
		if (str(split_list[0]).strip("(")!="256"):

			Product_Token=split_list[2].strip("'").strip("(").strip("')")
			Code_Token=split_list[3].strip("'").strip("(").strip("')")
			TargetWeight_Token=split_list[4].strip("'").strip("(").strip("')")
			MaxTolerance_Token=split_list[5].strip("'").strip("(").strip("')")
			MinTolerance_Token=split_list[6].strip("'").strip("(").strip("')")

			#response to be read by station
			print "<br>&Op=@ack@&Code=@prod_request@"+"&prod_desc=@"+Product_Token+"@&Target=@"+str(TargetWeight_Token)+"@&max=@"+MaxTolerance_Token+"@&min=@"+MinTolerance_Token+"@&Error=@None@"                        
		else:
			#product code not found - sending error to station
			print "<br>&Op=prod_request=@&product_desc=@ERROR@&Error=@Unknown_Code@"	

	elif(arg2=="store_data_old_dont_care"):
		#query_string={'N':arg1,'Op':'ack','id':arg3,'ErrorCode':'None'}
		#query_data=urllib.urlencode(query_string)
		#if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br>--Response url="+station_url+", response type=sim_ack, query string="+str(query_data)
		#request=urllib2.Request(station_url,query_data)
		#response=urllib2.urlopen(request).read()
		#print response
		station_response_string='N='+arg1+'&Op=ack'+'&id='+arg3+'&ErrorCode=None'
		if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br>--Response to station="+station_response_string
		print "<br>"+station_response_string

	if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br><b>End of Function Responding to station</b>"

####Main funct##
def main():

	global current_masterfile_index
	current_masterfile_index = GetMasterfileIndex() #getting latest masterfile number

	if (Debug_Flag=="DEEP"):print "<br><br><b>Executting Function Main. Debug_Flag=</b>"+Debug_Flag

	GetUrlArgs() #capturing url args
	
	#checking the type of operation type
	if (arg2=="store_data"):

		current_masterfile_string = "masterfile_"+ str(current_masterfile_index)+"_.csv"
		if (Debug_Flag=="DEEP" or Debug_Flag=="NORMAL"):print "<br>--Masterfile Index ="+ str(current_masterfile_index)
		data_string=arg1+","+arg2+","+arg3+","+arg4+","+arg5+","+arg6+","+arg7+","+arg8+","+arg9+","+station_ip
		if (Debug_Flag=="DEEP"):print "<br>--Data string ="+data_string 
		StoreData(masterfile_path+current_masterfile_string,data_string)
		ResponseToStation()

	elif(arg2=="sim_store_data"):
		ResponseToStation()

	elif(arg2=="prod_request"):
		ResponseToStation()
		

	if (Debug_Flag=="DEEP"): print "<br><br><b>Finished Function Main. Debug_Flag=</b>"+Debug_Flag

##########END OF FUNC DEF#####################################################



###########SCRIPT FLOW########################################################

########HTML CONTENT#######
print "Content-type: text/html\n\n"
print "<h2>Check args module</h2>"

main()


###########END OF SCRIPT FLOW#################################################





