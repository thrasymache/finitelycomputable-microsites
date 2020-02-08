from flask import Flask
from os import environ
from platform import python_version
from posixpath import join

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


try:
    from finitelycomputable.helloworld_flask import blueprint as helloworld_blue
    application.register_blueprint(
            helloworld_blue, url_prefix = join(base_path, 'hello_world'))
    included_apps.append('helloworld_flask')
except ModuleNotFoundError:
    pass


def run():
    from sys import argv
    if len(argv)== 2:
        application.run(port=(argv[1]))
    else:
        application.run(port=8080)
