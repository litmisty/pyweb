# -*- coding: utf-8 -*-
import datetime
import logging
from google.appengine.ext import db
from google.appengine.ext.db import Key

from django import forms
from google.appengine.ext.db import djangoforms

from UserModel import User

from forms import Recaptcha

from ErrorMessage import *
from Paging import PagingCursorMasterKey


class EntryIndex(db.Model):
    max_index = db.IntegerProperty(required=True, default=0)
    
    @classmethod
    def get_max_index(cls):
        index = cls.get_by_key_name('index')
        if index is None:
            index = cls(key_name='index')
        
        new_index = index.max_index + 1
        return new_index
    
    @classmethod
    def set_max_index(cls, new_index):
        index = cls.get_by_key_name('index')
        if index is None:
            index = cls(key_name='index')
        
        index.max_index = new_index
        index.put()

class Entry(db.Model):
    menu_id = db.IntegerProperty()
    index = db.IntegerProperty()
    title = db.StringProperty(required=True)    
    content = db.TextProperty(required=True)
    link = db.StringProperty()
    user = db.UserProperty()
    site_user_id = db.IntegerProperty()
    comment_count = db.IntegerProperty()
    is_removed = db.BooleanProperty( default=False )
    ip = db.StringProperty()
    created_on = db.DateTimeProperty()
    updated_on = db.DateTimeProperty()
    
    
    
    @classmethod
    def insert(cls, title, link, content, menu_id, user, remote_addr ):
        def txn():
            entry_index = EntryIndex.get_by_key_name('entry')
            if entry_index is None:
                entry_index = EntryIndex(key_name='entry')
            new_index = entry_index.max_index
            entry_index.max_index += 1
            entry_index.put()
            
            
            new_entry = Entry(key_name = 'entry'+str(new_index),
                          parent = entry_index, 
                          index = new_index,
                          title = title,
                          content = content,
                          menu_id = menu_id,
                          user = user,
                          comment_count = 0,
                          ip = remote_addr,
                          link=link,
                          created_on=datetime.datetime.now(),
                          updated_on=datetime.datetime.now())
            new_entry.put()
                        
            return new_entry
        
        if link != "" and link.find("http") == -1 :
            link = "http://" + link

        new_entry = db.run_in_transaction(txn)
        
        site_user_id = User.getSiteUserId(user)
        new_entry.site_user_id = site_user_id
        new_entry.put()
        
        PagingCursorMasterKey.clearModelKey("Entry")
        
        
        return new_entry
    
    @classmethod
    def delete_entry(cls, index):
        entry = cls.get_entry(index)
        if not entry:
            return
        entry.is_removed = True
        entry.put()
        PagingCursorMasterKey.clearModelKey("Entry")
        
    @classmethod
    def get_max_index(cls):
        if EntryIndex.get_by_key_name('entry') is not None:
            return EntryIndex.get_by_key_name('entry').max_index
        else:
            return 1
    
    @classmethod
    def get_entry(cls, index):
        key_name = "entry"+index
        return cls.get_by_key_name(key_name, parent=Key.from_path('EntryIndex', 'entry'))
    
    @classmethod
    def delete_with_user_id(cls, site_user_id):
        query = Entry.all()
        query.filter("site_user_id", site_user_id)
        query.filter("is_removed", False)
        entries = query.fetch(500, 0)
        
        while entries:
            for entry in entries:
                entry.is_removed = True
                entry.put()        
                
            query.with_cursor( query.cursor() )
            entries = query.fetch(500, 0 )
            
        PagingCursorMasterKey.clearModelKey("Entry")
            
        
    
    
class EntryForm(djangoforms.ModelForm):    
    link_error_messages={'invalid': (u'')}
    
    title = forms.CharField(max_length=100, required=True, label="제목", widget=forms.TextInput({'class':'editor_text'}), error_messages=getFormErrorMessage() )
    link = forms.URLField(required=False, label="링크",  widget=forms.TextInput({'class':'editor_text'}), error_messages=getFormErrorMessage('url') )
    content = forms.CharField(required=True, label="내용", widget=forms.Textarea({'rows':10, 'cols':50, 'class':'editor write_form'}), error_messages=getFormErrorMessage())
    
    class Meta:
        model = Entry
        exclude = ['updated_on', 'created_on', 'user', 'site_user_id','menu_id', 'index', 'comment_count', 'ip' ,'is_removed']
        
        
class EntryRecaptchaForm(EntryForm, Recaptcha.RecaptchaForm):
    pass