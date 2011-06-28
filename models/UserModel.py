# -*- coding: utf-8 -*-
# pyweb-ko
# UserModel.py
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
from google.appengine.ext import db
import datetime
from Paging import PagingCursorMasterKey

class UserStatus:
    USER_NORMAL = 0
    USER_BLOCKED = 1
    USER_BANED = 2
    
    @classmethod
    def getStatusLabel(cls, status):
        status_label = {
                        cls.USER_NORMAL:"정상",
                        cls.USER_BANED:"영구 차단",
                        cls.USER_BLOCKED:"일시 차단",
                        }
        if status_label.has_key( status ):
            return status_label[status]
    
class User(db.Model):
    google_user_id = db.StringProperty()
    email = db.EmailProperty()
    nickname = db.StringProperty()
    status = db.IntegerProperty(default=0)
    join_on = db.DateTimeProperty(auto_now_add = 1)
    last_write_on = db.DateTimeProperty()
    last_ip = db.StringProperty()
    
    
    @classmethod
    def isUserExist(cls, user):
        query = User.all().filter("google_user_id =", user.user_id())
        userRow = query.fetch(10)        
        
        if len(userRow) > 0:
            return True
        else:
            return False
        
    @classmethod
    def insertUser(cls, user, ip):
        if cls.isUserExist(user) :
            cls.updateLastWrited(user, ip)
            return
        
        new_user = User( google_user_id = user.user_id(),
                         email = user.email(),
                         nickname = user.nickname(),
                         last_ip = ip )
        
        new_user.put()
        PagingCursorMasterKey.clearModelKey("User")
        return new_user 
        
    @classmethod
    def getSiteUser(cls, user):
        if not user:
            return None
        query = cls.all().filter("google_user_id =", user.user_id() )
        return query.get()
    
    @classmethod
    def getSiteUserId(cls, user):
        if not user:
            return None
        return cls.getSiteUser(user).key().id()
    
    
    @classmethod
    def updateLastWrited(cls, user, ip):
        siteUser = cls.getSiteUser(user)
        siteUser.last_write_on = datetime.datetime.now()
        siteUser.last_ip = ip
        siteUser.put()
        
    @classmethod
    def isUserNeedCaptcha(cls, user=None):
        siteUser = cls.getSiteUser(user)
        if not siteUser:
            return True
        
        # last_write_on is less than 5min or bigger than 7 days
        if not siteUser.last_write_on:
            return True
        
        delta = datetime.datetime.now() - siteUser.last_write_on
        if delta.seconds < 5*60 or delta.seconds > 3600*24*7:
            return True

        return False
        
    
    