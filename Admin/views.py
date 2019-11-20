import os
import uuid
import re
import json
from django.shortcuts import render, redirect
from django.http import HttpRequest, Http404, HttpResponse, JsonResponse
from .models import Admin, Role, Permission
from .forms import CreateAdminForm, UpdateAdminForm, LoginForm
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.core import serializers
from django.db import connection
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from .helpers import is_allowed, is_loged_in


def index_admin(request):
    
    # from .locale.ar import lang as _
    # return HttpResponse(_["name"])
    return render(request,"index.html");




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
                user = Admin.objects.get(username = username, password = password)

                request.session["username"] = user.username

                request.session["user_id"]  = user.id
                
                request.session["user_avatar"]  = user.avatar
                
                user_permission_array = []

                for i in user.permission.all():
                    user_permission_array.append(i.name)

                request.session["permissions"] = user_permission_array
                    
                return redirect("/admin/")
            
            except  ObjectDoesNotExist:
                
                return render(request, "login.html", {"error": "Error, either username or password is wrong, try again! "})
                

            
            
        
def logout_admin(request):
    request.session.flush()
    return redirect("/admin/login")
            




def create_admin(request):

    METHOD = request.method
    context = {
        "create_form": CreateAdminForm,
        "roles"      :  Role.objects.all(),
        "permissions":  Permission.objects.all()
    }    
    
    if METHOD == "GET":
        return render(request, "administrators/create.html", context)
    
    elif METHOD == "POST":
        # print(f"\n {settings.BASE_DIR}\n")
        # return False
        createAdminForm = CreateAdminForm(request.POST, request.FILES)
        upload_url = os.path.join(settings.BASE_DIR, "media")
            
        user = Admin()
        
        if not  createAdminForm.is_valid():
            context["form_error"] = json.loads(createAdminForm.errors.as_json())
            context["form"] = createAdminForm
            return render(request, "administrators/create.html", context)

        else:
            username = request.POST["username"]
            fullname = request.POST["fullname"] 
            password = request.POST["password"]
            email = request.POST["email"]
            roles = request.POST["roles"]
            permissions = request.POST.getlist("permissions[]")
            avatar_file = request.FILES["avatar"]
            ext = "." + avatar_file.name.split(".")[-1]
            avatar_name = str(uuid.uuid4()) + ext
            
            user.username = username
            user.fullname = fullname
            user.password = password
            user.email = email
            user.role  = Role.objects.get(name = roles)
            user.avatar = avatar_name
            user.save()

            for i in permissions:
                user.permission.add(Permission.objects.get(id = i))

            user.save()

            print(upload_url + "/jdksajkdjaskjdkasjkas")
            
            with open(upload_url + "/" + avatar_name , "wb+") as dest:
                for i in avatar_file.chunks():
                    dest.write(i)

            messages.success(request, f"user {user.username} created successfully")
            return redirect("/admin/")



def edit_admin(request, id):
    old_user = Admin.objects.prefetch_related('permission').get(id= id)
    db_user = old_user
    db_roles = Role.objects.all()
    db_permissions = Permission.objects.all()

    if request.method == "GET":
        user_permission_array = []
        for i in db_user.permission.all():
            user_permission_array.append(i.name)

        return render(request, "administrators/edit.html", {
            "user": db_user,
            "roles": db_roles,
            "permissions": db_permissions,
            "user_permission_array": user_permission_array
        })

    elif request.method == "POST":
        user_permission_array = []
        
        for i in db_user.permission.all():
            user_permission_array.append(i.name)

        context = {"user": db_user, "roles": db_roles, "permissions": db_permissions,  "user_permission_array": user_permission_array}
        
        updateAdminForm = UpdateAdminForm(request.POST, request.FILES)
        upload_url = os.path.join(settings.BASE_DIR, "media")    
        user = old_user
        
        if not  updateAdminForm.is_valid():
            
            context["form_error"] = json.loads(updateAdminForm.errors.as_json()) 
            return render(request, "administrators/edit.html", context)

        else:
            username = request.POST["username"]
            
            fullname = request.POST["fullname"]
            
            password = request.POST.get("password") if request.POST.get("password") else None

            email = request.POST["email"]

            roles = request.POST["roles"]

            permissions = request.POST.getlist("permissions[]")

            print(f"\n {permissions} \n")
            
            if request.FILES.get("avatar") != None:
                avatar_file = request.FILES["avatar"]
                ext = "." + avatar_file.name.split(".")[-1]
                avatar_name = str(uuid.uuid4()) + ext
                user.avatar = avatar_name
             
            user.username = username
            user.fullname = fullname

            if password != None:
                user.password = password

            user.email = email
            user.role  = Role.objects.get(name = roles)
           
            user.save()

            user.permission.clear()
            for i in permissions:
                user.permission.add(Permission.objects.get(id = i))
                print(f"\n {i}\n")
            user.save()


            if request.FILES.get("avatar"):
                with open(upload_url + "/" + avatar_name , "wb+") as dest:
                    for i in avatar_file.chunks():
                        dest.write(i)

            messages.success(request, f"user {user.username} updated successfully")
            return redirect("/admin/all")




def detailed_admin(request, id):
    if request.method == "GET":
        
        db_user = Admin.objects.prefetch_related('permission').get(id= id)
        return render(request, "administrators/detailed_user.html", {"user": db_user} )
  




      
def delete_admin(request, id):
    
    context = {}
    if request.method == "POST":
        
        user = Admin.objects.get(id = id)
        if user.delete():
            return JsonResponse({"success": True , "message": "product has been deleted successfully"})

        else:
            return JsonResponse({"success": False , "message": "can't delete this product"})
    else:
        return JsonResponse({"error": "wrong method"})


    
        
def all_admins(request):
    users = list(Admin.objects.all().values("id","username", "fullname", "email", "avatar"))
    
    context = {
        "users": users,
    }
    return render(request, "administrators/all.html", context);













        
    




    

    
            
        
        
