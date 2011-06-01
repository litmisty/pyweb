from google.appengine.ext import webapp 
register = webapp.template.create_template_register()

from models.MenuModel import Menu

def menu_label(value):
    label = Menu.getLabel( value )
    return label

register.filter(menu_label)
