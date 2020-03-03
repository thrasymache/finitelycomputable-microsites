from flask import Blueprint, Flask
from os import environ
from posixpath import join

from finitelycomputable import helloworld_cherrypy


application = Flask(__name__)
blueprint = Blueprint('helloworld', __name__)
base_path = join('/', environ.get('BASE_PATH', ''))
impl = helloworld_cherrypy.HelloWorld()


@blueprint.route('/')
def hello_world():
    return impl.index()

application.register_blueprint(blueprint, url_prefix = base_path)

def run():
    from sys import argv
    if len(argv) == 2:
        application.run(port=(argv[1]))
    else:
        application.run(port=8080)
