"""id_trust URL Configuration

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
from django.urls import path
from finitelycomputable.idtrust_django import views

app_name = 'id_trust'
urlpatterns = [
    path('', views.home, name='home'),
    path('real/<int:pk>', views.interact,
        {'secrets': False}, name='real_interact'),
    path('reveal/<int:pk>', views.interact,
        {'secrets': True}, name='reveal_interact'),
    path('class_home', views.Home.as_view(), name='class_home'),
    path('real/<int:pk>', views.Interact.as_view(), name='class_real_interact'),
    path('reveal/<int:pk>', views.RevealInteract.as_view(),
        name='class_reveal_interact'),
    path('exchange_create/<int:interaction_id>', views.ExchangeCreate.as_view(),
        name='exchange_create'),
]
