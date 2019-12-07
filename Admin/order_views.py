import logging
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import Client, Category, Category_translation, Product_translation, Order, Product, Order_product
from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import gettext as _, get_language
from pprint import pprint
from django.template.loader import render_to_string
from django.core.paginator import Paginator
from .decorators import is_allowed

@is_allowed("read_order")
def index_order(request):

    ctx = {}
    per_page = 3
    if request.GET.get("q", None) != None:
        q = request.GET.get("q", "")
        orders = Paginator (Order.objects.prefetch_related("client", "product") \
                            .filter(client__name__contains=q) , per_page) \
                            .get_page(request.GET.get("page",1)
                            )
    else:
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

@is_allowed("read_order")
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

    # from django.db import connection
    # pprint(connection.queries)
    
    return JsonResponse(response)

    
#########################################################################################################################

@is_allowed("create_order")
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
        delivered = request.POST.get("delivered", None)

        if products == None or len(products) == 0 or  quantities == None or len(quantities) == 0:
            return JsonResponse({"success": False, "message": "some parameters are missing"})

        order_request = dict(zip(products, quantities))

        order = Order()
        order.client = client
        
        if delivered != None:
            delivered_state = True if delivered ==  "delivered" else False
            order.delivered = delivered_state


        for k,v  in order_request.items():

            product = Product.objects.get(id = k)
            product.available_quantity = int(product.available_quantity) - int(v)
            if product.available_quantity < 0:
                prod_name = Product_translation.objects.get(product=product, language = get_language()).name
                messages.error(request, _("prouct has no enough available quantity"))
                return redirect(request.META.get('HTTP_REFERER'))
            product.save()

            
            order.save()
            Order_product.objects.create(
                order = order,
                product = Product.objects.get(id = k),
                quantity = v,
            )
            messages.success(request, _("order created successfully"))    
        return redirect("/admin/order/all")



#########################################################################################################################

@is_allowed("edit_order")
def edit_order(request, order_id):
    ctx = {}

    categories = Category.objects.all()

    categories_translation =  Category_translation.objects.prefetch_related("Category").filter(language= str(get_language()))

    try:
        order = Order.objects.prefetch_related("order_product_set", "product").get(id=order_id)    
    except ObjectDoesNotExist:
        return render(request, "404.html")
    

    client = order.client
    
    related_products = order.product.all() 

    products_translations = Product_translation.objects.prefetch_related("product").filter(product__in= related_products, language= get_language())


    ctx["order"] = order
    
    ctx["categories"] = categories

    ctx["categories_translation"] = categories_translation

    ctx["products"] = products_translations
    
    if request.method == "GET":
        return render(request, "orders/edit.html", ctx)

    elif request.method == "POST":

        products = request.POST.getlist("products[]", None)
        quantities = request.POST.getlist("quantities[]", None)
        delivered = request.POST.get("delivered", None)
        
        

        if products == None or len(products) == 0 or  quantities == None or len(quantities) == 0 or delivered == None:
            return JsonResponse({"success": False, "message": "some parameters are missing", "request": request.POST})
        
        
        #delete the old order
        for product in order.product.all():
            product.available_quantity = int(product.available_quantity) + int(Order_product.objects.get(product_id = product.id, order_id = order_id).quantity) 
            product.save()
            order.product.remove(product)
            
        pprint(request.POST)
            
        #create the new order
        order_request = dict(zip(products, quantities))
        delivered_state = True if delivered ==  "delivered" else False
        
        
        order.client = client
        order.delivered = delivered_state
        order.save()

        # order.save()

        for k,v  in order_request.items():


            product = Product.objects.get(id = k)

            product.available_quantity = int(product.available_quantity) - int(v)
            
            if product.available_quantity < 0:
                messages.error(request, _("prouct has no enough available quantity"))
                return redirect("/admin/order/")
            
            product.save()
            
            Order_product.objects.create(
                order = order,
                product = Product.objects.get(id = k),
                quantity = v,
            )
        messages.success(request, _("order updated successfully"))    
        return redirect("/admin/order/")




















    

    


@is_allowed("delete_order")
def delete_order(request, order_id):

    if request.method == "POST":
        try:
            order = Order.objects.prefetch_related("product").get(id= order_id)
        except ObjectDoesNotExist:
            return HttpResponse("no order found")
        
        
        for product in order.product.all():
            product.available_quantity = int(product.available_quantity) + int(Order_product.objects.get(product_id = product.id, order_id = order_id).quantity) 
            product.save()


        if order.delete():

            response = {
                "success": True,
                "message": _("order deleted successfully")
            }
        else:
            response = {
                "success": False,
                "message": _("error, can't delete order")
            }

            
        return JsonResponse(response)

    else:
        return JsonResponse({
            "success": False,
            "message": "methd not allowed"
        }, status=405)
