from collections import OrderedDict
from django.db.models import Max
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.views.generic.base import TemplateView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView
import random

from finitelycomputable.idtrust_django.models import (
        Journey, Dialog, Exchange
)
from finitelycomputable.idtrust_common.strategies import (
    effect, pct_deviation, impl, trust_list_display, Strategy
)


from django.urls import reverse

from jinja2 import Environment


def DjangoEnvironment(**options):
    env = Environment(**options)
    env.globals.update({
        # this is where I had url and reverse, when the templates used them
    })
    return env

def new_dialogue(request, blind=True, journey_id=None):
    if journey_id is not None:
        journey = get_object_or_404(Journey, pk=journey_id)
    else:
        journey = None
    if request.method != 'POST':
        if journey_id is not None:
            blind_toggle_url = reverse(
               'id_trust:reveal_continue' if blind else 'id_trust:blind_continue',
               kwargs={'journey_id': journey_id},
            )
        else:
            blind_toggle_url = reverse(
               'id_trust:reveal_begin' if blind else 'id_trust:blind_begin'
            )
        return render(request, 'interaction_begin.html', {
                'blind': blind,
                'journey': journey,
                'form': None,
                'blind_toggle_url': blind_toggle_url,
        })
    try:
        user_miscommunication = float(request.POST.get('user_miscommunication'))
    except (ValueError, TypeError):
        user_miscommunication = round(random.random() / 2, 2)
    try:
        foil_miscommunication = float(request.POST.get('foil_miscommunication'))
    except (ValueError, TypeError):
        foil_miscommunication = round(random.random() / 2, 2)
    if journey_id is None:
        journey = Journey.objects.create()
    obj = Dialog.objects.create(
        journey=journey,
        foil_strategy=random.choice(Strategy.choices())[0],
        user_miscommunication=user_miscommunication,
        foil_miscommunication=foil_miscommunication,
    )
    interact_core(request, obj.id, not blind)
    return redirect(obj)


def interact_core(request, pk, blind):
    interaction = get_object_or_404(Dialog, pk=pk)
    foil_intent = impl(interaction.foil_strategy)(
            [e.user_effect for e in interaction.exchange_set.all()])
    user_intent = request.POST.get('user_intent')
    if user_intent == 'Trust':
        user_intent = True
    elif user_intent == 'Distrust':
        user_intent = False
    if user_intent in [True, False]:
        interaction.exchange_set.create(
            interaction_id=interaction.id,
            user_intent=user_intent,
            user_effect=effect(user_intent, interaction.user_miscommunication),
            foil_intent=foil_intent,
            foil_effect=effect(foil_intent, interaction.foil_miscommunication),
        )
    user_guess = request.POST.get('user_guess')
    if user_guess:
        interaction.user_guess = user_guess
        interaction.save()
    user_intent = [j.user_intent for j in interaction.exchange_set.all()]
    user_effect = [j.user_effect for j in interaction.exchange_set.all()]
    foil_intent = [j.foil_intent for j in interaction.exchange_set.all()]
    foil_effect = [j.foil_effect for j in interaction.exchange_set.all()]
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
    form_action_url = reverse(
       'id_trust:blind_interact' if blind else 'id_trust:reveal_interact',
       args=[interaction.id],
    )
    blind_toggle_url = reverse(
       'id_trust:reveal_interact' if blind else 'id_trust:blind_interact',
       args=[interaction.id],
    )
    new_partner_url = reverse(
       'id_trust:blind_continue' if blind else 'id_trust:reveal_continue',
       kwargs={'journey_id': interaction.journey_id},
    )
    new_journey_url = reverse(
       'id_trust:blind_begin' if blind else 'id_trust:reveal_begin',
    )
    return {
        'interaction': interaction,
        'user_intent': trust_list_display(user_intent),
        'user_effect': trust_list_display(user_effect),
        'foil_effect': trust_list_display(foil_effect),
        'foil_intent': trust_list_display(foil_intent),
        'blind': blind,
        'strategy_list': strategy_list,
        'strategies': Strategy,
        'blind_toggle_url': blind_toggle_url,
        'form_action_url': form_action_url,
        'new_partner_url': new_partner_url,
        'new_journey_url': new_journey_url,
    }

def interact(request, pk, blind):
    return render(request, 'interaction.html',
        interact_core(request, pk, blind))


class ExchangeCreate(CreateView):
    model = Exchange
    fields = ['interaction', 'user_intent']
    template_name = "exchange_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update(self.kwargs)
        return context

    def form_valid(self, form):
        interaction = form.instance.interaction
        form.instance.foil_trust = impl(
            form.instance.interaction.foil_strategy)(
            [e.user_intent for e in interaction.exchange_set]
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('id_trust:interact',
                       kwargs={'pk': self.object.interaction_id})


class Home(CreateView):
    model = Exchange
    fields = ['user_intent']
    template_name = "interaction_begin.html"

    def form_valid(self, form):
        interaction = form.instance.interaction = Dialog.objects.create(
            foil_strategy = random.choice(Strategy.choices())[0]
        )
        form.instance.foil_trust = impl(interaction.foil_strategy)(
            [e.user_intent for e in interaction.exchange_set]
        )
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('id_trust:interact',
                       kwargs={'pk': self.object.interaction_id})


class Interact(DetailView):
    template_name = 'interaction.html'
    fields = ['choice']
    model = Dialog

    def get_context_data(self, **kwargs):
        context = super(Interact, self).get_context_data(**kwargs)
        context.update(interact_core(self.request, self.object.pk, True))
        return context
