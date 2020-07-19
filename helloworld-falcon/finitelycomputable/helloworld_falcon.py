import falcon
from os import environ
from posixpath import join


class API(falcon.API):
    '''this will have __module__ == finitelycomputable.helloworld_falcon'''

class HelloWorld(object):
    def on_get(self, req, resp):
        resp.status = falcon.HTTP_200
        resp.content_type = falcon.MEDIA_TEXT
        resp.body = 'Falcon says "hello, world"\n'


application = API()
application.req_options.strip_url_path_trailing_slash = True
base_path = join('/', environ.get('BASE_PATH', ''))
application.add_route(base_path, HelloWorld())


def run():
    from sys import argv, exit, stderr
    from wsgiref import simple_server
    if len(argv) < 2 or argv[1] != 'run':
        stderr.write(f'usage: {argv[0]} run [port]\n')
        exit(1)
    try:
        port=int(argv[2])
    except IndexError:
        port=8080
    simple_server.make_server('127.0.0.1', port, application).serve_forever()
