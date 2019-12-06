from django import template

register = template.Library()

@register.filter
def endswith(value, arg):
    return value.endswith(arg)


@register.filter
def to_int(value):
    return int(value)
