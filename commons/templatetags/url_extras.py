from django.template import Library

register = Library()

@register.simple_tag(takes_context=True)
def url_paginate(context, *args, **kwargs):
    request = context["request"]
    queryparams = f"?page={kwargs.get('page')}"
    for i in args:
        if request.GET.get(i, None) != None:
            val = request.GET.get(i)
            queryparams+=f"&{i}={val}"
    return queryparams
