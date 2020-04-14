from flask import Flask
from os import environ
from platform import python_version
from posixpath import join
from werkzeug.middleware.dispatcher import DispatcherMiddleware

from finitelycomputable_microsites_setup import version


application = Flask(__name__)
base_path = join('/', environ.get('BASE_PATH', ''))
version_text = environ.get('MICROSITES_VERSION_TEXT', '')
included_apps = []


@application.route(join(base_path, 'wsgi_info/'))
@application.route(join(base_path, 'wsgi_info'))
def wsgi_info():
    return (
f'''{version_text} using {__name__} {version} on Python {python_version()}
at {base_path} with {', '.join(included_apps) or "nothing"}\n'''
    )


hello_base = join(base_path, 'hello_world')
try:
    from finitelycomputable.helloworld_flask import (
            application as helloworld_app)
    included_apps.append('helloworld_flask')
except ModuleNotFoundError:
    try:
        environ['BASE_PATH'] = hello_base
        from finitelycomputable.helloworld_cherrypy import (
                application as helloworld_app)
        environ['BASE_PATH'] = base_path
        included_apps.append('helloworld_cherrypy')
    except ModuleNotFoundError:
        try:
            from finitelycomputable.helloworld_falcon import (
                    application as helloworld_app)
            included_apps.append('helloworld_falcon')
        except ModuleNotFoundError:
            pass
if 'helloworld_app' in dir():
    application.wsgi_app = DispatcherMiddleware(application.wsgi_app, {
            hello_base: helloworld_app
    })


def run():
    from sys import argv
    if len(argv)== 2:
        application.run(port=(argv[1]))
    else:
        application.run(port=8080)
