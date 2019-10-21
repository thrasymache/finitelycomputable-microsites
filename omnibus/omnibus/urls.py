"""omnibus URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import include, path
from django.http import HttpResponse
import id_trust
import os

urlpatterns = [
    path('identification_of_trust/', include('id_trust.urls')),
    path('', id_trust.views.home, name='home'),
]

version_url = os.environ.get('OMNIBUS_VERSION_URL')
if version_url:
    urlpatterns += [
        path(version_url, lambda request: HttpResponse(
                os.environ.get('OMNIBUS_VERSION_TEXT', 'unspecified'),
                content_type='text/plain'),
            name='server_version')]
