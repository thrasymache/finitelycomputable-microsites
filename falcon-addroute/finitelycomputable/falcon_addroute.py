import falcon
from os import environ
from platform import python_version
from posixpath import join

from finitelycomputable_microsites_setup import version


class WsgiInfo(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.body = (
f'''{version_text} using {__name__} {version} on Python {python_version()}
at {base_path} with {', '.join(included_apps) or "nothing"}\n'''
    )


application = falcon.API()
application.req_options.strip_url_path_trailing_slash = True
base_path = join('/', environ.get('BASE_PATH', ''))
version_text = environ.get('MICROSITES_VERSION_TEXT', '')
included_apps = []
application.add_route(join(base_path, 'wsgi_info'), WsgiInfo())

try:
    from finitelycomputable.helloworld_falcon import HelloWorld
    application.add_route(join(base_path, 'hello_world'), HelloWorld())
    included_apps.append('helloworld_falcon')
except ModuleNotFoundError:
    pass


def run():
    from sys import argv
    from wsgiref import simple_server
    try:
        port=int(argv[1])
    except IndexError:
        port=8080
    simple_server.make_server('127.0.0.1', port, application).serve_forever()
