from .models import Admin
from django.core.exceptions import ObjectDoesNotExist

class CustomAuthBackend:

    def authenticate(self,request, username=None, password=None):
        try:            
            user = Admin.objects.prefetch_related("permission").get(username=username, password=password)
            return user;
        
        except ObjectDoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Admin.objects.prefetch_related("permission").get(pk=user_id)
        except ObjectDoesNotExist:
            return None


