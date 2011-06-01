#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import datetime


kind_list = ['Entry', 'EntryIndex', 'Comment', 'User']

appcfg_path = "/Users/mimu/dev/google_appengine/appcfg.py"
app_url = "http://pyweb-ko.appspot.com/remote_api"
data_path = "/home/mimu/dev/appengine/data/django-ko/data"


current_path = os.getcwd()

# make path
if not os.path.isdir(data_path):
    os.mkdir(data_path)

#make current path
current_string = datetime.datetime.now().strftime("%Y_%m_%d_%H%M%S")
working_path = "%s/%s" %( data_path, current_string )

if not os.path.isdir(working_path):
    os.mkdir(working_path)



    

# save csv files
for kind in kind_list:
    filename = "%s/%s.csv" % (working_path, kind)
    command = "%s download_data --config_file=%s/bulkloader.yaml --kind=%s --url=%s --filename=%s" % ( appcfg_path, current_path, kind, app_url, filename)
    os.system( command )


#delete log files
command = "rm %s/*.sql3" % ( current_path )
os.system( command )
command = "rm %s/bulkloader-log-*" % ( current_path)
os.system( command )
    

# save raw backup files
for kind in kind_list:
    filename = "%s/%s.data" % (working_path, kind)
    command = "%s download_data --application=django-ko --kind=%s --url=%s --filename=%s" % ( appcfg_path, kind, app_url, filename)
    
    os.system( command )


