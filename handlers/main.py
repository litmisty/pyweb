# -*- coding: utf-8 -*-
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

