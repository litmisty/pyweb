# -*- coding: utf-8 -*-

field_error_message = {
    'required': (u'입력 해 주세요. 필수 항목 입니다.'),                       
    'invalid': (u'올바른 값을 입력하세요')
}


email_error_message = {
    'invalid': (u'올바른 Email을 입력하세요')
}

url_error_message = {
    'invalid': (u'올바른 URL을 입력하세요'),
    'invalid_link': (u'해당 URL에 접속할 수 없습니다.'),
}


choice_error_message = {
    'invalid_choice': (u'올바른 값을 선택 해 주세요. %(value)는 올바른 선택이 아닙니다.'),
}


multiple_choice_error_message = {
    'invalid_choice': (u'올바른 값을 선택 해 주세요. %(value)는 올바른 선택이 아닙니다.'),
    'invalid_list': (u'값을 선택 해 주세요.'),
}

def getFormErrorMessage( type=None ):
    valid_type = {
        'email' : dict( field_error_message, **email_error_message ),
        'url' : dict( field_error_message, **url_error_message ),
        'choice' : dict( field_error_message, **choice_error_message ),
        'multiple_choice' : dict( field_error_message, **multiple_choice_error_message ),
    }
    
    if valid_type.has_key( type ):
        return valid_type[ type ]
    else:
        return field_error_message
    
    
def getSiteErrorMessage( type=None ):
    errorList = [
        SiteErrorType.ERROR_MENU_NOT_EXIST,
        SiteErrorType.ERROR_ENTRY_NOT_EXIST,
        SiteErrorType.ERROR_COMMENT_NOT_EXIST,
        SiteErrorType.ERROR_USER_BANNED,
        SiteErrorType.ERROR_INVALID_ACCESS
    ]
    
    if errorList.count( type ) > 0 :
        return type
    else:
        return SiteErrorType.ERROR


class SiteErrorType:
    ERROR                       = "처리할 수 없는 에러가 발생했습니다."
    ERROR_MENU_NOT_EXIST        = "잘못된 게시판 입니다."
    ERROR_ENTRY_NOT_EXIST       = "게시글이 존재하지 않습니다."
    ERROR_COMMENT_NOT_EXIST     = "코멘트가 존재하지 않습니다."
    ERROR_USER_BANNED           = "접근이 재한되었습니다."
    ERROR_INVALID_ACCESS        = "잘못된 접근입니다."
    
    
    
    
    