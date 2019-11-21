from django.shortcuts import render, redirect
from django.utils import translation

# Create your views here.

def change_lang(request, LANG):

    request.session[translation.LANGUAGE_SESSION_KEY] = LANG

    translation.activate(LANG)

    
    if request.session.get("user_id"): #logged in
        return redirect("/" + LANG + "/admin/all") 
    else:
        redirect("/")
