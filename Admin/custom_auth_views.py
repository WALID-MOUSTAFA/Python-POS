from django.shortcuts import render, redirect
from .helpers import is_loged_in
from .forms import LoginForm
from django.core.exceptions import ObjectDoesNotExist
from .models import Admin

def login_admin(request):
    
    if request.method == "GET":
        if is_loged_in(request):
            return redirect("/admin/")
        else:
            return render(request, "login.html")

 
    elif request.method == "POST":
        
        login_form = LoginForm(request.POST)

        print("\n \n dsadas \n\n")
        
        if not login_form.is_valid():

            context = {"form_error": json.loads(login_form.errors.as_json())}
            return render(request, "login.html",context)
        
        else:
            
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")

            try:
                user = Admin.objects.prefetch_related("permission").get(username = username, password = password)

                request.session["username"] = user.username

                request.session["user_id"]  = user.id
                
                request.session["user_avatar"]  = user.avatar

                user_permission_array = [p.name for p in user.permission.all()]
                request.session["user_permissions"] = user_permission_array
                    
                return redirect("/admin/")
            
            except  ObjectDoesNotExist:
                
                return render(request, "login.html", {"error": "Error, either username or password is wrong, try again! "})
                

            
            
        
def logout_admin(request):
    request.session.flush()
    return redirect("/admin/login")
