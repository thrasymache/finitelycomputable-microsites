import random
from finitelycomputable.idtrust_db.models import (
    IdTrustJourney,
    IdTrustDialog,
    IdTrustExchange,
)
from finitelycomputable.idtrust_common.strategies import (
    Strategy, effect, pct_deviation, impl, trust_list_display,
)

def dialog_from_id(pk):
    return IdTrustDialog.get(IdTrustDialog.id == pk)

def journey_from_id(journey_id):
    if journey_id is not None:
        return IdTrustJourney.get(IdTrustJourney.id == journey_id)
    else:
        return None

def create_dialog(journey, user_miscommunication, foil_miscommunication):
    try:
        user_miscommunication = float(user_miscommunication)
    except (ValueError, TypeError):
        user_miscommunication = round(random.random() / 2, 2)
    try:
        foil_miscommunication = float(foil_miscommunication)
    except (ValueError, TypeError):
        foil_miscommunication = round(random.random() / 2, 2)
    if journey is None:
        journey = IdTrustJourney.create()
    return IdTrustDialog.create(
        journey_id=journey.id,
        foil_strategy=random.choice(Strategy.choices())[0],
        user_miscommunication=user_miscommunication,
        foil_miscommunication=foil_miscommunication,
    )


def interact_core(interaction, blind, user_intent, user_guess=None):
    foil_intent = impl(interaction.foil_strategy)(
            [e.user_effect for e in interaction.idtrustexchange_set])
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
    }
