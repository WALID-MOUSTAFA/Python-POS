from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateClientForm, UpdateClientForm
from .models import Client
import json
import os
import uuid
from django.conf import settings
from django.utils.translation import gettext as _
from django.core.paginator import Paginator
from django.db.models import Q

def index_client(request):
    per_page = 4
    page = request.GET.get("page", 1)

    if request.GET.get("q", None) != None:
        q = request.GET.get("q", "")
        clients = Client.objects.filter(Q (Q(name__contains=q) | Q(address__contains=q) | Q(phone__contains=q)))

    else:
        clients = Client.objects.all()

    
    context = {
        "title": "clients",
        "clients" : Paginator(clients, per_page).get_page(page)
    }


    return render(request, "clients/all.html",context)



def create_client(request):
    context = {"title": "Create client"}
    if request.method == "GET":
        return render(request, "clients/create.html",context)

    elif request.method == "POST":

        # upload_url = os.path.join(settings.BASE_DIR, "media")
        
        create_client_form = CreateClientForm(request.POST) 

        if not create_client_form.is_valid():

            # context["form_error"] = json.loads(create_categorg_form.errors.as_json())

            context["form"] = create_client_form

            return render(request, "clients/create.html", context)

        else:
            
            client = Client()
        
            client.name = create_client_form.cleaned_data["name"]
            client.address = create_client_form.cleaned_data["address"]
            client.phone = create_client_form.cleaned_data["phone"]
            client.save()
                
            messages.success(request, _("client added successfully"))
            return redirect("/admin/client/")
    


def edit_client(request, id):
    
    client = Client.objects.get(id = id)

    context = {}

    context["client"]   = client


    
    if request.method == "GET":
        return render(request, "clients/edit.html",context)

    elif request.method == "POST":
        update_client_form = UpdateClientForm(request.POST)
        
        if not update_client_form.is_valid():

            # context["form_error"] = json.loads(update_client_form.errors.as_json())
            context["form"] = update_client_form
            return render(request, "clients/edit.html",context)

        else:
 
            client.name = update_client_form.cleaned_data["name"]
            client.phone = update_client_form.cleaned_data["phone"]
            client.address = update_client_form.cleaned_data["address"]
            client.save()
                        
                        
            messages.success(request, _("client has been edited successfully"))
            return redirect("/admin/client/all")

            



def detailed_client(request, id):
    context = {}
    
    client = Client.objects.get(id = id)
   
    context = {
        "client": client,
    }

    if request.method == "GET":
        return render(request, "clients/detailed_client.html", context)

    

def delete_client(request, id):
    context = {}

    if request.method == "POST":
        
        client = Client.objects.get(id = id)

        if client.delete():
            return JsonResponse({"success": True , "message": _("client has been deleted successfully")})
        else:           
            return JsonResponse({"success": False , "message": _("can't delete this client ")})
    else:
        return JsonResponse({"error": "wrong method"})
