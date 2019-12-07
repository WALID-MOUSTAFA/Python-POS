from django.shortcuts import redirect, render
from .helpers import is_loged_in, is_allowed
from django.utils.translation import get_language 
from pprint import pprint
from django.contrib.auth import load_backend, logout
import logging

class CheckAuth:

    def __init__(self, get_response):
        self.get_response = get_response
        

    def __call__(self, request):
        load_backend("Admin.CustomAuthBackend.CustomAuthBackend")

        
        if not request.user.is_authenticated and request.path.find("admin/login") == -1:
            return redirect("/en/admin/login/")
        else:
            return self.get_response(request)

        return self.get_response(request)

 
        
