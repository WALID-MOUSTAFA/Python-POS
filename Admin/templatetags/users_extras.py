from .. import helpers
from django import template

register = template.Library()

@register.simple_tag(takes_context = True)
def user_allowed(context, *args, **kwargs):
    request = context["request"]
    return helpers.is_allowed(request, request.session["user_id"], *args)

@register.simple_tag(takes_context = True)
def is_own_profile(context, *args, **kwargs):
    request = context["request"]
    return helpers.is_own_profile(request, args[0])
    
