# pyweb-ko
# user_status_label.py
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
register = webapp.template.create_template_register()

from models.UserModel import UserStatus

def user_status_label(value):
    label = UserStatus.getStatusLabel(value)
    return label

register.filter(user_status_label)
