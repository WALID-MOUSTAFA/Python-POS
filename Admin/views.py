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
from .helpers import is_allowed, is_loged_in, is_own_profile
from django.contrib.sessions.models import Session
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.db.models import Q

def index_admin(request):
    
    # from .locale.ar import lang as _
    # return HttpResponse(_["name"])
    return render(request,"index.html");



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

            with open(settings.MEDIA_ROOT + "/" + avatar_name , "wb+") as dest:
                for i in avatar_file.chunks():
                    dest.write(i)

            messages.success(request, _("user created successfully"))
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
        user = old_user
        
        if not  updateAdminForm.is_valid():
            context ["form"] = updateAdminForm
            context["form_error"] = json.loads(updateAdminForm.errors.as_json()) 
            return render(request, "administrators/edit.html", context)

        else:
            username = request.POST["username"]
            
            fullname = request.POST["fullname"]
            
            password = request.POST.get("password") if request.POST.get("password") else None

            email = request.POST["email"]
            
            roles = request.POST.get("roles", None)

            permissions = request.POST.getlist("permissions[]")

            print(f"\n {permissions} \n")
            
            if request.FILES.get("avatar") != None:
                
                avatar_file = request.FILES["avatar"]
                ext = "." + avatar_file.name.split(".")[-1]
                avatar_name = str(uuid.uuid4()) + ext

                old_image = user.avatar
                
                if os.path.exists(settings.MEDIA_ROOT + "/" + old_image):
                    os.remove(settings.MEDIA_ROOT + "/" + old_image)

                with open(settings.MEDIA_ROOT + "/" + avatar_name , "wb+") as dest:
                    for i in avatar_file.chunks():
                        dest.write(i)
                request.session["user_avatar"] = avatar_name
                user.avatar = avatar_name

            user.username = username
            user.fullname = fullname

            if password != None:
                user.password = password

            user.email = email

            ##save previous changes
            user.save()
            
            if roles:
                user.role  = Role.objects.get(name = roles)
                user.save()

            ##ensure if allowed because it's dangerous
            if permissions:
                if is_allowed(request, user.id, "edit_admin"):
                    user.permission.clear()
                    for i in permissions:
                        user.permission.add(Permission.objects.get(id = i))
                        user.save()
            
            ##log user out if a higher moderator edited his profile, keep him if he updated his own porfile
            for s in Session.objects.all():
                if s.get_decoded().get("user_id") == user.id and not is_own_profile(request, user.id):
                    s.delete()


            messages.success(request, _("user updated successfully"))
            return redirect(request.META.get("HTTP_REFERER"))




def detailed_admin(request, id):
    if request.method == "GET":
        
        db_user = Admin.objects.prefetch_related('permission', "role").get(id= id)
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
    per_page = 2
    page = request.GET.get("page", 1)
    
    if request.GET.get("q", None) != None:
        q = request.GET.get("q", "")
        users = Admin.objects.filter(Q (Q(username__contains=q) | Q(email__contains=q) | Q(fullname__contains=q) | Q(role__name__contains=q)))

    else:
        users = Admin.objects.all()

        
    context = {
        "users": Paginator(users, per_page).get_page(page),
    }

    return render(request, "administrators/all.html", context);













        
    




    

    
            
        
        
