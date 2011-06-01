from google.appengine.ext import webapp
import datetime

register = webapp.template.create_template_register()
def timeoffset(value, timedelta=0):
    timedelta = int(timedelta)
    t_timedelta = datetime.timedelta(seconds=3600*timedelta)
    return value + t_timedelta
register.filter(timeoffset)
