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
import shutil
import subprocess
import fileinput
from common_functs import *

####enabling debugging#######################################################

cgitb.enable()

#######################################SCRIPT CONSTS##########################
configfiles_path = "./config_files/" #where the config files are stored - relative path
product_config_filename="product_config.csv" #product config  name in unix
product_config_filename_tmp="product_config.csv.tmp" #temporal copy for modifications
product_config_filename_old="product_config.csv.old" #copy of old version of file for modifications
Debug_Flag = "DEEP"
Url="192.168.10.104/cgi-bin/products.py" #basic url of script

########################################SCRIPT VARS - DON'T TOUCH#############
number_of_pages=-1 # number of pages in table
current_page=-1	#current page to show in table
initial_date_value=""
final_date_value=""
script_state="DEBUG_ERROR" #state machine. values=START, SHOW_PRODUCT_CONFIG,EDIT_PRODUCT_CONFIG,DELETE_USER_CONFIG, DEBUG_ERROR
url_string="state=DEBUG_ERROR"



##############FUNCT DEFINITION##############################

#####used to force refresh. state=state of script where u want to redirect
def RedirectToUrl(state):

	print "<head><meta http-equiv='refresh' content='0;products.py?STATE="+state+"'/></head>"

####print default links for this page
def PrintBarMenu():

	Start_Link="<a href='/cgi-bin/products.py?STATE=START' title='Start'><img width='127' height='20' border='0' alt='Main' src='./html_common/Product_Main_Button.png'></a>"
	Show_Link="<a href='/cgi-bin/products.py?STATE=SHOW_PRODUCT_CONFIG' title='Show'><img width='127' height='20' border='0' alt='Start' src='./html_common/Product_Show_Button.png'></a>"
	Edit_Link="<a href='/cgi-bin/products.py?STATE=EDIT_START_PRODUCT_CONFIG' title='Edit'><img width='127' height='20' border='0' alt='Start' src='./html_common/Product_Edit_Button.png'></a>"


	print "<table border='0'>"
	print "<tr><td>"+Start_Link+"</td><td>"+Show_Link+"</td><td>"+Edit_Link+"</td></tr>"
	print "</table>"




#####reading state arg and store it in global script_state
def GetScriptState():

	global script_state

	if (Debug_Flag=="DEEP"):print "<br><b>Starting Function GetScriptState. Debug_Flag=</b>"+Debug_Flag

	form = cgi.FieldStorage()
	arg = form.getvalue('STATE')

	#checking if state arg is actually defined - otherwise return to START value
	if (not arg or str(arg)==""):
		script_state="START"
	else:
		script_state=str(arg)

	if (Debug_Flag=="NORMAL" or Debug_Flag=="DEEP"):print "<br>--script_state="+script_state
	if (Debug_Flag=="DEEP"):print "<br><b>Finished Function GetScriptState. Debug_Flag=</b>"+Debug_Flag

#######checking product config file integrity: Returns 0 if successfull, line number if invalid format, -2 if inexistent file
def CheckProdConfigFileIntegrity(file_to_check):
	
	if (Debug_Flag=="DEEP"):print "<br><b>Starting Function CheckProdConfigFileIntegrity. Debug_Flag=</b>"+Debug_Flag

	count=0#number of lines in config file
	numOfN=0 #number of  'N' tokens found in file. >1 means repeated
	numOfProduct=0 #number of  'Product' tokens found in file >1 means repeated
	numOfCode=0 #number of  'Code' tokens in file >1 means repeated
	
	#check if fail exists
	if (os.path.isfile(configfiles_path+file_to_check)==False):return -2
	else:	
		
		print "<br>--Starting validation process for tokens"  		
		#creating lists to check duplicated values and stuff
		N_token_list=[]
		Product_token_list=[]
		Code_token_list=[]
		#TargetWeight_token_list=[]
		#MaxTolerance_token_list=[]
		#MinTolerance_token_list=[]		

		count=0

		for line in open(configfiles_path+file_to_check):
			count+=1
			list=line.split(",")
			N_token = list[0]
			Product_token = list[1]
			Code_token=list[2]
			Code_token=Code_token.strip()	# eliminating new line char "/n"
			
			####
			TargetWeight_token=(list[3]).strip()
			MaxTolerance_token=(list[4]).strip()
			MinTolerance_token=(list[5]).strip()
			

			####checking that all tokens are not "". check that weight/tolerances are number and larger than >0. 
			if (Product_token==""):
				print "<br><b><font color=red>ERROR - item in column Product is empty. Product config file="+configfiles_path+file_to_check+"</font></b>"				
				return -20

			if (N_token==""):			
				print "<br><b><font color=red>ERROR - item in column N is empty. Product config file="+configfiles_path+file_to_check+"</font></b>"				
				return -30

			if (Code_token==""):			
				print "<br><b><font color=red>ERROR - item in column Code is empty. Product config file="+configfiles_path+file_to_check+"</font></b>"				
				return -40			

			if (TargetWeight_token==""):			
				print "<br><b><font color=red>ERROR - item in column TargetWeight is empty. Product config file="+configfiles_path+file_to_check+"</font></b>"				
				return -50

			else:
				if (count>1):
					try:	
						if (Debug_Flag=="DEEP"):print "<br>DEBUG - Testing the float cast="+str(TargetWeight_token)
						test=float(TargetWeight_token)
					except ValueError:
						print "<br><b><font color=red>ERROR - item in column TargetWeight is not a positive number="+str(TargetWeight_token)+"</font></b>"	
						return -50								
			
			if (MaxTolerance_token==""):			
				print "<br><b><font color=red>ERROR - item in column MaxTolerance is empty. Product config file="+configfiles_path+file_to_check+"</font></b>"				
				return -60

			else:

				if (count>1):			
					try:	
						test=float(MaxTolerance_token)
					except ValueError:
						print "<br><b><font color=red>ERROR - item in column MaxTolerance is not a positive number</font></b>"	
					return -60	

			if (MinTolerance_token==""):			
				print "<br><b><font color=red>ERROR - item in column MinTolerance is empty. Product config file="+configfiles_path+file_to_check+"</font></b>"				
				return -70
			
			else:
				if (count>1):
					try:	
						test=float(MinTolerance_token)
					except ValueError:
						print "<br><b><font color=red>ERROR - item in column MinTolerance is not a positive number</font></b>"	
						return -70	
			
			if (count>1):

				#adding tokens into checking lists
				try:
					N_token_list.append(int(N_token))
				except:
					print "<br><b><font color=red>ERROR - found non Integer element ("+N_token +") in column N, product config file="+configfiles_path+file_to_check+"</font></b>"	
					return -10	

				Product_token_list.append(Product_token)
				Code_token_list.append(Code_token)

					
	
		#end of for

		#looking for duplicated tokens in N, Product and Code column
		for n in N_token_list:
			if (N_token_list.count(n)>1):
				print "<br><b><font color=red>ERROR - duplicated element ("+str(n)+") in column N, product config file="+configfiles_path+product_config_filename+"</font></b>"	
				return -100
		for n in Product_token_list:
			if (Product_token_list.count(n)>1):
				print "<br><b><font color=red>ERROR - duplicated element ("+str(n)+") in column Product, product config file="+configfiles_path+product_config_filename+"</font></b>"	
				return -110
		for n in Code_token_list:		
			if (Code_token_list.count(n)>1):
				print "<br><b><font color=red>ERROR - duplicated element ("+str(n)+") in column Code, product config file="+configfiles_path+product_config_filename+"</font></b>"	
				return -120					
				

	if (Debug_Flag=="DEEP"):
			print "<br>---List of N tokens="+str(N_token_list)
			print "<br>---List of Product tokens="+str(Product_token_list)
			print "<br>---List of Code tokens="+str(Code_token_list)

		
	if (Debug_Flag=="DEEP"):print "<br><b>Finished Function CheckProdConfigFileIntegrity. Returning=0</b>"	
	return 0 #if no error is detected, return 0 (succesfull)	



########print report table, Set param=TRUE for editable table
def PrintTable(editable):

	if (Debug_Flag=="DEEP"):print "<br><b>Executing Function PrintTable. Debug_Flag=</b>"+Debug_Flag

	global url_string
	url_string="DEBUG_ERROR"
	count=0	#counting number lines

	#table to contain show and editable table
	print "<table border='2'>"
	print "<tr><td>"


	#printing non-editable table
	print "<br><b><font color='green'>Current product config file</font></b>"
	print "<table border='1'>"
	
	for line in open(configfiles_path+product_config_filename):
	
		count+=1
		list=line.split(",")
		print "<tr>"
		#print "<td>"+str(count)+"</td>"
		for i in list:
			print "<td>"+i+"</td>"
		print "</tr>"
		
	print "</table>"
	
	if (count==1): print "<br><font color='red'><b>Warning - Product config file is empty</b></font>"
	#end of non editable table
	

	if (editable=="FALSE"):#close non-editable table
		print "</td></tr></table>"

	#printing in editable mode - EDITABLE = TRUE
	else:
		count=0
		delete_button_action=[] #list for delete line buttons actions	
		delete_button_names=[] #to store button names	
	
		#create tmp copy of config file, also remove old tmp file before - JUST IF STATE==EDIT_START_PRODUCT_CONFIG

		if (script_state=="EDIT_START_PRODUCT_CONFIG"):
			if (os.path.isfile(configfiles_path+product_config_filename_tmp)==True):os.remove(configfiles_path+product_config_filename_tmp)  
			if (Debug_Flag=="DEEP"):print "<br>--Creating new tmp copy="+configfiles_path+product_config_filename_tmp		
			shutil.copy(configfiles_path+product_config_filename,configfiles_path+product_config_filename_tmp)
		
		elif (script_state=="EDIT_PRODUCT_CONFIG"):
			if (Debug_Flag=="DEEP"):print "<br>--Modifiying tmp copy="+configfiles_path+product_config_filename_tmp					
	
		print "</td><td><b><font color='blue'>Edit config file</font></b>"	
		print "<form action='/cgi-bin/products.py?STATE=EDIT_PRODUCT_CONFIG' method='POST'>"
		
		print "<table border='1'>"
		print "<tr><td>N</td><td>Product</td><td>Code</td><td>TargetWeight(Kg)</td><td>MaxTolerance(%)</td><td>MinTolerance(%)</td><td><font color='red'><b>Delete line?</b></font></td><td><font color='orange'><b>Warnings</b></font></td></tr>"
		
		if (Debug_Flag=="DEEP"):print "<br>--Opening tmp copy="+configfiles_path+product_config_filename_tmp
		for line in open(configfiles_path+product_config_filename_tmp):
			
			count+=1
			list=line.split(',')
			print "<br>Debug -"+str(list)
			if (count>1):	
				product_input_field_name="product_field"+str(count)
				code_input_field_name="code_field"+str(count)
				delete_line_button_name="delete_line_"+str(count)
				targetweight_input_field_name="targetweight_field"+str(count)
				maxtolerance_input_field_name="maxtolerance_field"+str(count)
				mintolerance_input_field_name="mintolerance_field"+str(count)
				delete_line_button_value="delete_line"
				
	
				print "<tr><td>"+str(count-1)+"</td>"
				print "<td><input type='text' name="+product_input_field_name+" value="+list[1]+"></td>"
				print "<td><input type='text' name="+code_input_field_name+" value="+list[2]+"></td>"
				print "<td><input type='text' name="+targetweight_input_field_name+" value="+list[3]+"></td>"
				print "<td><input type='text' name="+maxtolerance_input_field_name+" value="+list[4]+"></td>"
				print "<td><input type='text' name="+mintolerance_input_field_name+" value="+list[5]+"></td>"
				print "<td><input type='submit' name="+delete_line_button_name+" value="+delete_line_button_value+"></td></tr>"
							
				delete_button_names.append(delete_line_button_name)

		#end of for	
		
		#--------add new line components
		print "<tr><td>"+str(count)+"</td>"
		print "<td><input type='text' name='new_product_field'></td>"	
		print "<td><input type='text' name='new_code_field'></td>"
		print "<td><input type='text' name='new_targetweight_field'></td>"
		print "<td><input type='text' name='new_maxtolerance_field'></td>"
		print "<td><input type='text' name='new_mintolerance_field'></td>"
		print "<td><input type='submit' name='add_newline_button' value='add_newline'></td>"
		print "</tr>"

		#close the table
		print "</table>"	

		#Save/discard/Publish changes button
		print "<tr><td><input type='submit' name='revert_cfgfile_button' value='Revert to old file' title='Revert to old product config file'></td>"
		print "<td><input type='submit' name='save_tmp_changes_button' value='Save temp' title='Save changes to temporary product config'>" #buton to save changes 
		print "<input type='submit' name='discard_changes_button' value='Cancel' title='Cancel changes'>"#button to cancel	
		print "<input type='submit' name='apply_changes_button' value='Apply' title='Apply changes'></td></tr>"#button to publish	
		print "</td></tr></table></form>" #closing big table

		#-----------save/cancel/add buttons handler--------------

		add_newline_configfile_action=button_form.getvalue('add_newline_button')
		save_tmp_configfile_action = button_form.getvalue('save_tmp_changes_button')
		apply_tmp_configfile_action = button_form.getvalue('apply_changes_button')
		discard_tmp_configfile_action = button_form.getvalue('discard_changes_button')
		delete_line2_action=button_form.getvalue('delete_line2')
		new_product_value=str(button_form.getvalue('new_product_field'))
		new_code_value=str(button_form.getvalue('new_code_field'))
		new_targetweight_value=str(button_form.getvalue('new_targetweight_field'))
		new_maxtolerance_value=str(button_form.getvalue('new_maxtolerance_field'))
		new_mintolerance_value=str(button_form.getvalue('new_mintolerance_field'))

		#add
		if(add_newline_configfile_action=="add_newline"):
			if(new_product_value!='None' and new_code_value!='None'):
				addline_string=str(count)+","+new_product_value+","+new_code_value+","+new_targetweight_value+","+new_maxtolerance_value+","+new_mintolerance_value
				AppendLineConfFile(addline_string)
			else:
				print "<br><b><font color='red'>ERROR - Must introduce product name,code,target weight, min and max tolerance</font></b>"


		#save changes
		if(save_tmp_configfile_action=="Save temp"):
			print "<br>--Button save activated!"
			#os.system("ls >> config_files/example.csv")	#for debug purposes
			SaveTempConfFile(count)

		#apply changes
		if(apply_tmp_configfile_action=="Apply"):
			print "<br>--Button apply activated!"
			ApplyConfFileChanges()		
			

		#print "button state "+str(button_form.getvalue('save_changes_button'))


		#----------delete lines button handler---------------------
		
		if (Debug_Flag=="DEEP"):
			print "<br>--List of available buttons="
			for x in range(2,count+1):
				print "<br>---Count="+str(count)+","+str(delete_button_names[x-2])

		for w in range(2,count+1):
			if (Debug_Flag=="DEEP"):print "<br>----Button delete"+str(w)+" status="+str(button_form.getvalue(delete_button_names[w-2]))
			delete_button_action.append(button_form.getvalue(delete_button_names[w-2]))

			#------deleting line from tmp file
			if (button_form.getvalue(delete_button_names[w-2])=="delete_line"):
				
				#splitting button name to get line number
				split_list2=[]
				split_list2=delete_button_names[w-2].split('_')
				if (Debug_Flag=="DEEP"): print "<br>-----Delete Button name split "+str(split_list2)				
				DeleteLineConfFile(split_list2[2])

			#end of if
		
		if (Debug_Flag=="DEEP"): print "<br>--Button action status"+str(delete_button_action)

	if (Debug_Flag=="DEEP"):print "<br><b>Executed Function PrintTable. Debug_Flag=</b>"+Debug_Flag

###### notify stations about the prod-conf-file update
def NotifyStations(): 

	if (Debug_Flag=="DEEP"):print "<br><b>Executing Function NotifyStations. Debug_Flag=</b>"+Debug_Flag

	if (Debug_Flag=="DEEP"):print "<br><b>Executed Function NotifyStations. Debug_Flag=</b>"+Debug_Flag



######appends line to config file
def AppendLineConfFile(data):	

	if (Debug_Flag=="DEEP"):print "<br><b>Executing Function AppendLineConfFile. Debug_Flag</b>"	
	command_string="echo '"+data+"' >>"+configfiles_path+product_config_filename_tmp	
	if (Debug_Flag=="DEEP"):print "<br>--command_string="+command_string
	os.system(command_string)
	RedirectToUrl("EDIT_PRODUCT_CONFIG") # required for lack-of-table-refresh issue
	if (Debug_Flag=="DEEP"):print "<br><b>Executed Function AppendLineConfFile. Debug_Flag</b>"	

######Saves changes to temp product config file, captured from html input fields. 
def SaveTempConfFile(number_of_lines):

	global configfiles_path, product_config_filename_tmp

	if (Debug_Flag=="DEEP"):print "<br><b>Executing Function SaveConfFile. Count=</b>"+str(number_of_lines)

	#delete old tmp file
	if (Debug_Flag=="DEEP"):print "<br>--Deleting current tmp product config file"
	os.remove(configfiles_path+product_config_filename_tmp)  

	#saving file header
	command_string="echo 'N,Product,Code,TargetWeight(Kg),MaxTolerance(%),MinTolerance(%)' > "+configfiles_path+product_config_filename_tmp
	os.system(command_string) 
	#command_string="echo 'save,test,save,test' >> "+configfiles_path+product_config_filename_tmp
	#os.system(command_string) 

	for N in range(1,number_of_lines):
		
		Product = str(button_form.getvalue('product_field'+str(N+1)))
		Code=str(button_form.getvalue('code_field'+str(N+1)))
		TargetWeight=str(button_form.getvalue('targetweight_field'+str(N+1)))
		MaxTolerance=str(button_form.getvalue('maxtolerance_field'+str(N+1)))
		MinTolerance=str(button_form.getvalue('mintolerance_field'+str(N+1)))

		
		command_string="echo "+ str(N)+","+Product+","+Code+","+TargetWeight+","+MaxTolerance+","+MinTolerance+" >> "+configfiles_path+product_config_filename_tmp
		os.system(command_string)
		if (Debug_Flag=="DEEP"):print "<br>---Saving line into tmp file="+command_string
		
	#end of for	
	
	if (CheckProdConfigFileIntegrity(product_config_filename_tmp)==0):
		RedirectToUrl("EDIT_PRODUCT_CONFIG") # required for lack-of-table-refresh issue
	

	if (Debug_Flag=="DEEP"):print "<br><b>Ending Function SaveConfFile</b>"


#######Apply changes to  product config file
def ApplyConfFileChanges():

	global configfiles_path, product_config_filename_tmp,product_config_filename_old
	if (Debug_Flag=="DEEP"):print "<br><b>Executing Function ApplyConfFileChanges. Debug_Flag=</b>"+Debug_Flag

	#bring warning YES/NO popup window

	#check tmp file integrity - if its fine can proceed
	if (CheckProdConfigFileIntegrity(product_config_filename_tmp)==0):

		#create backup of original
		
		#--deleting old backup file
		if (Debug_Flag=="DEEP"):print "<br>--Deleting old backup of product config file="+configfiles_path+product_config_filename_old
		command_string="rm -f "+configfiles_path+product_config_filename_old
		if (Debug_Flag=="DEEP"):print "<br>---Command string="+command_string
		os.system(command_string)	 

		#--creating new backup of original 
		if (Debug_Flag=="DEEP"):print "<br>--Creating new backup"
		command_string="cp -f "+configfiles_path+product_config_filename +" "+configfiles_path+product_config_filename_old 	
		if (Debug_Flag=="DEEP"):print "<br>---Command string="+command_string
		os.system(command_string)

		#--delete current config file
		if (Debug_Flag=="DEEP"):print "<br>--Removing current new product config file="+configfiles_path+product_config_filename
		os.remove(configfiles_path+product_config_filename)
				
		#create new config product file
		if (Debug_Flag=="DEEP"):print "<br>--Creating current new product config file="+configfiles_path+product_config_filename		
		command_string="cp -f "+configfiles_path+product_config_filename_tmp+" "+configfiles_path+product_config_filename 
		os.system(command_string)

		#FIXME:notify stations on updates
		NotifyStations()
		
		#Force refresh
		RedirectToUrl("EDIT_PRODUCT_CONFIG") # required for lack-of-table-refresh issue

	if (Debug_Flag=="DEEP"):print "<br><b>Executed Function ApplyConfFileChanges. Debug_Flag=</b>"+Debug_Flag 

#########revert product config file to old version
def RevertConfFile():

	if (Debug_Flag=="DEEP"):print "<br><b>Executing Function RevertConfFile. Debug_Flag=</b>"+Debug_Flag

	if (Debug_Flag=="DEEP"):print "<br><b>Executed Function RevertConfFile. Debug_Flag=</b>"+Debug_Flag 

		
######delete line in  config file (store changes in tmp copy of product_config_filename)
def DeleteLineConfFile(line_number_to_replace):

	if (Debug_Flag=="DEEP"):print "<br><b>Executing Function DeleteLineConfFile. Debug_Flag=</b>"+Debug_Flag

	#sudo sed -i.bak -e '2d' product_config.csv.tmp #example of command
	command_string="sudo sed -i.bak -e '2d' ./config_files/product_config.csv.tmp"
	#command_string="sudo sed -i.bak -e "+line+"d "+configfiles_path+product_config_filename_tmp
	#command_string="sudo ls >> "+configfiles_path+product_config_filename_tmp
	#command_string = "ls"
	if (Debug_Flag=="DEEP"): print "<br>--Command string="+command_string
	#os.system(command_string)

	#command = os.popen(command_string)
	#command_result=command.read()
	#if (Debug_Flag=="DEEP"): print "<br>--Command execution result="+command_result	
	
	#subprocess.call(command_string)
	
	for line_number, line in enumerate(fileinput.input(configfiles_path+product_config_filename_tmp,inplace=1)):
		if line_number==(int(line_number_to_replace)-1):
			continue
		else:
			sys.stdout.write(line)

	RedirectToUrl("EDIT_PRODUCT_CONFIG") # required for lack-of-table-refresh issue
	if (Debug_Flag=="DEEP"):print "<br><b>Finished Function DeleteLineConfFile. Debug_Flag=</b>"+Debug_Flag


######main###########
def Main():

	checkConfigFile=-5000

	GetScriptState()

	if (script_state=="SHOW_PRODUCT_CONFIG"):
		
		if (Debug_Flag=="DEEP"):print "<br>--Try to open product config file="+configfiles_path+product_config_filename
		PrintTable("FALSE")
		checkConfigFile = CheckProdConfigFileIntegrity(product_config_filename)
		if (checkConfigFile==-2):
			print "<br><b><font color='red'>ERROR: unable to find product config file=</font></b>"+configfiles_path+product_config_filename
		
	elif (script_state=="EDIT_PRODUCT_CONFIG" or script_state=="EDIT_START_PRODUCT_CONFIG"):

		if (Debug_Flag=="DEEP"):print "<br>--Try to open product config file(edit mode)="+configfiles_path+product_config_filename
		if (os.path.isfile(configfiles_path+product_config_filename)==True):
			PrintTable("TRUE")

	#redirecting required because of PrintTable issue - not showing last update of product config file 
	#elif (script_state=="REDIRECT_TO_EDIT"):

		

###########END OF FUNCT###########################################

###########HTML###########

print "Content-type: text/html\n\n"
print "<body style='background-color:lightgrey'>"
button_form=cgi.FieldStorage()
PrintDefaultLinks()
print "<hr>"
PrintBarMenu()
print "<h2>Products</h2>"
print "<br>"

Main()