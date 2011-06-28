# -*- coding: utf-8 -*-
# pyweb-ko
# admin.py
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.import logging 
import urllib

#from google.appengine.ext import db
from google.appengine.api import users

from Handler import Handler


#from models.MenuModel import Menu
from models.UserModel import User, UserStatus
from models.EntryModel import Entry
from models.CommentModel import Comment
from models.Paging import Paging

from models.ErrorMessage import SiteErrorType

def adminRequired(func):
    def wrapper(self, *args, **kw):
        user = users.get_current_user()
        if not user:
            self.redirect(users.create_login_url(self.request.uri))
        else:
            if not users.is_current_user_admin():
                self.siteError( SiteErrorType.ERROR_INVALID_ACCESS )
                return
            else:
                func(self, *args, **kw)
            
    return wrapper


class AdminHandler(Handler):
    def __init__(self):
        self.context['user'] = users
        self.context['auth_url'] = users.create_logout_url("/")




class IndexHandler(AdminHandler):
    @adminRequired
    def get(self):
        self.render( "admin/index.html" )
        
        
                

class EntryHandler(AdminHandler):
    @adminRequired
    def get(self, cursor=None):
        
        LIST_NUMS = 10
        
        if cursor:
            cursor = urllib.unquote(cursor).decode('utf-8')
        
        self.context['siteUser'] = None
        
        query = Entry.all()
        query.filter("is_removed", False)
        query.order("-created_on")
        
        paging = Paging( query )
        paging.setCurrentCursor( cursor )
        paging.setLimit( LIST_NUMS )
        paging.execute()    
        self.context['paging'] = paging                
        
        self.render( "admin/entry.html" )


class CommentHandler(AdminHandler):
    @adminRequired
    def get(self, cursor=None):
        
        if cursor:
            cursor = urllib.unquote(cursor).decode('utf-8')
            
        query = Comment.all()
        query.order("-created_on")
        
        paging = Paging(query)
        paging.setLimit(10)
        paging.setCurrentCursor(cursor)
        paging.execute()
    
        self.context['paging'] = paging                
        
        self.render( "admin/comment.html" )


class UserHandler(AdminHandler):
    @adminRequired
    def get(self, cursor=None):
        if cursor:
            cursor = urllib.unquote(cursor).decode('utf-8')
            
        query = User.all()
        query.order("-join_on")
        
        paging = Paging( query )
        paging.setLimit(20)
        paging.setCurrentCursor(cursor)
        paging.execute()
        
        self.context['paging'] = paging
            
        self.render( "admin/user.html" )



class UserEntryHandler(AdminHandler):
    @adminRequired
    def get(self, type, site_user_id, cursor=None):
        logging.info( type )
        if type != "entry" and type != "comment":
            self.siteError( SiteErrorType.ERROR_INVALID_ACCESS )
            return
        
        if cursor:
            cursor = urllib.unquote(cursor).decode('utf-8')
            
        self.context['siteUser'] = User.get_by_id( int( site_user_id ) )
            
        if type == "entry":
            query = Entry.all()
            query.filter("site_user_id", int( site_user_id) )
            query.filter("is_removed", False)
            query.order("-created_on")
        elif type == "comment":
            query = Comment.all()
            query.filter("site_user_id", int( site_user_id) )
            query.order("-created_on")
        
        
        logging.info( query.__dict__ )
        paging = Paging( query )
        paging.setLimit(10)
        paging.setCurrentCursor(cursor)
        paging.execute()        
        
        self.context['paging'] = paging
        
        if type == "entry":
            self.render( "admin/entry.html" )
        elif type == "comment":
            self.render( "admin/comment.html" )
            



        

class EntryDeleteHandler(AdminHandler):
    @adminRequired
    def get(self, entry_index=None):
        entry = Entry.get_entry(entry_index)
        if not entry or entry.is_removed:
            self.siteError( SiteErrorType.ERROR_ENTRY_NOT_EXIST )
            return
        
        self.context['entry'] = entry
        self.render('admin/delete.html')
        pass
    
    
    @adminRequired
    def post(self, entry_index=None):
        entry = Entry.get_entry(entry_index)
        if not entry or entry.is_removed:
            self.siteError( SiteErrorType.ERROR_ENTRY_NOT_EXIST )
            return
        
        is_spam = self.request.get('is_spam')
        
        if is_spam:
            # block user
            siteUser = User.getSiteUser( entry.user )
            siteUser.status = UserStatus.USER_BANED
            siteUser.put()
            
            site_user_id = siteUser.key().id()
            
            # delete user's comment
            Comment.delete_with_user_id(site_user_id)
            
            # delete user's entry
            Entry.delete_with_user_id(site_user_id)
            
        
        #delete comment
        for comment in entry.comments:
            comment.delete()
            
        Entry.delete_entry(entry_index)
        
        self.redirect( "/admin/entry" )
        

class CommentDeleteHandler(AdminHandler):
    @adminRequired
    def get(self, comment_id=None):
        comment_id = int( comment_id )
        comment = Comment.get_by_id( comment_id )
        
        if not comment:
            self.siteError( SiteErrorType.ERROR_COMMENT_NOT_EXIST )
            return
        
        self.context['comment'] = comment
        self.render('admin/delete_comment.html')
        pass
    
    @adminRequired
    def post(self, comment_id=None):
        comment_id = int( comment_id )
        comment = Comment.get_by_id( comment_id )
        if not comment:
            self.siteError( SiteErrorType.ERROR_COMMENT_NOT_EXIST )
            return
        
        siteUser = User.getSiteUser( comment.user )
        Comment.delete_comment(comment)
        
        is_spam = self.request.get('is_spam')
        if is_spam:
            siteUser.status = UserStatus.USER_BANED
            siteUser.put()
            
            site_user_id = siteUser.key().id()
            
            # delete user's comment
            Comment.delete_with_user_id(site_user_id)
            
            # delete user's entry
            Entry.delete_with_user_id(site_user_id)
        
        self.redirect( '/admin/comment' )
            

AdminPath = [('/admin/?', IndexHandler),
             ('/admin/entry/?', EntryHandler),
             ('/admin/entry/(.*)/?', EntryHandler),
             ('/admin/comment/?', CommentHandler),
             ('/admin/comment/(.*)/?', CommentHandler),
             ('/admin/entry_delete/(\d+)/?', EntryDeleteHandler),
             ('/admin/comment_delete/(\d+)/?', CommentDeleteHandler),
             ('/admin/user/?', UserHandler),
             ('/admin/userEntry/(entry|comment)/(\d+)/?', UserEntryHandler),
             ('/admin/userEntry/(entry|comment)/(\d+)/(.*?)/?', UserEntryHandler),
             ];

