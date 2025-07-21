from django import template

register = template.Library() 

@register.filter(name='ComoJson') 
def ComoJson(Grupos):
    return list(Grupos.values_list('name', flat=True))
