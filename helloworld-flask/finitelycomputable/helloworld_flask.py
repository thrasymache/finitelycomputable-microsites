from flask import Blueprint, Flask
from os import environ
from posixpath import join


application = Flask(__name__)
blueprint = Blueprint('helloworld', __name__)
base_path = join('/', environ.get('BASE_PATH', ''))


@blueprint.route('/')
def hello_world():
    return 'Flask says "hello, world"\n'

application.register_blueprint(blueprint, url_prefix = base_path)

def run():
    from sys import argv
    if len(argv)== 2:
        application.run(port=(argv[1]))
    else:
        application.run(port=8080)
