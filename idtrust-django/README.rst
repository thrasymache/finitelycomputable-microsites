=======================
Identification of Trust
=======================

This is the implementation of the Identification of Trust microsite.

Installation::

  INSTALLED_APPS += 'finitelycomputable.idtrust_django.apps.IdTrustConfig',
  urlpatterns += path('identification_of_trust/',
                      include('finitelycomputable.idtrust_django.urls')),
