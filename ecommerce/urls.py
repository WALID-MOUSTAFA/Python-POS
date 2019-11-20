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
from django.conf import settings
from django.contrib import admin
from django.urls import path
from django.urls import include
from Admin import urls as adminUrls
from commons import urls as commonsUrls
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _ 


def index(request):
    from django.http import HttpResponse
  
    return HttpResponse("<h1> <a href='/admin/'> Admin</a> </h1>")

urlpatterns = [
   

]

urlpatterns += i18n_patterns(

    path("", index),
    path('djangoadmin/', admin.site.urls),
    path("admin", include(adminUrls) ),
    path("commons", include(commonsUrls)),

    prefix_default_language=True)+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path("__debug__", include(debug_toolbar.urls))
    ]
