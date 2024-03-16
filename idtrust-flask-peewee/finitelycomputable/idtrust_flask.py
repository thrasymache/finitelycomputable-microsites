import flask
from jinja2 import PackageLoader


class Flask(flask.Flask):
    '''this will have __module__ == finitelycomputable.idtrust_flask_peewee'''
    # debug = True
class Blueprint(flask.Blueprint):
    '''this will have __module__ == finitelycomputable.idtrust_flask_peewee'''
    jinja_loader = PackageLoader(
            'finitelycomputable.idtrust_common', 'templates'
    )
