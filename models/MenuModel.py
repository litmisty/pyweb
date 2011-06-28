# -*- coding: utf-8 -*-
# pyweb-ko
# MenuModel.py
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
import logging 
class Menu:
    MENU_FREE = 1
    MENU_NEWS = 2
    MENU_TIPS = 3
    MENU_QNA = 4
    
    labels = { MENU_FREE:"자유게시판",
              MENU_NEWS:"새소식",
              MENU_TIPS:"강좌,팁",
              MENU_QNA:"질문,답변" }
    
    identifiers = { MENU_FREE:"free",
              MENU_NEWS:"news",
              MENU_TIPS:"tips",
              MENU_QNA:"qna" }

    @classmethod
    def getLabel( cls, menu_id ):
        if cls.labels.has_key( menu_id ):
            return cls.labels[menu_id]
        return ''
        
    @classmethod
    def getMenuDictionary(cls):
        return cls.labels

    @classmethod
    def getMenuIdentifierDictionary(cls):
        return cls.identifiers
    
    @classmethod
    def getMenuIdList(cls):
        return cls.labels.keys()
    
    @classmethod
    def getMenuIdentifier(cls, menu_id):
        if cls.identifiers.has_key( menu_id ):
            return cls.identifiers[menu_id]
        
    @classmethod
    def isRightIdentifier(cls, identifier):
        for menu_id, menu_identifier in cls.identifiers.items():
            if menu_identifier == identifier:
                return True            
        return False
    
    @classmethod
    def getMenuIdWithIdentifier(cls, identifier):
        for menu_id, menu_identifier in cls.identifiers.items():
            if menu_identifier == identifier:
                return menu_id            
        return None
    
    
