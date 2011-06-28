# pyweb-ko
# Handler.py
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users

class Handler(webapp.RequestHandler):
    context = {}
        
    def render(self, filename):
#        if self.request.host_url.find("http://m.") != -1 :
#            path = os.path.join( os.path.dirname(__file__), '../template/mobile/%s' % filename )
#        else:
        
        if users.get_current_user():
            self.context['auth_url'] = users.create_logout_url("/")
        else :
            self.context['auth_url'] = users.create_login_url(self.request.uri)
        
        self.context['layout'] = "layout.html"
        
        if self.request.user_agent.find("MSIE 6") != -1:
            self.context['layout'] = "layout_ie6.html"
        
        path = os.path.join( os.path.dirname(__file__), '../template/%s' % filename )
        self.response.out.write( template.render( path, self.context ) )

    def siteError(self, msg):
        self.response.clear()
        self.response.set_status(500)
        self.context['error_msg'] = msg
        self.render( "error.html" )
                