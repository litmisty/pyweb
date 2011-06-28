# -*- coding: utf-8 -*-
# pyweb-ko
# bbcode.py
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
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.from google.appengine.ext import webapp 
import re
register = webapp.template.create_template_register()

def addUrlPrefix(matchobj):    
    if matchobj.group(1).find("http") != 0:
        url = "http://" + matchobj.group(1)
    else:
        url = matchobj.group(1)
        
    return '<a href="%s">%s</a>' % ( url, matchobj.group(2) )

def addImagePrefix(matchobj):    
    if matchobj.group(1).find("http") != 0:
        url = "http://" + matchobj.group(1)
    else:
        url = matchobj.group(1)
        
    return '<img src="%s" />' % ( url )

def bbcode(value):
    single_tags = {'p':'p','br':'br /','i':'em','strong':'strong','b':'strong','blockquote':'blockquote','h3':'h3','h4':'h4','h5':'h5','h6':'h6'}
    
    value = value.replace("<", "&lt;")
    value = value.replace(">", "&gt;")
    
    value = value.replace("\n", "<br />")
    
    p = re.compile("\[code.*?\](.*?)\[\/code\]+", re.S)
    result = p.findall( value )
    for c in result:
        nc = c.replace("<br />", "\n");
        value = value.replace( c, nc )
    
    for bbcode, html in single_tags.items():    
        value = value.replace("[%s]"%bbcode, "<%s>"%html)
        value = value.replace("[/%s]"%bbcode, "</%s>"%html)
        
    value = re.sub( '\[img.*?\](.*?)\[\/img\]', addImagePrefix, value )
    
    value = re.sub( '\[url=(.*?)\](.*?)\[\/url\]', addUrlPrefix, value )
    
    p = re.compile( '\[code.*?class=(.*?)\](.*?)\[\/code\]', re.DOTALL )
    value = p.sub( '<pre class="brush: \\1;">\\2</pre>', value )
    
    return value

register.filter(bbcode)
