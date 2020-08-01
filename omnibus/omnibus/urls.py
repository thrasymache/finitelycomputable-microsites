"""omnibus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
"""
from django.urls import include, path
from django.http import HttpResponse
import os

urlpatterns = []
try:
    import id_trust
    root = os.environ.get('ID_TRUST_ROOT', 'identification_of_trust/')
    urlpatterns += [
        path(root, include('id_trust.urls')),
        path('', id_trust.views.home, name='home'),
    ]
except ModuleNotFoundError:
    pass


version_url = os.environ.get('MICROSITES_VERSION_PATH')
if version_url:
    urlpatterns += [
        path(version_url, lambda request: HttpResponse(
                os.environ.get('MICROSITES_VERSION_TEXT', 'unspecified'),
                content_type='text/plain'),
            name='server_version')]
