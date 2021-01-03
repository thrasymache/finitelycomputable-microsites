"""django_apps URL Configuration
"""
from django.conf import settings
from django.http import HttpResponse
from django.urls import include, path
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
at {base_path} with {', '.join(included_apps) or "nothing"}\n''',
        content_type='text/plain',
    )

urlpatterns = [
    path(join(base_path, 'wsgi_info/'), wsgi_info),
    path(join(base_path, 'wsgi_info'), wsgi_info),
]

if 'django.contrib.admin' in settings.INSTALLED_APPS:
    from django.contrib import admin
    urlpatterns += [
        path('admin/', admin.site.urls),
    ]

if 'finitelycomputable.helloworld_django' in settings.INSTALLED_APPS:
    urlpatterns += [
    path(join(base_path, 'hello_world/'),
         include('finitelycomputable.helloworld_django.urls')),
    ]
    included_apps.append('helloworld_django')

if 'finitelycomputable.idtrust_django.apps.IdTrustConfig' in settings.INSTALLED_APPS:
    from finitelycomputable.idtrust_django import views
    root = environ.get('BASE_PATH', 'identification_of_trust/')
    urlpatterns += [
        path(root, include('finitelycomputable.idtrust_django.urls')),
        path('', views.home, name='home'),
    ]
    included_apps.append('idtrust_django')
