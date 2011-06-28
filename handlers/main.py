# -*- coding: utf-8 -*-
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
from google.appengine.api import users

from Handler import Handler

from models.EntryModel import Entry
from models.MenuModel import Menu

class MainHandler(Handler):
    def __init__(self):
        self.context['user'] = users


class IndexHandler(MainHandler):
    def get(self):
        entries = {}
        entries['news'] = Entry.all().filter('is_removed', False).filter("menu_id", Menu.MENU_NEWS).order("-created_on").fetch(5, 0)
        entries['free'] = Entry.all().filter('is_removed', False).filter("menu_id", Menu.MENU_FREE).order("-created_on").fetch(5, 0)
        entries['tips'] = Entry.all().filter('is_removed', False).filter("menu_id", Menu.MENU_TIPS).order("-created_on").fetch(5, 0)
        entries['qna'] = Entry.all().filter('is_removed', False).filter("menu_id", Menu.MENU_QNA).order("-created_on").fetch(5, 0)
        
            
        self.context['entries'] = entries
        
        self.render( "index.html" )


class AboutHandler(MainHandler):
    def get(self):
        self.render( "about.html" )


class NotFoundHandler(MainHandler):
    def get(self):
        self.error(404)
        self.render("404.html")


MainPath = [('/', IndexHandler),
            ('/about/?', AboutHandler),
            ('/.*', NotFoundHandler)
            ];

