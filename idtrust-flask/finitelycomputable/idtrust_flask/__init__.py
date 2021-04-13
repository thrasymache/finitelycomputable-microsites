import flask
from jinja2 import PackageLoader
from os import environ
from posixpath import join


class Flask(flask.Flask):
    '''this will have __module__ == finitelycomputable.idtrust_flask'''
class Blueprint(flask.Blueprint):
    '''this will have __module__ == finitelycomputable.idtrust_flask'''
    jinja_loader = PackageLoader(
            'finitelycomputable.idtrust_common', 'templates'
    )



application = Flask(__name__)
blueprint = Blueprint('idtrust', __name__)
base_path = join('/', environ.get('BASE_PATH', ''))


@blueprint.route('/e')
def exchange_form():
    return flask.render_template('exchange_form.html', form=None)

@blueprint.route('/i')
def interaction():
    return flask.render_template('interaction.html', form=None)

@blueprint.route('/ib')
def interaction_begin():
    return flask.render_template('interaction_begin.html', form=None)

@blueprint.route('/')
def hello_world():
    return 'Flask says "ID trust!"\n'

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
