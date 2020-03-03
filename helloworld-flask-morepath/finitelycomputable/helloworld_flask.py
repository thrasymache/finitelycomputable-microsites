from flask import Blueprint, Flask, request
from os import environ
from posixpath import join

from finitelycomputable import helloworld_morepath


application = Flask(__name__)
blueprint = Blueprint('helloworld', __name__)
base_path = join('/', environ.get('BASE_PATH', ''))
model = helloworld_morepath.Root()


@blueprint.route('/')
def hello_world():
    return helloworld_morepath.hello_world(model, request)

application.register_blueprint(blueprint, url_prefix = base_path)

def run():
    from sys import argv
    if len(argv)== 2:
        application.run(port=(argv[1]))
    else:
        application.run(port=8080)
