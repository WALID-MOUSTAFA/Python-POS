from django.urls import path
from . import views

urlpatterns = [
    path("/lang/<str:LANG>/", views.change_lang),
    path("/fake/", views.fake),
    # path("/test/", views.test)
    path("/dt/", views.datatables)
]

