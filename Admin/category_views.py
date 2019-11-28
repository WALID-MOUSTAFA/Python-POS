from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CreateCategoryForm, UpdateCategoryForm
from .models import Category, Category_translation
import json
import os
import uuid
from django.conf import settings
from django.utils.translation import gettext_lazy as _, get_language
from django.db.models import Q
from django.core.paginator import Paginator

def index_category(request):
    per_page = 2
    page= request.GET.get("page", 1)
    LANG = get_language()

    if request.GET.get("q", None):
        q = request.GET.get("q")

        if LANG == "en":
            categories_trans = Category_translation.objects.filter(Q(name__contains=q) | Q(desc__contains=q), language = "en")
        else:
            categories_trans = Category_translation.objects.filter(Q(name__contains=q) | Q(desc__contains=q), language = "ar")
                        
        
        result_categories_trans_ids = categories_trans.values_list("Category__id", flat=True)

        categories = Category.objects.filter(id__in=result_categories_trans_ids)
        
    else:
        if LANG=="en":
            categories_trans = Category_translation.objects.filter(language = "en")
        else:
            categories_trans = Category_translation.objects.filter(language = "ar")
        
        categories = Category.objects.all()

    context = {
        "title": "Categories",
        "categories_trans": Paginator(categories_trans, per_page).get_page(page),
        "categories" : Paginator(categories, per_page).get_page(page)
    }



    return render(request, "categories/all.html",context)



def create_category(request):
    context = {"title": "Create category"}

    if request.method == "GET":
        return render(request, "categories/create.html",context)

    elif request.method == "POST":

        upload_url = os.path.join(settings.BASE_DIR, "media")
        
        create_categorg_form = CreateCategoryForm(request.POST, request.FILES) 

        if not create_categorg_form.is_valid():

            context["form_error"] = json.loads(create_categorg_form.errors.as_json())

            context["form"] = create_categorg_form

            return render(request, "categories/create.html", context)

        else:
            #parent category
            category = Category()
            desc_image = str(uuid.uuid4()) + '.' + request.FILES.get("desc_image").name.split(".")[-1]
            category.desc_image = desc_image
            category.save()
            
            with open(upload_url + "/" + desc_image, "wb+") as dest:
                for i in request.FILES.get("desc_image").chunks():
                    dest.write(i)

            #en category
            cate_trans_en = Category_translation()
            cate_trans_en.language = "en"
            cate_trans_en.name = request.POST.get("name")
            cate_trans_en.desc = request.POST.get("desc")
            cate_trans_en.Category = category
            cate_trans_en.save()
            
            cate_trans_ar = Category_translation()
            cate_trans_ar.language = "ar"
            cate_trans_ar.name = request.POST.get("name_ar")
            cate_trans_ar.desc = request.POST.get("desc_ar")
            cate_trans_ar.Category = category
            cate_trans_ar.save()

                
            
            messages.success(request, _("category added successfully"))
            return redirect("/admin/category/")
    


def edit_category(request, id):
    
    category = Category.objects.get(id = id)
    category_en = Category_translation.objects.get(Category = category, language = "en")
    category_ar = Category_translation.objects.get(Category = category, language = "ar")
    context = {}
    context["category"]    = category
    context["category_en"] = category_en
    context["category_ar"] = category_ar
    
    if request.method == "GET":
        return render(request, "categories/edit.html",context)

    elif request.method == "POST":
        update_category_form = UpdateCategoryForm(request.POST, request.FILES)
        
        if not update_category_form.is_valid():

            context["form_error"] = json.loads(update_category_form.errors.as_json())
            context["form"] = update_category_form
            return render(request, "categories/edit.html",context)

        else:
 
            category_en.name = request.POST.get("name")
            category_en.desc = request.POST.get("desc")
            category_en.save()
            category_ar.name = request.POST.get("name_ar")
            category_ar.desc = request.POST.get("desc_ar")
            category_ar.save()
            

            if request.FILES.get("desc_image") != None:
                old_image = category.desc_image
                if os.path.exists(settings.MEDIA_ROOT + "/" + old_image):
                    os.remove(settings.MEDIA_ROOT + "/" + old_image)

                desc_image = str(uuid.uuid4()) + '.' + request.FILES.get("desc_image").name.split(".")[-1]

                category.desc_image = desc_image
                upload_url = settings.MEDIA_ROOT 
                with open(upload_url + "/" + desc_image, "wb+") as dest:
                    for i in request.FILES.get("desc_image").chunks():
                        dest.write(i)

                        
            category.save()
            messages.success(request, _("category has been edited successfully"))
            return redirect("/admin/category/all")

            
        


def detailed_category(request, id):
    context = {}
    
    category = Category.objects.get(id = id)
    category_en = Category_translation.objects.get(Category=category, language = "en")
    category_ar = Category_translation.objects.get(Category=category, language = "ar")

    context = {
        "category": category,
        "category_en": category_en,
        "category_ar":category_ar
    }

    if request.method == "GET":
        return render(request, "categories/detailed_category.html", context)

    

def delete_category(request, id):
    context = {}

    if request.method == "POST":
        
        category = Category.objects.get(id = id)

        if category.delete():
            return JsonResponse({"success": True , "message": "category has been deleted successfully"})
        else:           
            return JsonResponse({"success": False , "message": "can't delete this category"})
    else:
        return JsonResponse({"error": "wrong method"})
