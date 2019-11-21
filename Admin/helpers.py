from .models import Admin
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect

def is_allowed(user_id, *args):

    try:
        user = Admin.objects.prefetch_related("permission").get(id = user_id)

        user_permission_array  = []
    
        for i in user.permission.all():

            user_permission_array.append(i.name)
        
        for i in args:   

            if not i in user_permission_array:
                
                return False

            return True
            
    except ObjectDoesNotExist:

        print(f"\nuser not found\n")
        return redirect("/admin/")


    
def is_loged_in(request):
    if request.session.get("username"):
        return True
    return False
        
            

            
