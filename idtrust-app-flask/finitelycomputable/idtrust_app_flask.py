import flask
from os import environ
from posixpath import join
from finitelycomputable.idtrust_flask import Flask, Blueprint
from finitelycomputable.idtrust_db.controller import (
        dialog_from_id, journey_from_id, create_dialog, interact_core
)
from finitelycomputable.idtrust_common.strategies import Strategy


application = Flask(__name__)
blueprint = Blueprint('idtrust', __name__)
base_path = join('/', environ.get('BASE_PATH', ''))


@blueprint.route('interact/<int:pk>', defaults={'blind': True},
        methods=('GET', 'POST'))
@blueprint.route('interact/<int:pk>/reveal_miscommunication',
        methods=('GET', 'POST'))
def interact(pk, blind=False):
    try:
        interaction = dialog_from_id(pk)
    except:
        flask.abort(flask.Response(f"Dialog {pk} not found.", 404))
    return flask.render_template('interaction.html',
        new_partner_url=flask.url_for(
                'idtrust.new_dialogue',
                journey_id=interaction.journey_id,
                blind=blind),
        new_journey_url=flask.url_for('idtrust.new_dialogue', blind=blind),
        **interact_core(
            interaction,
            blind,
            flask.request.form.get('user_intent'),
            flask.request.form.get('user_guess'),
    ))


@blueprint.route('', defaults={'blind': True}, methods=('GET', 'POST'))
@blueprint.route('choose_miscommunication',
        defaults={'blind': False}, methods =('GET', 'POST'))
@blueprint.route('journey/<int:journey_id>',
        defaults={'blind': True}, methods =('GET', 'POST'))
@blueprint.route('journey/<int:journey_id>/choose_miscommunication',
        defaults={'blind': False}, methods=('GET', 'POST'))
@blueprint.endpoint('home')
def new_dialogue(blind, journey_id=None):
    try:
        journey = journey_from_id(journey_id)
    except:
        flask.abort(flask.Response(f"Journey {journey_id} not found.", 404))
    if flask.request.method != 'POST':
        return flask.render_template('interaction_begin.html', **{
                'blind': blind,
                'journey': journey,
                'form': None,
                'blind_toggle_url': flask.url_for(
                    'idtrust.new_dialogue',
                    journey_id=journey_id,
                    blind=not blind),
        })
    obj = create_dialog(
            journey,
            flask.request.form.get('user_miscommunication'),
            flask.request.form.get('foil_miscommunication'),
    )
    interact_core(obj, not blind, flask.request.form.get('user_intent'))
    return flask.redirect(
            flask.url_for( 'idtrust.interact', pk=obj.id, blind=True)
    )

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
