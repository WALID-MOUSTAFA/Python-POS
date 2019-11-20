import os
import json
from django.http import JsonResponse, HttpResponseServerError
from django.shortcuts import render, HttpResponse, redirect
from django.utils.translation import gettext as _
from .models import Category_translation, Product_translation, Product, Product_images
from .forms import CreateProductForm, UpdateProductForm
from django.conf import settings
from django.contrib import messages

#---------------------------------------------------------------------------------------#



def index_product(request):
    products_en =  Product_translation.objects.filter(language = "en")
    products_ar =  Product_translation.objects.filter(language = "ar")
    products    = Product.objects.all()
    images      = Product_images.objects.all()
    context = {
        "products": products,
        "products_en": products_en,
        "products_ar" : products_ar,
        "images"     : images
    }
    return render(request, "products/all.html", context)


def create_product(request):
    context = {
        "title": _("Add product"),
        "categories": Category_translation.objects.all()
    }
    

    if request.method == "GET":
        return render(request, "products/create.html", context)
    
    elif request.method == "POST":

        create_product_form = CreateProductForm(request.POST, request.FILES)

        if not create_product_form.is_valid():

            context["form"] = create_product_form
            
            return render(request, "products/create.html", context)
        
        else:
      
            product = Product()
            product.category = Category_translation.objects.get(name = request.POST["category"]).Category
            product.sell_price = request.POST["sell_price"]
            product.save()

            product_trans_ar = Product_translation()
            product_trans_ar.name = request.POST["name_ar"]
            product_trans_ar.desc = request.POST["desc_ar"]
            product_trans_ar.language = "ar"
            product_trans_ar.product = product
            product_trans_ar.save()

            
            product_trans_en = Product_translation()
            product_trans_en.name = request.POST["name"]
            product_trans_en.desc = request.POST["desc"]
            product_trans_en.language = "en"
            product_trans_en.product = product
            product_trans_en.save()

            images = request.FILES.getlist("desc_images")
            
            for i in images:
                Product_images.objects.create(image = i.name, product = product)
                with open(settings.MEDIA_ROOT + "/" + i.name, "wb+") as dest:
                    for j in i.chunks():
                        dest.write(j)
                    dest.close()

                    
            messages.success(request, _("product added successfully"))
            return redirect("/admin/product/all")
            



        

def edit_product(request, id):
    product =  Product.objects.get(id = id)
    product_ar = Product_translation.objects.get(product = product, language = "ar")
    product_en =  Product_translation.objects.get(product = product, language = "en")
    context = {
        "product": product,
        "product_ar": product_ar,
        "product_en":  product_en,
        "product_category": product.category.id,
        "categories": Category_translation.objects.all()
    }
    if request.method == "GET":
        return render(request, "products/edit.html", context)

    elif request.method == "POST":
        update_product_form = UpdateProductForm(request.POST, request.FILES)
        context["form"] = update_product_form
        if not update_product_form.is_valid():
            return render(request, "products/edit.html", context)

        else:
            
            product.category = Category_translation.objects.get(name = request.POST["category"]).Category
            product.sell_price = request.POST["sell_price"]
            product.save()

        
            product_ar.name = request.POST["name_ar"]
            product_ar.desc = request.POST["desc_ar"]
            product_ar.save()

            

            product_en.name = request.POST["name"]
            product_en.desc = request.POST["desc"]
            product_en.save()

            if request.FILES.getlist("desc_images"):
                images = request.FILES.getlist("desc_images")
            
                for i in images:
                    Product_images.objects.create(image = i.name, product = product)
                    with open(settings.MEDIA_ROOT + "/" + i.name, "wb+") as dest:
                        for j in i.chunks():
                            dest.write(j)
                        dest.close()

            messages.success(request, _("product edited successfully"))
            return redirect("/admin/product/")
            





        
def detailed_product(request, id):
    product = Product.objects.get(id = id)
    product_en =  Product_translation.objects.get(product = product, language = "en")
    product_ar =  Product_translation.objects.get(product = product,  language = "ar")
    images     = Product_images.objects.filter(product = product)
    context = {
        "product": product,
        "product_en": product_en,
        "product_ar": product_ar,
        "images"    : images
    }
    return render(request, "products/detailed_product.html", context)



def delete_product(request, id):
    context = {}
    if request.method == "POST":

        product = Product.objects.get(id = id)
        images  = Product_images.objects.filter(product = product) 

        for i in images:
            if os.path.exists(settings.MEDIA_ROOT + "/" + i.image):
                os.remove(settings.MEDIA_ROOT + "/" + i.image)


        if product.delete():
            return JsonResponse({"success": True , "message": "product has been deleted successfully"})
        
        else:
            return JsonResponse({"success": False , "message": "can't delete this product"})
    else:
        return JsonResponse({"error": "wrong method"})



def delete_product_images(request):
    
    if request.method == "POST":
        images = request.POST.getlist("images[]")
        if images is not None:
            for i in images:
                if os.path.exists(settings.MEDIA_ROOT + "/" + i):
                    os.remove(settings.MEDIA_ROOT + "/" + i)
                    Product_images.objects.get(image = i).delete()
                    
            return JsonResponse({"success": True}, safe=False)

        else:
            return JsonResponse({"images": "false"})
        
    else:
        return JsonResponse({"error": "wrong method"})
