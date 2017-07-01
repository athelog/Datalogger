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
cgitb.enable()



print "Content-type: text/html\n\n"
button_form=cgi.FieldStorage()
print "<h2>CONFIG</h2>"
print "<br>"


def button():
	print "<form action='/cgi-bin/html_test.py?state=EDIT_PRODUCT_CONFIG' method='POST'>"
	print "<form action='/cgi-bin/html_test.py?state=EDIT_PRODUCT_CONFIG' >"
	print "<input type='submit' name='save_changes_button' value='Save'>" #buton to save changes 
	print "<input type='submit' name='discard_changes_button' value='Cancel'>"#button to cancel
	print "</form>"

def button2():
	print "<form action='/cgi-bin/html_test.py?state=EDIT_PRODUCT_CONFIG' method='POST'>"
	#print "<form action='/cgi-bin/html_test.py?state=EDIT_PRODUCT_CONFIG' >"
	print "<input type='submit' name='save_changes_button' value='Save'>" #buton to save changes 
	print "<input type='submit' name='discard_changes_button' value='Cancel'>"#button to cancel
	print "</form>"


#print "<form action='/cgi-bin/html_test.py?state=EDIT_PRODUCT_CONFIG' method='POST'>"
#print "<form action='/cgi-bin/html_test.py?state=EDIT_PRODUCT_CONFIG' >"
#print "<input type='submit' name='save_changes_button' value='Save'>" #buton to save changes 
#print "<input type='submit' name='discard_changes_button' value='Cancel'>"#button to cancel
#print "</form>"

button2()
	