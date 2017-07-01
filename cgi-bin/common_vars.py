#!/usr/bin/env python
import cgi
import cgitb
import sys



#####debugging##############
cgitb.enable()
###########################

########################################SCRIPT CONST########################

language = "SP" #SP=Spanish, ENG=english




####stats plots

analysis_basefolder = "/cgi-bin/analysis/"
plot_width="400" #to print in html page
plot_height="400" #to print in html page
bars_plot_filename="bars_plot"
pie_plot_filename="pie_plot"
histogram_plot_filename="hist_plot"


###########################################################################