import cherrypy
from os import environ

from finitelycomputable import helloworld_morepath


class HelloWorld(object):
    model = helloworld_morepath.Root()

    @cherrypy.expose
    def index(self):
        return helloworld_morepath.hello_world(self.model, cherrypy.request)


base_path = environ.get('BASE_PATH', '')
application = cherrypy.tree.mount(HelloWorld(), base_path, {'/': {}})


def run():
    from sys import argv
    if len(argv) == 2:
        cherrypy.config.update({'server.socket_port': int(argv[1])})
    cherrypy.engine.start()
    cherrypy.engine.block()
