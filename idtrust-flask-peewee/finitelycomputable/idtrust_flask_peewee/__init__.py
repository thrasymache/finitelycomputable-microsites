import flask
from jinja2 import PackageLoader
from os import environ
from posixpath import join


class Flask(flask.Flask):
    '''this will have __module__ == finitelycomputable.idtrust_flask'''
    # debug = True
class Blueprint(flask.Blueprint):
    '''this will have __module__ == finitelycomputable.idtrust_flask'''
    jinja_loader = PackageLoader(
            'finitelycomputable.idtrust_common', 'templates'
    )



application = Flask(__name__)
blueprint = Blueprint('idtrust', __name__)
base_path = join('/', environ.get('BASE_PATH', ''))


import random
from finitelycomputable.idtrust_db_peewee import (
    IdTrustJourney,
    IdTrustDialog,
    IdTrustExchange,
)
from finitelycomputable.idtrust_common.strategies import (
    Strategy, effect, pct_deviation, impl, trust_list_display,
)

def interact_core(pk, blind):
    try:
        interaction = IdTrustDialog.get(IdTrustDialog.id == pk)
    except:
        flask.abort(flask.Response(f"Dialog {pk} not found.", 404))
    foil_intent = impl(interaction.foil_strategy)(
            [e.user_effect for e in interaction.idtrustexchange_set])
    user_intent = flask.request.form.get('user_intent')
    if user_intent == 'Trust':
        user_intent = True
    elif user_intent == 'Distrust':
        user_intent = False
    if user_intent in [True, False]:
        IdTrustExchange.create(
            interaction_id=interaction.id,
            user_intent=user_intent,
            user_effect=effect(user_intent, interaction.user_miscommunication),
            foil_intent=foil_intent,
            foil_effect=effect(foil_intent, interaction.foil_miscommunication),
        )
    user_guess = flask.request.form.get('user_guess')
    if user_guess:
        interaction.user_guess = user_guess
        interaction.save()
    user_intent = [j.user_intent for j in interaction.idtrustexchange_set]
    user_effect = [j.user_effect for j in interaction.idtrustexchange_set]
    foil_intent = [j.foil_intent for j in interaction.idtrustexchange_set]
    foil_effect = [j.foil_effect for j in interaction.idtrustexchange_set]
    strategy_list = []
    if len(user_intent):
        for (k, v) in Strategy.choices():
            st = impl(k)
            strategy_list.append({
                'strategy': v,
                'foil_intent': 100-pct_deviation(foil_intent, user_effect, st),
                'foil_effect': 100-pct_deviation(foil_effect, user_effect, st),
                'user_intent': 100-pct_deviation(user_intent, foil_effect, st),
                'user_effect': 100-pct_deviation(user_effect, foil_effect, st),
            })
    strategy_list.sort(key=lambda t: t['foil_intent'], reverse=True)
    return {
        'interaction': interaction,
        'user_intent': trust_list_display(user_intent),
        'user_effect': trust_list_display(user_effect),
        'foil_effect': trust_list_display(foil_effect),
        'foil_intent': trust_list_display(foil_intent),
        'blind': blind,
        'strategy_list': strategy_list,
        'strategies': Strategy,
        'new_partner_url': flask.url_for(
                'idtrust.new_dialogue',
                journey_id=interaction.journey_id,
                blind=blind),
        'new_journey_url': flask.url_for(
                'idtrust.new_dialogue',
                blind=blind),
    }

@blueprint.route('interact/<int:pk>', defaults={'blind': True},
        methods=('GET', 'POST'))
@blueprint.route('interact/<int:pk>/reveal_miscommunication',
        methods=('GET', 'POST'))
def interact(pk, blind=False):
    return flask.render_template('interaction.html',
        **interact_core(pk, blind))


@blueprint.route('', defaults={'blind': True}, methods=('GET', 'POST'))
@blueprint.route('choose_miscommunication',
        defaults={'blind': False}, methods =('GET', 'POST'))
@blueprint.route('journey/<int:journey_id>',
        defaults={'blind': True}, methods =('GET', 'POST'))
@blueprint.route('journey/<int:journey_id>/choose_miscommunication',
        defaults={'blind': False}, methods=('GET', 'POST'))
@blueprint.endpoint('home')
def new_dialogue(blind, journey_id=None):
    if journey_id is not None:
        try:
            journey = IdTrustJourney.get(IdTrustJourney.id == journey_id)
        except:
            flask.abort(flask.Response(f"Journey {journey_id} not found.", 404))
    else:
        journey = None
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
    try:
        user_miscommunication = float(flask.request.form.get('user_miscommunication'))
    except (ValueError, TypeError):
        user_miscommunication = round(random.random() / 2, 2)
    try:
        foil_miscommunication = float(flask.request.form.get('foil_miscommunication'))
    except (ValueError, TypeError):
        foil_miscommunication = round(random.random() / 2, 2)
    if journey_id is None:
        journey = IdTrustJourney.create()
    obj = IdTrustDialog.create(
        journey_id=journey.id,
        foil_strategy=random.choice(Strategy.choices())[0],
        user_miscommunication=user_miscommunication,
        foil_miscommunication=foil_miscommunication,
    )
    interact_core(obj.id, not blind)
    return flask.redirect(obj.get_absolute_url())

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
