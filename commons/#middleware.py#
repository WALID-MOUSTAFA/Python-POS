from django.shortcuts import redirect, render
from django.utils import translation



class Global:
    def __init__(self, get_response):
        self.get_response = get_response

        

    def __call__(self, request):
        return self.get_response(request)



