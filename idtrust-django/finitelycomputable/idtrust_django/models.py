from django.db import models
from django.urls import reverse


def alternate_strategy(inputs, strategy):
    result = []
    for n in range(len(inputs)+1):
        subset = inputs[:n]
        result.append(strategy(subset))
    return result


def pct_deviation(outputs, inputs, strategy):
    return round(100 * deviation(outputs, inputs, strategy))

def deviation(outputs, inputs, strategy):
    result = 0
    for n in range(len(inputs)):
        subset = inputs[:n]
        result += outputs[n] != strategy(subset)
    return result / len(inputs)


class Strategy(models.TextChoices):
    COPY_CAT = "C", 'copy cat'
    CHEAT = "X", 'cheat'
    INNOCENT = "I", 'innocent'
    GRUDGER = "G", 'grudger'
    DETECTIVE = "D", 'detective'

    @classmethod
    def impl(cls, enum_val):
        if enum_val == Strategy.COPY_CAT:
            return cls.copy_cat
        elif enum_val == Strategy.CHEAT:
            return cls.cheat
        elif enum_val == Strategy.INNOCENT:
            return cls.innocent
        elif enum_val == Strategy.GRUDGER:
            return cls.grudger
        elif enum_val == Strategy.DETECTIVE:
            return cls.detective
        else:
            raise KeyError(f'Unrecognized enum_val: {enum_val}')

    @classmethod
    def copy_cat(cls, exchanges):
        return exchanges[-1] if len(exchanges) else True

    @classmethod
    def cheat(cls, exchanges):
        return False

    @classmethod
    def innocent(cls, exchanges):
        return True

    @classmethod
    def grudger(cls, exchanges):
        return not [i for i in exchanges if not i]

    @classmethod
    def detective(cls, exchanges):
        if len(exchanges) in [0, 2, 3]:
            return True
        elif len(exchanges) in [1]:
            return False
        elif [i for i in exchanges if not i]:
            return cls.copy_cat(exchanges)
        else:
            return cls.cheat(exchanges)


# TODO add exchange time to the exchange models, make sure that it's
# sub-second, or have a better strategy


class Dialog(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    foil_strategy = models.CharField(choices=Strategy.choices, max_length=1)
    user_miscommunication  = models.FloatField()
    foil_miscommunication  = models.FloatField()
    user_guess = models.CharField(choices=Strategy.choices, max_length=1,
            blank=True)


    def score(self):
        user_result = foil_result = 0
        for e in self.exchange_set.all():
            if e.user_intent and e.foil_effect:
                user_result += 2
                foil_result += 2
            elif e.user_intent:
                user_result -= 1
                foil_result += 3
            elif e.foil_effect:
                user_result += 3
                foil_result -= 1
            else:
                pass
        return user_result, foil_result

    def get_absolute_url(self):
        return reverse('id_trust:blind_interact', kwargs={'pk': self.pk})


class Exchange(models.Model):
    interaction = models.ForeignKey(Dialog, on_delete=models.CASCADE)
    user_intent = models.BooleanField()
    user_effect = models.BooleanField()
    foil_intent = models.BooleanField()
    foil_effect = models.BooleanField()
