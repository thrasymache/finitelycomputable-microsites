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


def home(request):
    context = {
        'interaction_pk': 1+
            (Interaction.objects.all().aggregate(Max('pk'))['pk__max'] or 0),
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
    user_list = [i.user_trust for i in interaction.exchange_set.all()]
    foil_list = [i.foil_trust for i in interaction.exchange_set.all()]
    strategy_lists = OrderedDict()
    if len(user_list):
        for (k, v) in Strategy.choices:
            st = Strategy.impl(k)
            strategy_lists[v] = [deviation(user_list, foil_list, st)]
            strategy_lists[v].append(deviation(foil_list, user_list, st))
    s_results = [
            "%s: (foil %.1f) (user %.1f)" %
            (k, v[0], v[1]) for (k, v) in strategy_lists.items()]
    score = interaction.score()
    user_list_display = ", ".join(
            ["Trust" if t else "Distrust" for t in user_list])
    foil_list_display = ", ".join(
            ["Trust" if t else "Distrust" for t in foil_list])
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


class ExchangeCreate(CreateView):
    model = Exchange
    fields = ['interaction', 'foil_trust', 'user_trust']
    template_name = "id_trust/interaction_begin.html"

    def form_valid(self, form):
        #form.foil_strategy = random.choice(Strategy.choices)[0]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('id_trust:reveal_interact',
                       kwargs={'pk': self.object.interaction_id})


class Home(CreateView):
    model = Interaction
    fields = []#'foil_strategy']
    template_name_suffix = "_begin"

    def form_valid(self, form):
        #form.foil_strategy = random.choice(Strategy.choices)[0]
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('id_trust:real_interact',
                       kwargs={'pk': self.object.pk})


class RevealInteract(DetailView):
    template_name = 'id_trust/reveal_interaction.html'
    fields = ['choice']
    model = Interaction

    def get_context_data(self, **kwargs):
        context = super(RevealInteract, self).get_context_data(**kwargs)
        #(interaction, created) = Interaction.objects.get_or_create(
        #        {'foil_strategy': random.choice(Strategy.choices)[0]},
        #        pk=pk)
        # import ipdb; ipdb.set_trace()
        foil_response = Strategy.impl(interaction.foil_strategy)(
                [e.user_trust for e in self.object.exchange_set.all()])
        user_trust = self.request.POST.get('choice')
        if user_trust == 'Trust':
            user_trust = True
        elif user_trust == 'Distrust':
            user_trust = False
        if user_trust in [True, False]:
            self.object.exchange_set.create(
                    user_trust=user_trust,
                    foil_trust=foil_response)
        user_list = [i.user_trust for i in self.object.exchange_set.all()]
        foil_list = [i.foil_trust for i in self.object.exchange_set.all()]
        strategy_lists = OrderedDict()
        if len(user_list):
            for (k, v) in Strategy.choices:
                st = Strategy.impl(k)
                strategy_lists[v] = [deviation(user_list, foil_list, st)]
                strategy_lists[v].append(deviation(foil_list, user_list, st))
        s_results = [
                "%s: (foil %.1f) (user %.1f)" %
                (k, v[0], v[1]) for (k, v) in strategy_lists.items()]
        score = self.object.score()
        user_list_display = ", ".join(
                ["Trust" if t else "Distrust" for t in user_list])
        foil_list_display = ", ".join(
                ["Trust" if t else "Distrust" for t in foil_list])
        context.update({
            'interaction_pk': self.object.pk,
            'interaction': self.object,
            'score': score,
            'user_list': user_list_display,
            'foil_list': foil_list_display,
            's_results': s_results,
        })
        return context


class Interact(UpdateView, RevealInteract):
    template_name = 'id_trust/real_interaction.html'

    def get_success_url(self):
        return reverse('id_trust:real_interact',
                       kwargs={'pk': self.object.pk})
