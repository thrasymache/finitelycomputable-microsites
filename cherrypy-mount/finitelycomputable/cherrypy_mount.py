import cherrypy
from os import environ
from platform import python_version
from posixpath import join

from finitelycomputable_microsites_setup import version


version_text = environ.get('MICROSITES_VERSION_TEXT', '')
base_path = join('/', environ.get('BASE_PATH', ''))
included_apps = []

class WsgiInfo(object):
    @cherrypy.expose
    def index(self):
        return (
f'''{version_text} using {__name__} {version} on Python {python_version()}
at {base_path} with {', '.join(included_apps) or "nothing"}\n'''
    )

def setup_server():
    cherrypy.tree.mount(WsgiInfo(), join(base_path, 'wsgi_info/'), {'/': {}})
    try:
        from finitelycomputable.helloworld_cherrypy import HelloWorld
        cherrypy.tree.mount(
                HelloWorld(), join(base_path,'hello_world/'), {'/': {}})
        included_apps.append('helloworld_cherrypy')
    except ModuleNotFoundError:
        pass
    return cherrypy.tree


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
