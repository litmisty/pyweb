# pyweb-ko
# main.py
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

import os, re
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings' 
from google.appengine.dist import use_library
use_library('django', '1.2')
from django.conf import settings
_ = settings.TEMPLATE_DIRS

from google.appengine.ext import webapp
from google.appengine.ext.webapp import util
from google.appengine.ext.webapp import template

from handlers.main import MainPath
from handlers.admin import AdminPath
from handlers.entry import EntryPath


def initFilters():
    filters_root = os.path.join(os.path.dirname(__file__), 'filters')
    if os.path.exists(filters_root):
        filters = os.listdir(filters_root)
        for filter in filters:
            if not re.match('^__|^\.|.*pyc$', filter ):
                template.register_template_library('filters.'+filter.replace(".py","" ) )



def main():
    initFilters()
    application = webapp.WSGIApplication(
                                         AdminPath+
                                         EntryPath+
                                         MainPath,
                                         debug=True)
    util.run_wsgi_app(application)

if __name__ == "__main__":
    main()
