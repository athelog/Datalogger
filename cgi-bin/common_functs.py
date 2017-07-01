#!/usr/bin/env python
import cgi
import cgitb
import sys



#####debugging##############
cgitb.enable()
###########################

########################################SCRIPT CONST########################

language = "SP" #SP=Spanish, ENG=english


########################################SCRIPT VARS#########################

script_status="STD" #STD=standard view



########################################FUNCT DEFINITION####################

###print html links  
def PrintLinks():

	if (language=="SP"):

		Report_link="<a href='/cgi-bin/report.py' title='Reporte'><img width='70' height='70' border='0' alt='Reporte' src='./html_common/report_icon.png'></a>"
		Products_link="<a href='/cgi-bin/products.py?STATE=SHOW_PRODUCT_CONFIG' title='Productos'><img width='70' height='70' border='0' alt='Productos' src='./html_common/products_icon.png'></a>"
		Users_link="<a href='/cgi-bin/users.py?state=START' title='Usuarios'><img width='70' height='70' border='0' alt='Usuarios' src='./html_common/users_icon.png'></a>"
		Manual_link="<a href='/cgi-bin/manual.py?state=START' title='Manual'><img width='70' height='70' border='0' alt='Manual' src='./html_common/manual_icon.png'></a>"
		Log_link="<a href='/cgi-bin/log.py?state=START' title='Log'><img width='70' height='70' border='0' alt='Log' src='./html_common/log_icon.png'></a>"
		About_link="<a href='/cgi-bin/about.py?state=START' title='Acerca de'><img width='70' height='70' border='0' alt='Acerca de' src='./html_common/about_icon.png'></a>"
		Stations_link="<a href='/cgi-bin/stations.py?state=START' title='Estaciones'><img width='70' height='70' border='0' alt='Estaciones' src='./html_common/stations_icon.png'></a>"
	
		print "<table border='1'>"
		print "<tr><td><b>Link</b></td><td><b>Descripcion</b></td></tr>"
		print "<tr><td>"+Report_link+"</td><td>Generar reportes en formato CSV</td></tr>"
		print "<tr><td>"+Products_link+"</td><td>Editar archivo de configuracion;" 
		print "<br>agregar nuevo producto/codigo</td></tr>"
		print "<tr><td>"+Users_link+"</td><td>Anadir/Editar usuarios</td></tr>"
		print "<tr><td>"+Manual_link+"</td><td>Manual de usuario</td></tr>"
		print "<tr><td>"+Stations_link+"</td><td>Estaciones</td></tr>"
		print "<tr><td>"+Log_link+"</td><td>Log del servidor</td></tr>"
		print "<tr><td>"+About_link+"</td><td>Informacion acerca de</td></tr>"
		print "</table>"

	else:
	
		Report_link="<a href='/cgi-bin/report.py' title='Report'><img width='70' height='70' border='0' alt='Report' src='./html_common/report_icon.png'></a>"
		Products_link="<a href='/cgi-bin/config.py?state=START' title='Producs'><img width='70' height='70' border='0' alt='Products' src='./html_common/products_icon.png'></a>"
		Users_link="<a href='/cgi-bin/users.py?state=START' title='Users'><img width='70' height='70' border='0' alt='Users' src='./html_common/users_icon.png'></a>"
		Manual_link="<a href='/cgi-bin/manual.py?state=START' title='Manual'><img width='70' height='70' border='0' alt='Manual' src='./html_common/manual_icon.png'></a>"
		Log_link="<a href='/cgi-bin/log.py?state=START' title='Log'><img width='70' height='70' border='0' alt='Log' src='./html_common/log_icon.png'></a>"
		About_link="<a href='/cgi-bin/about.py?state=START' title='About'><img width='70' height='70' border='0' alt='About' src='./html_common/about_icon.png'></a>"
		Stations_link="<a href='/cgi-bin/stations.py?state=START' title='Stations'><img width='70' height='70' border='0' alt='About' src='./html_common/stations_icon.png'></a>"
	
		print "<table border='1'>"
		print "<tr><td><b>Link</b></td><td><b>Description</b></td></tr>"
		print "<tr><td>"+Report_link+"</td><td>Generate reports in CSV format</td></tr>"
		print "<tr><td>"+Products_link+"</td><td>Edit config file; add new product name/code</td></tr>"
		print "<tr><td>"+Users_link+"</td><td>Add/Edit users</td></tr>"
		print "<tr><td>"+Manual_link+"</td><td>User manual</td></tr>"
		print "<tr><td>"+Stations_link+"</td><td>Stations</td></tr>"
		print "<tr><td>"+Log_link+"</td><td>Server log</td></tr>"
		print "<tr><td>"+About_link+"</td><td>About info</td></tr>"
		print "</table>"

	#print "<img src='sas_banner_1.png'>"
	#print "<img src='./html_common/sas_banner_1.png'>"

###print default links
def PrintDefaultLinks():

	if(language=="SP"):
		print "<a href='/cgi-bin/index.py'>Indice</a>"
		print "<a href='/cgi-bin/report.py'>Reporte</a>"
		print "<a href='/cgi-bin/products.py?STATE=SHOW_PRODUCT_CONFIG'>Productos</a>"
		print "<a href='/cgi-bin/users.py?state=START'>Usuarios</a>"
		#FIXME: enble real manual #print "<a href='/cgi-bin/docs/manual.pdf'>Manual</a>"
		print "<a href='/cgi-bin/manual.py'>Manual</a>"
		print "<a href='/cgi-bin/log.py?state=START'>Log</a>"
		print "<a href='/cgi-bin/about.py?state=START'>Acerca de</a>"

	else:
		print "<a href='/cgi-bin/index.py'>Index</a>"
		print "<a href='/cgi-bin/report.py'>Report</a>"
		print "<a href='/cgi-bin/products.py?STATE=SHOW_PRODUCT_CONFIG'>Products</a>"
		print "<a href='/cgi-bin/users.py?state=START'>Users</a>"
		#FIXME: enble real manual #print "<a href='/cgi-bin/docs/manual.pdf'>Manual</a>"
		print "<a href='/cgi-bin/manual.py'>Manual</a>"
		print "<a href='/cgi-bin/log.py?state=START'>Log</a>"
		print "<a href='/cgi-bin/about.py?state=START'>About</a>"


#######################################END OF FUNCT DEF######################



