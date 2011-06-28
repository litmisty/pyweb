#!/usr/bin/python
# -*- coding: utf-8 -*-
# bulk_download.py
# Copyright (C) 2011  mimu
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

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


