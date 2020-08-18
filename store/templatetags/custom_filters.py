from django import template

register = template.Library()

@register.filter(name="add_currency_sign")
def add_currency_sign(value):
    return str(value)+' Rs.'