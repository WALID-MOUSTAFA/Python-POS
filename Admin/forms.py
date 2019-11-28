from django import forms
from .models import Client
from django.utils.translation import ugettext_lazy

class CreateAdminForm(forms.Form):


    username = forms.CharField(min_length =3, label = "da")
    fullname = forms.CharField()
    password = forms.CharField()
    confirm_password   = forms.CharField()
    email    = forms.EmailField()
    roles     = forms.CharField(required=False)
    permissions  = forms.CheckboxInput()
    avatar     = forms.FileField()

    def clean(self):
        cleaned_data = super(CreateAdminForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            self.add_error("confirm_password", "password and confirm password fields are not identical")


            
class UpdateAdminForm(CreateAdminForm):
    
    password     = forms.CharField(required = False)
    confirm_password     = forms.CharField(required = False)
    avatar     = forms.FileField(required = False)

    def clean(self):
        cleaned_data = super(CreateAdminForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if password is not None:
            if password != confirm_password:
                self.add_error("confirm_password", "password and confirm password fields are not identical")
                
        
            



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField()

    

class CreateCategoryForm(forms.Form):
    name = forms.CharField(min_length =3)
    desc = forms.CharField()
    desc_image = forms.FileField()
    name_ar = forms.CharField()
    desc_ar = forms.CharField()
        

class UpdateCategoryForm(CreateCategoryForm):
    desc_image = forms.FileField(required = False)
    
    

class CreateProductForm(forms.Form):
    name = forms.CharField(min_length =3)
    desc = forms.CharField()
    name_ar = forms.CharField()
    desc_ar = forms.CharField()
    buy_price = forms.CharField(required = False)
    sell_price = forms.CharField(required = False)
    available_quantity = forms.CharField(required=False)
    category = forms.CharField()
    desc_images = forms.FileField()


class UpdateProductForm(CreateProductForm):
    desc_images = forms.FileField(required = False)

    
class CreateClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ["name", "phone", "address"]
    

class UpdateClientForm(CreateClientForm):
    pass
