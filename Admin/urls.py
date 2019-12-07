from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from . import views 
from . import category_views as c_v
from . import product_views  as p_v
from . import client_views  as client_views
from . import order_views as order_views
from . import custom_auth_views as auth_views



custom_auth_urlpatterns = [
    path("/login/", auth_views.login_admin),
    path("/logout/", auth_views.logout_admin),
]

categories_urlpatterns = [
    path("/", c_v.index_category),
    path("/all/", c_v.index_category),
    path("/add/", c_v.create_category),
    path("/edit/<int:id>/", c_v.edit_category),
    path("/<int:id>/", c_v.detailed_category),
    path("/delete/<int:id>/", c_v.delete_category)

]


products_urlpatterns = [
    path("/all/", p_v.index_product),
    path("/", p_v.index_product),
    path("/cat_filt/<int:category_id>/", p_v.filtered_by_category_product),
    path("/add/", p_v.create_product),
    path("/edit/<int:id>/", p_v.edit_product),
    path("/<int:id>", p_v.detailed_product),
    path("/delete/<int:id>/", p_v.delete_product),
    path("/delete_product_images/", p_v.delete_product_images)
    
]


clients_urlpatterns = [
    path("/", client_views.index_client),
    path("/all/", client_views.index_client),
    path("/add/", client_views.create_client),
    path("/edit/<int:id>/", client_views.edit_client),
    path("/<int:id>/", client_views.detailed_client),
    path("/delete/<int:id>/", client_views.delete_client),
    ##orders
    path("/<int:client_id>/orders/add", order_views.create_order)
]

orders_urlpatterns = [
    path("/", order_views.index_order),
    path("/all", order_views.index_order),
    path("/<int:order_id>/products/", order_views.get_products_order),
    path("/edit/<int:order_id>/", order_views.edit_order),
    path("/delete/<int:order_id>/", order_views.delete_order),
]


def error403(request):
    return render(request, "403.html")


urlpatterns = [
    path("/", views.index_admin),
    path("/all/", views.all_admins),
    path('/create/', views.create_admin),
    path("/edit/<int:id>", views.edit_admin),
    path("/<int:id>", views.detailed_admin),
    path("/delete/<int:id>", views.delete_admin),
    path("/category", include(categories_urlpatterns)),
    path("/product", include(products_urlpatterns)),
    path("/client", include(clients_urlpatterns)),
    path("/order", include(orders_urlpatterns)),
    path("/error403/", error403)
]


urlpatterns += custom_auth_urlpatterns
