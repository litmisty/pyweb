#!/usr/bin/python
# -*- coding: utf-8 -*-
import os, sys
import datetime


kind_list = ['Entry', 'EntryIndex', 'Comment', 'User']

appcfg_path = "/Users/mimu/dev/google_appengine/appcfg.py"
app_url = "http://pyweb-ko.appspot.com/remote_api"
data_path = "/home/mimu/dev/appengine/data/django-ko/data"


current_path = os.getcwd()

#check files
if len( sys.argv ) < 2:
    print "please select data directory"
    sys.exit()
    
working_path = sys.argv[1]
if not os.path.isdir( working_path ):
    print "%s is not directory" % working_path
    sys.exit()
    
for kind in kind_list:
    filename = "%s/%s.data"%( working_path, kind )
    if os.path.isfile( filename ):
        command = "%s upload_data --filename=%s --kind=%s --url=%s" % (appcfg_path, filename, kind, app_url )
        os.system( command )



#delete log files
command = "rm %s/*.sql3" % ( current_path )
os.system( command )
command = "rm %s/bulkloader-log-*" % ( current_path)
os.system( command )
