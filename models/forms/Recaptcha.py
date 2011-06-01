# -*- coding: utf-8 -*-
import urllib, random, re

from django import forms
from django.conf import settings
from django.utils.safestring import mark_safe

from google.appengine.api import urlfetch
from google.appengine.ext.db import djangoforms

class RecaptchaWidget(forms.Widget):
    def render(self, name, value, attrs=None):
        captcha = ReCaptcha()
        captcha.generate()
        return mark_safe( u"""<img src="%s" alt="captcha_image"/><input type="text" id="id_%s" name="%s" value="" /><input type="hidden" name="challenge_code" value="%s" />""" 
                          %( captcha.get_image_url(), name, name, captcha.get_challenge_code()  ) )
    
    def value_from_datadict(self, data, files, name):
        challenge = data.get(name)
        challenge_code = data.get('challenge_code')
        return (challenge_code, challenge)
    
class RecaptchaField(forms.Field):
    widget = RecaptchaWidget
    default_error_messages = {
        'required': (u'스팸 방지 문자열을 입력 해 주세요.'),
        'invalid': (u'잘못된 문자열 입니다.'),
        'invalid_remote_addr': (u'잘못된 접근입니다.'),
        'invalid_challenge_code': (u'Captcha서비스에 에러가 발생했습니다.'),
    }
    
    def __init__(self, *args, **kwargs):
        self.remote_addr = None
        super(RecaptchaField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not self.remote_addr:
            raise forms.ValidationError(self.default_error_messages['invalid_remote_addr'])
        
        value = super(RecaptchaField, self).clean(value)
        challenge_code, challenge_value = value
        
        if not challenge_code:
            raise forms.ValidationError(self.default_error_messages['invalid_challenge_code'])
        if not challenge_value:
            raise forms.ValidationError(self.default_error_messages['required'])
        
        recaptcha = ReCaptcha( challenge_code )
        if recaptcha.check( challenge_value, self.remote_addr):
            return value
        else:
            raise forms.ValidationError(self.default_error_messages['invalid'])
    
class RecaptchaForm(djangoforms.ModelForm):
    captcha = RecaptchaField(label="스팸 방지")
    
    def __init__(self, remote_addr, *args, **kwargs):
        super(RecaptchaForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field, RecaptchaField):
                field.remote_addr = remote_addr
        
    

class ReCaptcha:
    def __init__(self, challenge_code=""):
        self.challenge_code = challenge_code
        pass
    
    def generate(self):
        response = urlfetch.fetch( url="http://www.google.com/recaptcha/api/challenge?k=%s&cachestop=%f" % ( settings.RECAPTCHA_PUBLICKEY, random.random() ) )
        if response.status_code == 200:
            return_values = response.content.splitlines();
            p = re.match(".*challenge.*'(.*)'", return_values[3] )
            self.challenge_code = p.group(1)
        else:
            return False
        pass
    
    def get_image_url(self):
        return "http://www.google.com/recaptcha/api/image?c=%s" % self.challenge_code 
    
    def get_challenge_code(self):
        return self.challenge_code
    
    def check(self, answer, remote_addr):
        if not answer or answer=="" or not remote_addr or remote_addr== "":
            return False
        
        headers = {
                   'Content-type':  'application/x-www-form-urlencoded'
        }
        
        params = urllib.urlencode ({
            'privatekey': settings.RECAPTCHA_PRIVATEKEY,
            'remoteip' : remote_addr,
            'challenge': self.challenge_code,
            'response' : answer,
        })
        
        response = urlfetch.fetch(
            url      = "http://www.google.com/recaptcha/api/verify",
            payload  = params,
            method   = urlfetch.POST,
            headers  = headers
        )     
        
        if response.status_code == 200:
            return_values = response.content.splitlines();
            return_code = return_values[0]
            if return_code == "true":
                return True
            else:
                return False
            return True
        else:
            return False
        
        
        
        
        