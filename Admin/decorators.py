from .helpers import is_allowed as is_al
from django.shortcuts import redirect
    


def is_allowed(permission):
    def decorator_mask(function):
        def function_mask(*args, **kwargs):
            request=args[0]
            if is_al(request, request.user.id, permission):
                return function(*args, **kwargs)
            else:
                return redirect("/admin/error403")
        return function_mask
    return decorator_mask
