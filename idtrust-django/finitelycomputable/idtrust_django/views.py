from collections import OrderedDict
from django.db.models import Max
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
import random

from finitelycomputable.idtrust_django.models import (
        Interaction, Exchange, Strategy, deviation,
)

def trust_list_display(trust_list):
    return ", ".join(["Trust" if t else "Distrust" for t in trust_list])

def home(request):
    context = {
        'interaction_pk': 1+
            (Interaction.objects.all().aggregate(Max('pk'))['pk__max'] or 0),
        'interaction': None,
        'score': (0, 0),
        'user_intent': [],
        'user_appears': [],
        'foil_appears': [],
        'foil_intent': [],
        's_results': [],
    }
    return render(request, 'id_trust/interaction.html', context)


def interact_core(request, pk):
    (interaction, created) = Interaction.objects.get_or_create(
            {'foil_strategy': random.choice(Strategy.choices)[0]},
            pk=pk)
    foil_response = Strategy.impl(interaction.foil_strategy)(
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
    user_guess = request.POST.get('user_guess')
    if user_guess:
        interaction.user_guess = user_guess
        interaction.save()
    user_intent = [i.user_trust for i in interaction.exchange_set.all()]
    user_appears = user_intent
    foil_intent = [i.foil_trust for i in interaction.exchange_set.all()]
    foil_appears = foil_intent
    strategy_lists = OrderedDict()
    if len(user_intent):
        for (k, v) in Strategy.choices:
            st = Strategy.impl(k)
            strategy_lists[v] = [deviation(user_intent, foil_intent, st)]
            strategy_lists[v].append(deviation(foil_intent, user_intent, st))
    s_results = [
            "%s: (foil %.1f) (user %.1f)" %
            (k, v[0], v[1]) for (k, v) in strategy_lists.items()]
    score = interaction.score()
    return {
        'interaction_pk': interaction.pk,
        'interaction': interaction,
        'score': score,
        'user_intent': trust_list_display(user_intent),
        'user_appears': trust_list_display(user_appears),
        'foil_appears': trust_list_display(foil_appears),
        'foil_intent': trust_list_display(foil_intent),
        's_results': s_results,
        'strategies': Strategy,
    }

def interact(request, pk):
    return render(request, 'id_trust/interaction.html',
        interact_core(request, pk))


class ExchangeCreate(CreateView):
    model = Exchange
    fields = ['interaction', 'user_trust']
    template_name = "id_trust/exchange_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context

    def form_valid(self, form):
        interaction = form.instance.interaction
        form.instance.foil_trust = Strategy.impl(
            form.instance.interaction.foil_strategy)(
            [e.user_trust for e in interaction.exchange_set.all()]
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('id_trust:interact',
                       kwargs={'pk': self.object.interaction_id})


class Home(CreateView):
    model = Exchange
    fields = ['user_trust']
    template_name = "id_trust/interaction_begin.html"

    def form_valid(self, form):
        interaction = form.instance.interaction = Interaction.objects.create(
            foil_strategy = random.choice(Strategy.choices)[0]
        )
        form.instance.foil_trust = Strategy.impl(interaction.foil_strategy)(
            [e.user_trust for e in interaction.exchange_set.all()]
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('id_trust:interact',
                       kwargs={'pk': self.object.interaction_id})


class Interact(DetailView):
    template_name = 'id_trust/interaction.html'
    fields = ['choice']
    model = Interaction

    def get_context_data(self, **kwargs):
        context = super(Interact, self).get_context_data(**kwargs)
        context.update(interact_core(self.request, self.object.pk, True))
        return context
