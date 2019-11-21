from .. import helpers
from django import template

register = template.Library()

@register.simple_tag(takes_context = True)
def user_allowed(context, *args, **kwargs):
    request = context["request"]
    return helpers.is_allowed(request.session["user_id"], *args)
    
    
