"""django_apps URL Configuration
"""
from django.contrib import admin
from django.http import HttpResponse
from django.urls import path
from os import environ
from platform import python_version
from posixpath import join

from finitelycomputable_microsites_setup import version

base_path = environ.get('BASE_PATH', '')
version_text = environ.get('MICROSITES_VERSION_TEXT', '')
included_apps = []

def wsgi_info(request):
    return HttpResponse(
f'''{version_text} using {__name__} {version} on Python {python_version()}
at {base_path} with {', '.join(included_apps) or "nothing"}\n'''
    )

urlpatterns = [
    path('admin/', admin.site.urls),
    path(join(base_path, 'wsgi_info/'), wsgi_info),
    path(join(base_path, 'wsgi_info'), wsgi_info),
]
