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
        return resp.body


base_path = environ.get('BASE_PATH', '')
application = cherrypy.tree.mount(HelloWorld(), base_path, {'/': {}})


def run():
    from sys import argv
    if len(argv) == 2:
        cherrypy.config.update({'server.socket_port': int(argv[1])})
    cherrypy.engine.start()
    cherrypy.engine.block()
