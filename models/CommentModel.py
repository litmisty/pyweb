# -*- coding: utf-8 -*-
# pyweb-ko
# CommentModel.py
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
from google.appengine.ext.db import djangoforms

from django import forms

from EntryModel import Entry
from UserModel import User
from Paging import PagingCursorMasterKey
from forms import Recaptcha

import logging
    
class Comment(db.Model):
    entry = db.ReferenceProperty(Entry, collection_name='comments')
    entry_index = db.IntegerProperty()
    
    content = db.TextProperty(required=True) 
    created_on = db.DateTimeProperty(auto_now_add = 1)
    
    user = db.UserProperty()
    site_user_id = db.IntegerProperty()
    ip = db.StringProperty()
    
    @classmethod
    def insert(cls, entry, content, user, remote_addr):
        comment = Comment(
            entry = entry,
            entry_index = entry.index,
            content=content,
            user = user,
            site_user_id = User.getSiteUserId(user),
            ip = remote_addr
        ).put()
        return comment
    
    
    @classmethod
    def delete_comment(cls, comment):
        entry = comment.entry
        if entry:
            entry.comment_count -= 1
            
            entry.put()
             
        comment.delete()
        PagingCursorMasterKey.clearModelKey("Comment")
        
    
    
    @classmethod
    def delete_with_user_id(cls, site_user_id):
        query = Comment.all()
        query.filter("site_user_id", site_user_id)
        comments = query.fetch(500, 0)
        
        while comments:
            for comment in comments:
                cls.delete_comment(comment)
                
            query.with_cursor( query.cursor() )
            comments = query.fetch(500, 0 )
            
        PagingCursorMasterKey.clearModelKey("Comment")
    
    
class CommentForm(djangoforms.ModelForm):
    
    content = forms.CharField(required=True, label="코멘트", widget=forms.Textarea({'rows':5, 'cols':50, 'class':'editor comment_form'}))
    
    class Meta:
        model = Comment
        exclude = ['entry', 'created_on', 'user', 'site_user_id', 'ip', 'entry_index']


class CommentRecaptchaForm(CommentForm, Recaptcha.RecaptchaForm):
    pass