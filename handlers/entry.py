# -*- coding: utf-8 -*-
import os
import logging
import datetime
import urllib
import hashlib

from google.appengine.ext import db
from google.appengine.ext.webapp.util import login_required
from google.appengine.api import users


from models.MenuModel import Menu
from models.UserModel import User, UserStatus
from models.EntryModel import Entry, EntryForm, EntryRecaptchaForm
from models.CommentModel import Comment, CommentForm, CommentRecaptchaForm
from models.Paging import Paging, PagingCursorMasterKey

from models.ErrorMessage import getSiteErrorMessage, SiteErrorType 
from models.Cookies import Cookies
from models.ReCaptcha import ReCaptcha

from Handler import Handler


def checkUserStatus(func):
    def wrapper(self, *args, **kw):
        user = users.get_current_user()
        if user:
            siteUser = User.getSiteUser(user)
            if siteUser and siteUser.status > UserStatus.USER_NORMAL:
                self.redirect("/error/user_banned")
                return
        func(self, *args, **kw)
            
    return wrapper

def checkCSRFToken(func):
    def wrapper(self, *args, **kw):
        cookies = Cookies( self )
        cookie_token = cookies['csrf_token']
        form_token = self.request.get("csrf_token")

        if not cookie_token or cookie_token == "" or not form_token or form_token == "" :
            self.siteError( SiteErrorType.ERROR_INVALID_ACCESS )
            return
        
        if cookie_token != form_token:
            self.siteError( SiteErrorType.ERROR_INVALID_ACCESS )
            return
        
        func(self, *args, **kw)
        
    return wrapper
        
        


class MainHandler(Handler):
    def __init__(self):
        self.context['user'] = users
        
    def createCSRFToken(self):
        if not self.context['user'].get_current_user():
            return
        
        
        siteUser = User.getSiteUser( self.context['user'].get_current_user() )
        
        if not siteUser:
            siteUser = User.insertUser( self.context['user'].get_current_user(), self.request.remote_addr )
          
        m = hashlib.md5()  
        # prepare salt
        if siteUser.last_write_on:            
            m.update( siteUser.last_write_on.strftime("%Y/%m/%d %H:%M:%S.%f") )
        else:
            m.update( siteUser.join_on.strftime("%Y/%m/%d %H:%M:%S.%f") )
        m.update( str( siteUser.key().id() ) )
        
        self.context['csrf_token'] = m.hexdigest()
        
        cookies = Cookies( self )
        cookies['csrf_token'] = self.context['csrf_token']        
                
    def get_current_user(self):
        if not self.context['user'] or not self.context['user'].get_current_user():
            return None
        
        return self.context['user'].get_current_user()
        
        
        
        
class ErrorHandler(MainHandler):
    def get(self, error_type):                
        self.siteError( getSiteErrorMessage(error_type) )
        return


class ListHandler(MainHandler):
    def get(self, menu_identifier=None, cursor=None):
        if menu_identifier is None or not Menu.isRightIdentifier(menu_identifier):
            self.siteError( SiteErrorType.ERROR_MENU_NOT_EXIST )
            return
        
        self.context['menu_id'] = Menu.getMenuIdWithIdentifier( menu_identifier )
        self.context['menu_label'] = Menu.getLabel( self.context['menu_id'] )
        self.context['menu_identifier'] = menu_identifier
        
        LIST_NUMS = 5
        
        if cursor:
            cursor = urllib.unquote(cursor).decode('utf-8')
            
        query = Entry.all()
        query.filter("menu_id", self.context['menu_id'] )
        query.filter("is_removed", False)
        query.order("-created_on")
        
        paging = Paging( query )
        paging.setCurrentCursor( cursor )
        paging.setLimit( LIST_NUMS )
        paging.execute()
    
        self.context['paging'] = paging
                
        self.render( "list.html" )

class RSSHandler(MainHandler):
    def get(self, menu_identifier=None):

        LIST_NUMS = 10
            
        query = Entry.all()
        query.filter("is_removed", False)
        query.order("-created_on")
        
        paging = Paging( query )
        paging.setLimit( LIST_NUMS )
        paging.execute()
        
    
        self.context['paging'] = paging
                
        self.render( "rss.xml" )


class ViewHandler(MainHandler):
    def get(self, index):
        entry = Entry.get_entry(index)

        if not entry or entry.is_removed:
            self.siteError( SiteErrorType.ERROR_ENTRY_NOT_EXIST )
            return

        
        if self.context['user'] and User.isUserNeedCaptcha( self.get_current_user() ):
            comment_form = CommentRecaptchaForm(self.request.remote_addr)
        else:
            comment_form = CommentForm()
        
        
        self.context['comment_form'] = comment_form
        self.context['entry'] = entry
        
        if self.context['user']:
            self.createCSRFToken()
        
        self.render( "view.html" )



class WriteMainHandler(MainHandler):
    @login_required
    def get(self):
        self.render( "write_main.html" )


class WriteHandler(MainHandler):
    
    @login_required
    @checkUserStatus
    def get(self, menu_identifier=None):
        if menu_identifier is None or not Menu.isRightIdentifier(menu_identifier):
            self.siteError( SiteErrorType.ERROR_MENU_NOT_EXIST )
            return

        
        self.context['menu_id'] = Menu.getMenuIdWithIdentifier( menu_identifier )
        self.context['menu_label'] = Menu.getLabel( self.context['menu_id'] )
        self.context['menu_identifier'] = menu_identifier
        
        
        
        self.createCSRFToken()

        if self.context['user'] and User.isUserNeedCaptcha( self.get_current_user() ):
            entry_form = EntryRecaptchaForm(self.request.remote_addr)
        else:
            entry_form = EntryForm()
        
        
        self.context['entry_form'] = entry_form
        

        self.render( "write.html" )
        
    
    @checkUserStatus
    @checkCSRFToken
    def post(self, menu_identifier=None):
            
        if menu_identifier is None or not Menu.isRightIdentifier(menu_identifier):
            self.siteError( SiteErrorType.ERROR_MENU_NOT_EXIST )
            return

        user = self.context['user'].get_current_user()
        if not user:
            self.redirect( users.create_login_url("/write/"+menu_identifier ) )
            
        remote_addr = self.request.remote_addr        
        if not remote_addr:
            self.siteError( getSiteErrorMessage("invalid_access") )
            return
                    
        self.context['menu_id'] = Menu.getMenuIdWithIdentifier( menu_identifier )
        self.context['menu_label'] = Menu.getLabel( self.context['menu_id'] )
        self.context['menu_identifier'] = menu_identifier
        
        if self.context['user'] and User.isUserNeedCaptcha( self.get_current_user() ):
            entry_form = EntryRecaptchaForm(remote_addr, data=self.request.POST)
        else:
            entry_form = EntryForm(data=self.request.POST)
            
        if entry_form.is_valid():
            # insert
            # check user            
            User.insertUser(user, remote_addr)
            menu_id = self.context['menu_id']
            Entry.insert( entry_form.cleaned_data['title'], entry_form.cleaned_data['link'], entry_form.cleaned_data['content'], menu_id, user, remote_addr )
            self.redirect("/list/"+Menu.getMenuIdentifier( menu_id) )
        else:
            self.createCSRFToken()
            self.context['entry_form'] = entry_form
            self.render( "write.html" )




class EditHandler(MainHandler):
    @login_required
    @checkUserStatus
    def get(self, index=None):
        self.context['index'] = index
        
        entry = Entry.get_entry( index )
        
        if not entry or entry.is_removed:
            self.siteError( getSiteErrorMessage("entry_not_exist") )
            return
        
        if entry.user != self.context['user'].get_current_user() and not self.user.is_current_user_admin() :
            self.siteError( getSiteErrorMessage("invalid_access") )
            return
                
        entry_form = EntryForm(instance=entry)
        self.context['entry_form'] = entry_form
        
        self.createCSRFToken()

        self.render( "edit.html" )
        
    
    @checkUserStatus
    @checkCSRFToken
    def post(self, index=None):
        self.context['index'] = index
        
        entry = Entry.get_entry( index )
        
        if not entry or entry.is_removed:
            self.siteError( getSiteErrorMessage("entry_not_exist") )
            return
        
        if entry.user != self.context['user'].get_current_user() and not self.user.is_current_user_admin() :
            self.siteError( getSiteErrorMessage("invalid_access") )
            return
        
        remote_addr = self.request.remote_addr        
        if not remote_addr:
            self.siteError( getSiteErrorMessage("invalid_access") )
            return
        
        
        entry_form = EntryForm(data=self.request.POST, instance=entry)
        
        if entry_form.is_valid():

            entry = entry_form.save(commit=False)
            if entry.link and entry.link.find("http") == -1 :
                entry.link = "http://" + entry.link
            
            entry.put()
            
            self.redirect("/entry/"+index)
        else:
            self.context['entry_form'] = entry_form
            self.render( "edit.html" )
            
            
class WriteCommentHandler(MainHandler):
    @checkUserStatus
    @checkCSRFToken
    def post(self, index=None):
        if not self.context['user'].get_current_user():
            self.siteError( SiteErrorType.ERROR_INVALID_ACCESS )
            return
            
        self.context['index'] = index
        
        entry = Entry.get_entry( index )
        
        if not entry or entry.is_removed:
            self.siteError( getSiteErrorMessage("entry_not_exist") )
            return
            
        remote_addr = self.request.remote_addr        
        if not remote_addr:
            self.siteError( getSiteErrorMessage("invalid_access") )
            return
        user = self.context['user'].get_current_user()
        User.insertUser(user, remote_addr)
        
        
        if self.context['user'] and User.isUserNeedCaptcha( self.get_current_user() ):
            comment_form = CommentRecaptchaForm(self.request.remote_addr, data = self.request.POST)
        else:
            comment_form = CommentForm(data = self.request.POST)
            
        if comment_form.is_valid():
            comment = Comment.insert(entry, comment_form.cleaned_data['content'], user, remote_addr)
            
            entry.comment_count = entry.comment_count + 1
            entry.updated_on = datetime.datetime.now()
            entry.put()
            
            PagingCursorMasterKey.clearModelKey("Comment")
            
            self.redirect("/entry/%s#comment%d"%(index, comment.id()))
            
        else:
            self.createCSRFToken()
            self.context['entry'] = entry
            self.context['comment_form'] = comment_form
            self.render("view.html")
        


class UserHandler(MainHandler):
    @login_required
    def get(self, cursor=None):
        siteUser = User.getSiteUser( self.context['user'].get_current_user() )
        if not siteUser:
            siteUser = User.insertUser(self.context['user'].get_current_user(), self.request.remote_addr )
            
        self.context['siteUser'] = siteUser
        LIST_NUMS = 10
        
        query = Entry.all()
        query.filter("site_user_id", User.getSiteUserId( self.context['user'].get_current_user() ) )
        query.filter("is_removed", False )
        query.order("-created_on")
        
        paging = Paging( query )
        paging.setCurrentCursor( cursor )
        paging.setLimit( LIST_NUMS )
        paging.execute()
        
        
        self.context['paging'] = paging
        
        
        self.render("user.html")



            
class TestHandler(MainHandler):
    def get(self):
        pass
        
        


EntryPath = [('/test/?', TestHandler),
             ('/error/([a-zA-Z_]+)/?', ErrorHandler),
             ('/list/([a-z]+)/?', ListHandler),
             ('/list/([a-z]+)/(.*?)/?', ListHandler),
             ('/entry/(\d+)/?', ViewHandler),
             ('/write/?', WriteMainHandler),
             ('/write/([a-z]+)/?', WriteHandler),
             ('/edit/(\d+)/?', EditHandler),
             ('/write_comment/(\d+)/?', WriteCommentHandler),
             ('/user/?', UserHandler),
             ('/user/(.*?)/?', UserHandler),
             ('/rss/?', RSSHandler),
            ];
