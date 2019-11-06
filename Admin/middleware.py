from django.shortcuts import redirect, render
from .helpers import is_loged_in, is_allowed



class CheckAuth:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)
    
    def process_view(self, request, view_func, view_args, view_kwargs):

        if view_func.__name__.endswith("admin") or view_func.__name__.endswith("admins"):
            if not  is_loged_in(request):
                return redirect("/admins/login")
            
        if view_func.__name__ == "edit_admin":            
            if not is_allowed(request.session.get("user_id"), "edit_admin") :
                return render(request, "403.html", {}, status = 403)
            
        if view_func.__name__ == "delete_admin":
            if not is_allowed(request.session.get("user_id"), "delete_admin") :
                return render(request, "403.html", {}, status = 403)
            
                
        if view_func.__name__ == "create_admin":
            if not is_allowed(request.session.get("user_id"), "create_admin") :
                return render(request, "403.html", {}, status = 403)
            

        if view_func.__name__ == "all_admins":
            if not is_allowed(request.session.get("user_id"), "show_admin") :
                 return render(request, "403.html", {}, status = 403)
