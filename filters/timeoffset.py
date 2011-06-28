# pyweb-ko
# timeoffset.py
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
from google.appengine.ext import webapp
import datetime

register = webapp.template.create_template_register()
def timeoffset(value, timedelta=0):
    timedelta = int(timedelta)
    t_timedelta = datetime.timedelta(seconds=3600*timedelta)
    return value + t_timedelta
register.filter(timeoffset)
