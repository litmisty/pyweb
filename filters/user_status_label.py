from google.appengine.ext import webapp 
register = webapp.template.create_template_register()

from models.UserModel import UserStatus

def user_status_label(value):
    label = UserStatus.getStatusLabel(value)
    return label

register.filter(user_status_label)
