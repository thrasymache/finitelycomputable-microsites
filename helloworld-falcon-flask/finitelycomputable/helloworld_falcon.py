import falcon
from os import environ
from posixpath import join

from finitelycomputable import helloworld_flask


class HelloWorld(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.body = helloworld_flask.hello_world()


application = falcon.API()
application.req_options.strip_url_path_trailing_slash = True
base_path = join('/', environ.get('BASE_PATH', ''))
application.add_route(base_path, HelloWorld())


def run():
    from sys import argv
    from wsgiref import simple_server
    try:
        port=int(argv[1])
    except IndexError:
        port=8080
    simple_server.make_server('127.0.0.1', port, application).serve_forever()
