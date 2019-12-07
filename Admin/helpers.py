from .models import Admin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect


def is_allowed(request, user_id, *args):
    print(args)
    try:
        user_permissions = request.user.permission.all()
        user_permission_array  = [p.name for p in user_permissions]
        
        for i in args:   

            if not i.strip() in user_permission_array:
                
                return False

            return True
            
    except ObjectDoesNotExist:

        
        return redirect("/admin/")


def is_own_profile(request, id):
    if request.user.id == int(id):
        return True
    return False
        


    
def is_loged_in(request):
    if request.user.is_authenticated:
        return True
    return False
        
            

            
