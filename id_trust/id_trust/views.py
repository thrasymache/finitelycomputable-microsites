from collections import OrderedDict
from django.db.models import Max
from django.shortcuts import render
import random

from id_trust.models import Interaction, Strategy, deviation


def home(request):
    context = {
        'interaction_pk':
            Interaction.objects.all().aggregate(Max('pk'))['pk__max']+1,
        'interaction': None,
        'score': (0, 0),
        'user_list': [],
        'foil_list': [],
        's_results': [],
    }
    return render(request, 'id_trust/real_interaction.html', context)


def interact(request, pk, secrets):
    (interaction, created) = Interaction.objects.get_or_create(
            {'foil_strategy': random.choice(Strategy.choices)[0]},
            pk=pk)
    foil_response = Strategy.get_choice(
            interaction.foil_strategy).impl(
                    [e.user_trust for e in interaction.exchange_set.all()])
    user_trust = request.POST.get('choice')
    if user_trust == 'Trust':
        user_trust = True
    elif user_trust == 'Distrust':
        user_trust = False
    if user_trust in [True, False]:
        interaction.exchange_set.create(
                user_trust=user_trust,
                foil_trust=foil_response)
    user_list = [i.user_trust for i in interaction.exchange_set.all()]
    foil_list = [i.foil_trust for i in interaction.exchange_set.all()]
    strategy_lists = OrderedDict()
    if len(user_list):
        for (k, v) in Strategy.choices:
            st = Strategy.get_choice(k)
            strategy_lists[v] = [deviation(user_list, foil_list, st)]
            strategy_lists[v].append(deviation(foil_list, user_list, st))
    s_results = [
            "%s: (foil %.1f) (user %.1f)" %
            (k, v[0], v[1]) for (k, v) in strategy_lists.items()]
    score = interaction.score()
    user_list_display = ["Trust" if t else "Distrust" for t in user_list]
    foil_list_display = ["Trust" if t else "Distrust" for t in foil_list]
    context = {
        'interaction_pk': interaction.pk,
        'interaction': interaction,
        'score': score,
        'user_list': user_list_display,
        'foil_list': foil_list_display,
        's_results': s_results,
    }
    return render(request,
            'id_trust/reveal_interaction.html' if secrets
            else 'id_trust/real_interaction.html',
            context)
