================================
Identification of Trust (Django)
================================

This is a implementation of the Identification of Trust microsite using the
Django framework

Installation::

  INSTALLED_APPS += 'finitelycomputable.idtrust_django.apps.IdTrustConfig',
  urlpatterns += path('identification_of_trust/',
                      include('finitelycomputable.idtrust_django.urls')),
