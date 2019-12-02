from django.shortcuts import render, redirect, HttpResponse
from django.utils import translation
from faker import Faker
from Admin.models import Client, Category,  Category_translation, Product, Product_translation, Product_images
import random

def change_lang(request, LANG):

    request.session[translation.LANGUAGE_SESSION_KEY] = LANG

    translation.activate(LANG)

    
    if request.session.get("user_id"): #logged in
        return redirect("/" + LANG + "/admin/all") 
    else:
        redirect("/")





def fake(request):

    fake_ar = Faker("ar_SA")
    fake_en = Faker()

    ##fake clients
    # for i in range(1, 50):
    #     Client.objects.create(name=fake.name(), address=fake.address(), phone=fake.phone_number() )

    ##fake categorys
    # for i in range(1, 10):
    #     Category.objects.create(
    #         desc_image = "32dc4a04-8cf1-46b6-b28e-fcdc5b60e54c.gif"
    #     )

    ## fake category_translate

    # for i in range(30, 38):
    #     Category_translation.objects.create(
    #         name = fake_en.sentence(nb_words=2),
    #         desc = fake_en.sentence(),
    #         Category= Category.objects.get(id = i),
    #         language = "en"
    #     )

    #     Category_translation.objects.create(
    #         name = fake_ar.sentence(nb_words=2),
    #         desc = fake_ar.text(1),
    #         Category= Category.objects.get(id = i),
    #         language = "ar"
    #     )


    
    # fake product
    # for i in range(1, 10):
    #     Product.objects.create(
    #         category = Category.objects.get(id = random.randrange(30, 37,1))
    #     )

    
    
    # product_translate faker
    
    for i in range(42, 51):        
        Product_translation.objects.create(
            name = fake_en.sentence(nb_words=3),
            desc = fake_en.sentence(),
            product= Product.objects.get(id = i),
            language = "en"
        )

        Product_translation.objects.create(
            name = fake_ar.sentence(nb_words=3),
            desc = fake_ar.sentence(),
            product= Product.objects.get(id = i),
            language = "ar"
        )

        for j in range(1, 10):
            Product_images.objects.create(
                product = Product.objects.get(id=i),
                image   = "oo.png"
            )
            
    
    return HttpResponse("doned")


# def test(request):
#     from django.db import connection
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT product_en.name as name_en, \
#         product_ar.name as name_ar, \
#         product_en.desc as desc_en, \
#         product_ar.desc as desc_ar, \
#         product_en.product_id \
#         FROM product_translation as product_en \
#         INNER JOIN product_translation as product_ar \
#         on product_en.product_id = product_ar.product_id and product_en.id != product_ar.id \
#         GROUP BY product_en.product_id" )
#         row = cursor.fetchall()
#         for i in row:
#             print("\n\n" + i[0] + " | " + i[1])
#     return HttpResponse("test")


# def test(request):
#     from Admin.models import Product_translation
#     from itertools import chain
#     res = HttpResponse()
    
#     product_en = Product_translation.objects.filter(language = "en")
#     product_ar = Product_translation.objects.filter(language = "ar")
#     p = list(chain(product_en, product_ar))

#     for index, i in enumerate(p):
#          res.write(str(index +1 ) + "- " + i.name + "|" +i.language +"</br>")    
#     return res


def datatables(request):
    import csv
    from Admin.models import Admin
    response = HttpResponse(content_type="text/csv")
    response['Content-Disposition'] = 'attachment; filename="users.csv"'
    writer = csv.writer(response)
    writer.writerow(['username', 'fullname', 'email'])
    users = Admin.objects.all().values_list("username", "fullname", "email")
    for user in users:
        writer.writerow(user)
    return response
