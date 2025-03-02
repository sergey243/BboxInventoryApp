from django import template

register = template.Library()

@register.filter(name="active")
def active(value, arg):
    return arg in value