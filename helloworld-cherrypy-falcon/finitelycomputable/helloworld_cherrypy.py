import cherrypy
from os import environ
from falcon import Response

from finitelycomputable import helloworld_falcon


class HelloWorld(object):
    impl = helloworld_falcon.HelloWorld()

    @cherrypy.expose
    def index(self):
        resp = Response()
        self.impl.on_get(cherrypy.request, resp)
        return "CherryPy adapts, " + resp.text


def setup_server():
    return cherrypy.tree.mount(HelloWorld(), base_path, {'/': {}})

base_path = environ.get('BASE_PATH', '')
application = cherrypy.tree.mount(HelloWorld(), base_path, {'/': {}})


def run():
    from sys import argv, exit, stderr
    if len(argv) < 2 or argv[1] != 'run':
        stderr.write(f'usage: {argv[0]} run [port]\n')
        exit(1)
    try:
        cherrypy.config.update({'server.socket_port': int(argv[2])})
    except IndexError:
        pass
    cherrypy.engine.start()
    cherrypy.engine.block()
