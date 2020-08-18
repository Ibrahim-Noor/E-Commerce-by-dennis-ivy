from django import template

register = template.Library()


@register.filter(name="add_place_holder")
def add_place_holder(field, place_holder=None):
    if place_holder == None:
        return field
    else:
        field.field.widget.attrs.update({'placeholder': place_holder})
        return field
