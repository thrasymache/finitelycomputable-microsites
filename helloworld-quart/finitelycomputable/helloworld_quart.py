#! /bin/env python
import quart 
from os import environ
from posixpath import join


class Quart(quart.Quart):
    '''this will have __module__ == finitelycomputable.helloworld_flask'''
class Blueprint(quart.Blueprint):
    '''this will have __module__ == finitelycomputable.helloworld_flask'''


application = Quart(__name__)
blueprint = Blueprint('helloworld', __name__)
base_path = join('/', environ.get('BASE_PATH', ''))


@blueprint.route('/')
async def hello_world():
    return 'Quart says "hello, world"\n'

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
