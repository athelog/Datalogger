#!/usr/bin/env python
import cgi
import cgitb
import sys

#FIXME:uncomment SAS info

########CONST########################

language="SP"#SP=spanish




#######HTML FORMS####################
print "Content-type: text/html\n\n"
print "<body style='background-color:white'>"

if(language=="SP"):print "<a href='/cgi-bin/index.py'>Indice</a>"
else:print "<a href='/cgi-bin/index.py'>Index</a>"

print "<hr>"
if(language=="SP"):print "<h2>Acerca de</h2>"
else:print "<h2>About</h2>"

print "<br>Datalogger v1.0. Updated Nov 2015"
#print "<br>Design by SAS.SA"

if(language=="SP"):print "<br><b>Contacto:</b>"
else:print "<br><b>Contact:</b>"

print "<br>&nbsp Phone: +506 8917-3644 +506 8864-2093"
print "<br>&nbsp Mail: ramirovq@gmail.com bvrolo@yahoo.es"
print "<br>"
#print "<br><img src='./html_common/sas_banner_2.png' style='width:800px;height:100px;border:0'>"

if(language=="SP"):print "<br>Iconos por " + "<a href='http://www.iconshock.com'>www.iconshock.com</a>"  
else:print "<br>Icons by " + "<a href='http://www.iconshock.com'>www.iconshock.com</a>"

