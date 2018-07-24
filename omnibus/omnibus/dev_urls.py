"""omnibus dev URL Configuration """
from django.contrib import admin
from django.urls import path
from omnibus.urls import urlpatterns

urlpatterns += [
    path('admin/', admin.site.urls),
]
