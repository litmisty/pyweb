# -*- coding: utf-8 -*-
import os, urllib, random, re
from google.appengine.api import urlfetch
import logging

class ReCaptcha:
    PUBLIC_KEY = ""
    PRIVATE_KEY= ""
    
    @classmethod
    def initialize(cls):
        private_file = os.path.dirname( os.path.dirname(__file__ ) ) + "/private.data"
        f = open( private_file )
        contents = f.readlines()
        f.close()
        for line in contents:
            if line.find("recaptcha_public_key") == 0:
                ReCaptcha.PUBLIC_KEY = line.replace("recaptcha_public_key", "")
                ReCaptcha.PUBLIC_KEY = ReCaptcha.PUBLIC_KEY.replace("\n", "")
            if line.find("recaptcha_private_key") == 0:
                ReCaptcha.PRIVATE_KEY = line.replace("recaptcha_private_key", "")
                ReCaptcha.PRIVATE_KEY = ReCaptcha.PRIVATE_KEY.replace("\n", "")
                
    @classmethod
    def get_public_key(cls):
        if ReCaptcha.PUBLIC_KEY != "":
            return ReCaptcha.PUBLIC_KEY
        
        ReCaptcha.initialize()
        return ReCaptcha.PUBLIC_KEY
    
    @classmethod
    def get_private_key(cls):
        if ReCaptcha.PRIVATE_KEY != "":
            return ReCaptcha.PRIVATE_KEY
        
        ReCaptcha.initialize()
        return ReCaptcha.PRIVATE_KEY
    
    
    def __init__(self, challenge_code=""):
        self.challenge_code = challenge_code
        pass
    
    def generate(self):
        response = urlfetch.fetch( url="http://www.google.com/recaptcha/api/challenge?k=%s&cachestop=%f" % ( ReCaptcha.get_public_key(), random.random() ) )
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
            'privatekey': ReCaptcha.get_private_key(),
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
    