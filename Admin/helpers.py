from .models import Admin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect


def is_allowed(request, user_id, *args):

    try:
        
        user_permission_array  = request.session["user_permissions"] 
    

        for i in args:   

            if not i in user_permission_array:
                
                return False

            return True
            
    except ObjectDoesNotExist:

        print(f"\nuser not found\n")
        return redirect("/admin/")


def is_own_profile(request, id):
    if request.session.get("user_id") == int(id):
        return True
    return False
        


    
def is_loged_in(request):
    if request.session.get("username"):
        return True
    return False
        
            

            
