"""id_trust URL Configuration
"""
from django.urls import path
from finitelycomputable.idtrust_django import views

app_name = 'id_trust'
urlpatterns = [
    path('', views.home, name='blind_home'),
    path('choose_miscommunication', views.home,
        {'blind': False}, name='reveal_home'),
    path('interact/<int:pk>', views.interact, {'blind': True},
        name='blind_interact'),
    path('interact/<int:pk>/reveal_miscommunication', views.interact,
        {'blind': False}, name='reveal_interact'),
    path('class_home', views.Home.as_view(), name='class_home'),
    path('class_interact/<int:pk>', views.Interact.as_view(),
        name='class_interact'),
    path('exchange_create/<int:interaction_id>', views.ExchangeCreate.as_view(),
        name='exchange_create'),
]
