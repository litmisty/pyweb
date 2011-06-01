# -*- coding: utf-8 -*-
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
    
    
