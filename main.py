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
