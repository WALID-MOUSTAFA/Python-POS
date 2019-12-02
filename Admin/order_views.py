import logging
from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from .models import Client, Category, Category_translation, Product_translation, Order, Product, Order_product
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _, get_language
from pprint import pprint
from django.template.loader import render_to_string
from django.core.paginator import Paginator

def index_order(request):
    ctx = {}
    per_page = 3
    orders = Paginator(Order.objects.prefetch_related("client", "product").all(), per_page).get_page(request.GET.get("page",1))
    prices_list = {}
    sum = 0

    for o in orders:
        for p in o.product.all():
            sum+=float(p.sell_price) * float(Order_product.objects.get(order_id = o.id, product_id = p.id).quantity)
        prices_list[o.id] = sum
        sum = 0
        
    
    ctx["orders"] = orders
    ctx["prices_list"] = prices_list
    return render(request, "orders/all.html", ctx)



##############################################################################


def get_products_order(request, order_id):
    LANG = get_language()

    try:
        order = Order.objects.prefetch_related("product").get(id= order_id)
    except ObjectDoesNotExist:
        return JsonResponse({"success": False, "html": "<h1> order dosn't exist </h1>"})
    
    
    related_products_ids = [p.id for p in order.product.all()]
    products = Product_translation.objects.prefetch_related("product").filter(product__id__in=related_products_ids, language=LANG)
    order_products = Order_product.objects.filter(order=order)

    
    sum = 0
    for i in order.product.all():
        sum += float(i.sell_price) * float(order_products.get(product_id = i.id).quantity)
        
    
    ctx =  {
        "order": order,
        "products": products,
        "order_products": order_products,
        "sum" : sum
    }

    html = render_to_string("orders/get_order_products.html", ctx)

    response= {
        "success": True,
        "html"   : html
    }

    from django.db import connection
    pprint(connection.queries)
    
    return JsonResponse(response)

    
##############################################################################

def create_order(request, client_id):
    ctx = {}


    try:
        client = Client.objects.get(id = client_id)
    except ObjectDoesNotExist:
        return render(request, "404.html", status=404)

    if request.method == "GET":
        categories = Category.objects.all()
        categories_translation =  Category_translation.objects.prefetch_related("Category").filter(language= str(get_language()))


        ctx["client_id"] = client_id
        ctx["categories"] = categories
        ctx["categories_translation"] = categories_translation
        return render(request, "orders/create.html", ctx) 

    elif request.method == "POST":
        
        products = request.POST.getlist("products[]")
        quantities = request.POST.getlist("quantities[]")
        order_request = dict(zip(products, quantities))

        order = Order()
        order.client = client
        order.save()

        for k,v  in order_request.items():
            Order_product.objects.create(
                order = order,
                product = Product.objects.get(id = k),
                quantity = v,
            )
        return HttpResponse("response")
