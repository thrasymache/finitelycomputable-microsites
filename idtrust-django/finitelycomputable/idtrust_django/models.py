from django.db import models
from django.urls import reverse
from finitelycomputable.idtrust_common import logic
from finitelycomputable.idtrust_common.strategies import Strategy


# TODO add exchange time to the exchange models, make sure that it's
# sub-second, or have a better strategy


class Journey(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)

    def results(self):
        return logic.results(self.dialog_set.all())

class Dialog(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    journey = models.ForeignKey(Journey, on_delete=models.CASCADE)
    foil_strategy = models.CharField(choices=Strategy.choices(), max_length=1)
    user_miscommunication  = models.FloatField()
    foil_miscommunication  = models.FloatField()
    user_guess = models.CharField(choices=Strategy.choices(), max_length=1,
            blank=True)

    def score(self):
        return logic.score(self.exchange_set.all())

    def exchange_count(self):
        return self.exchange_set.count()

    def get_absolute_url(self):
        return reverse('id_trust:blind_interact', kwargs={'pk': self.pk})


class Exchange(models.Model):
    interaction = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    user_intent = models.BooleanField()
    user_effect = models.BooleanField()
    foil_intent = models.BooleanField()
    foil_effect = models.BooleanField()
