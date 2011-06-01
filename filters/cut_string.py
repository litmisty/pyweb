from google.appengine.ext import webapp

register = webapp.template.create_template_register()

def cut_string(value, max_length):
    if len(value) <= max_length:  
        return value  
  
    truncd_val = value[:max_length]  
    if value[max_length] != " ":  
        rightmost_space = truncd_val.rfind(" ")  
        if rightmost_space != -1:  
            truncd_val = truncd_val[:rightmost_space]  
    
    return truncd_val + "..."
    
register.filter(cut_string)
