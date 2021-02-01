import os
import sys

path = os.path.expanduser('~/mysite')
if path not in sys.path:
        sys.path.append(path)
        os.environ['DJANGO_SETTINGS_MODULE'] = 'finitelycomputable.django_apps.settings.pythonanywhere'
        from django.core.wsgi import get_wsgi_application
        from django.contrib.staticfiles.handlers import StaticFilesHandler
        application = StaticFilesHandler(get_wsgi_application())
