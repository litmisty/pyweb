# -*- coding: utf-8 -*-
# pyweb-ko
# Paging.py
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
from google.appengine.api import memcache

class PagingCursorMasterKey:
    master_key = "paging_cursor_master_key"
            
    @classmethod
    def appendToMasterKey(cls, key):
        keyList = memcache.Client().get( cls.master_key )
        if not keyList:
            keyList = []
        
        try:
            keyList.index( key )
        except:            
            keyList.append(key)
            memcache.Client().set( cls.master_key, keyList )            
            
    @classmethod
    def setMasterKeyList(cls, keyList):
        memcache.Client().set( cls.master_key, keyList )
            
    @classmethod
    def remoteFromMasterKey(cls, key):
        keyList = memcache.Client().get( cls.master_key )
        if not keyList:
            return 
        
        try:
            keyList.remove( key )
            cls.setMasterKeyList( keyList )
        except:            
            return
        
        
    @classmethod
    def isKeyExist(cls, key):
        keyList = memcache.Client().get( cls.master_key )
        
        if not keyList:
            return False
        
        try:
            keyList.index( key )
            return True
        except:
            return False
    
    @classmethod
    def isValueExist(cls, key):
        if not cls.isKeyExist(key):
            return False
        
        return memcache.Client().get( key )
    
    @classmethod
    def setValue(cls, key, value):
        cls.appendToMasterKey( key )
        memcache.Client().set( key , value )
    
    @classmethod
    def getValue(cls, key):
        if not cls.isKeyExist(key):
            return None
                
        return memcache.Client().get( key )
        
    
    @classmethod
    def deleteValue(cls, key):
        if not cls.isKeyExist(key):
            return None
        
        memcache.Client().delete( key )
        cls.remoteFromMasterKey( key )
        
    @classmethod
    def clearModelKey(cls, model_name):
        if not model_name:
            return
        keyList = cls.getAllKey()
        if not keyList:
            return
        
        for key in keyList:
            if key.find( "cursor::model=%s::"%model_name ) != -1:
                cls.deleteValue(key)
    
    @classmethod
    def clearModelAndQueryKey(cls, model_name, query):
        if not model_name:
            return
        if not query:
            return
        
        keyList = cls.getAllKey()
        if not keyList:
            return
        
        for key in keyList:
            if key.find( "cursor::model=%s::"%model_name ) != -1:
                if key.find(query) != -1:
                    cls.deleteValue(key)
    
    @classmethod
    def getAllKey(cls):
        return memcache.Client().get(cls.master_key)        
        
    
    @classmethod
    def clearAllKey(cls):
        keyList = cls.getAllKey()
        if not keyList:
            return
        
        for key in keyList:
            cls.deleteValue(key)
        
        memcache.Client().delete(cls.master_key)


class PagingCursor:    
    @classmethod
    def getPagingCursorKey(cls, query, limit):
        return "cursor::model=%s::filter=%s::order=%s::limit=%d" %(
           query._model_class.__name__,
           ",".join(["%s:%s"%(key,value) for key, value in query._Query__query_sets[0].items()]),
           ",".join(["%s:%d"%(key,value) for key, value in query._Query__orderings]),
           limit
        )
    
    @classmethod
    def getCursorList(cls, key):
        return PagingCursorMasterKey.getValue( key )
    
    @classmethod
    def clearCursorList(cls, key):
        PagingCursorMasterKey.deleteValue(key)
        
    @classmethod
    def appendCursor(cls, key, cursor):
        cursorList = cls.getCursorList(key)

        if not cursorList:
            cursorList = []
        
        try:
            cursorList.index( cursor )
        except:
            cursorList.append( cursor )
            PagingCursorMasterKey.setValue(key, cursorList)
    
    @classmethod
    def hasNextCursor(cls, key, cursor):
        cursorList = cls.getCursorList(key)
        if not cursorList:
            return False
        try:
            cursorIndex = cursorList.index( cursor )
            if len(cursorList) > cursorIndex+1:
                return True
            else:
                return False
        except:
            return False
        
    @classmethod
    def getNextCursor(cls, key, cursor):
        if not cls.hasNextCursor(key, cursor):
            return None
        
        cursorList = cls.getCursorList(key)
        cursorIndex = cursorList.index( cursor )
        return cursorList[cursorIndex+1]
    
    
    @classmethod
    def hasPrevCursor(cls, key, cursor):
        if not cursor:
            return False
        
        cursorList = cls.getCursorList(key)
        if not cursorList:
            return False
        
        
        try:
            cursorIndex = cursorList.index( cursor )
            if cursorIndex >= 0:
                return True
            else:
                return False
        except:
            return False
        
    @classmethod
    def getPrevCursor(cls, key, cursor):
        if not cls.hasPrevCursor(key, cursor):
            return None
        
        cursorList = cls.getCursorList(key)
        cursorIndex = cursorList.index( cursor )
        if cursorIndex is 0:
            return None
        return cursorList[cursorIndex-1]


        
class Paging():
    def __init__(self, query):
        self.limit = 10        
        self.query = query        
        self.result = []        
        
        self.cursor = None
        self.olderCursor = None
        self.newerCursor = None
        
        self._hasOlderCursor = False
        self._hasNewerCursor = False
           
    def setLimit(self, limit):
        self.limit = limit
    
    def getLimit(self):
        return self.limit
    
    def setCurrentCursor(self, cursor):
        self.cursor = cursor

    def getCurrentCursor(self):
        return self.cursor
        
    def getOlderCursor(self):
        if self.olderCursor is None:
            return ''
        return self.olderCursor

    def getNewerCursor(self):
        if self.newerCursor is None:
            return ''
        return self.newerCursor
    
    def hasOlderCursor(self):
        return self._hasOlderCursor

    def hasNewerCursor(self):
        return self._hasNewerCursor
    
    
    def execute(self):
        cursor_key = PagingCursor.getPagingCursorKey( self.query, self.limit )
        
        #get current page's result
        try:
            self.query.with_cursor( self.cursor )
            self.result = self.query.fetch(limit=self.limit, offset=0)
            
            if len( self.result ) > 0:
                # get newer cursor 
                self._hasNewerCursor = PagingCursor.hasPrevCursor( cursor_key, self.cursor )
                if self._hasNewerCursor:
                    self.newerCursor = PagingCursor.getPrevCursor( cursor_key, self.cursor )
                
                # get older cursor
                self._hasOlderCursor = PagingCursor.hasNextCursor( cursor_key, self.cursor )
                if self._hasOlderCursor:
                    self.olderCursor = PagingCursor.getNextCursor( cursor_key, self.cursor )
                else:
                    try:
                        older_cursor = self.query.cursor()
                        self.query.with_cursor( older_cursor )
                        older_result = self.query.fetch(limit=self.limit, offset=0)
                        if len( older_result ) > 0:
                            self._hasOlderCursor = True
                            self.olderCursor = older_cursor
                            PagingCursor.appendCursor( cursor_key, self.olderCursor )
                    except:
                        pass
                        
        except:
            return
                
    def getResult(self):
        return self.result
    
