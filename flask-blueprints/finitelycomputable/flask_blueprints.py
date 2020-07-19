from flask import Flask, cli
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
included_apps = [app.__module__
        for name, app in locals().items() if name in ['helloworld_blue']]


def run():
    from sys import argv, exit, stderr
    usage = f'usage: {argv[0]} run|routes [port]\n'
    if len(argv) < 2:
        stderr.write(usage)
        exit(1)
    if argv[1] == 'run':
        try:
            port=int(argv[2])
        except IndexError:
            port=8080
        application.run(port=port)
    else:
        environ['FLASK_APP'] = __name__
        stderr.write(environ['FLASK_APP'])
        cli.main()
