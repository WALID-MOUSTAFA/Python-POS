from django.shortcuts import render, redirect
from .helpers import is_loged_in
from .forms import LoginForm
from django.core.exceptions import ObjectDoesNotExist
from .models import Admin
from django.contrib.auth import login, logout,authenticate, load_backend
import json

def login_admin(request):
    
    if request.method == "GET":
        if is_loged_in(request):
            return redirect("/admin/")
        else:
            return render(request, "login.html")

 
    elif request.method == "POST":
        
        login_form = LoginForm(request.POST)

        
        
        if not login_form.is_valid():

            context = {"form_error": json.loads(login_form.errors.as_json())}
            return render(request, "login.html",context)
        
        else:
            
            username = login_form.cleaned_data.get("username")
            password = login_form.cleaned_data.get("password")

            user = authenticate(username=username, password=password)
            print(f"\n\nresult\n{user}")

            if user != None:
                login(request,user)
                return redirect('/admin/')
            else:
                return render(request, "login.html", {"error": "Error, either username or password is wrong, try again! "})

            

      
        
        

            
            
        
def logout_admin(request):
    # request.session.flush()
    logout(request)
    return redirect("/admin/login")
