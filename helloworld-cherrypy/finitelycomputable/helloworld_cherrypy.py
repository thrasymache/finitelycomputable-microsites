import cherrypy
from os import environ


class Application(cherrypy.Application):
    '''this will have __module__ == finitelycomputable.helloworld_cherrypy'''


class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return 'CherryPy says "hello, world"\n'


def setup_server():
    return cherrypy.tree.mount(HelloWorld(), base_path, {'/': {}})

base_path = environ.get('BASE_PATH', '')
application = setup_server()


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
