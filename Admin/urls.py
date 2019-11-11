"""ecommerce URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from . import views 
from . import category_views as c_v


categories_urlpatterns = [
    path("/all/", c_v.index_category),
    path("/add/", c_v.create_category),
    path("/edit/<int:id>/", c_v.edit_category),
    path("/<int:id>", c_v.detailed_category),
    path("/delete/<int:id>", c_v.delete_category)

]


urlpatterns = [
    path("/", views.index_admin),
    path("/login/", views.login_admin),
    path("/logout/", views.logout_admin),
    path("/all/", views.all_admins),
    path("/create/", views.create_admin),
    path("/edit/<int:id>", views.edit_admin),
    path("/<int:id>", views.detailed_admin),
    path("/delete/<int:id>", views.delete_admin),

    path("/category", include(categories_urlpatterns))
    
]
