from finitelycomputable.django_apps.settings.base import *

DEBUG = False

ALLOWED_HOSTS += 'finitelycomputable.nfshost.com',
CSRF_COOKIE_SECURE = True
SECURE_CONTENT_TYPE_NOSNIFF = True
#SECURE_HSTS_INCLUDE_SUBDOMAINS = True
#SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 60
#SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
