from finitelycomputable.django_apps.settings.base import *
# CSRF_COOKIE_SECURE = True
DEBUG = True
INSTALLED_APPS += [
    'django.contrib.admin',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]
MIDDLEWARE += [
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]
# SECURE_CONTENT_TYPE_NOSNIFF = True
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# SECURE_HSTS_PRELOAD = True
# SECURE_HSTS_SECONDS = 60
# SECURE_SSL_REDIRECT = True
# SESSION_COOKIE_SECURE = True
X_FRAME_OPTIONS = 'DENY'
