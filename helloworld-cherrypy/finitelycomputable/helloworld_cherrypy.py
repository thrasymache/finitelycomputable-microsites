import cherrypy
from os import environ


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return 'CherryPy says "hello, world"\n'


base_path = environ.get('BASE_PATH', '')
application = cherrypy.tree.mount(HelloWorld(), base_path, {'/': {}})


def run():
    from sys import argv
    if len(argv) == 2:
        cherrypy.config.update({'server.socket_port': int(argv[1])})
    cherrypy.engine.start()
    cherrypy.engine.block()
