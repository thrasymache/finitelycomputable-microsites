import flask
from os import environ
from posixpath import join

from finitelycomputable import helloworld_cherrypy


class Flask(flask.Flask):
    '''this will have __module__ == finitelycomputable.helloworld_flask'''
class Blueprint(flask.Blueprint):
    '''this will have __module__ == finitelycomputable.helloworld_flask'''


application = Flask(__name__)
blueprint = Blueprint('helloworld', __name__)
base_path = join('/', environ.get('BASE_PATH', ''))
impl = helloworld_cherrypy.HelloWorld()


@blueprint.route('/')
def hello_world():
    return "Flask adapts, " + impl.index()

application.register_blueprint(blueprint, url_prefix = base_path)

def run():
    from sys import argv, exit, stderr
    if len(argv) < 2 or argv[1] != 'run':
        stderr.write(f'usage: {argv[0]} run [port]\n')
        exit(1)
    try:
        port=int(argv[2])
    except IndexError:
        port=8080
    application.run(port=port)
