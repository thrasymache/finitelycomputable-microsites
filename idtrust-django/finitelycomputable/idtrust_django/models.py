from django.db import models
from djchoices import DjangoChoices, ChoiceItem


def copy_cat(exchanges):
    return exchanges[-1] if len(exchanges) else True


def cheat(exchanges):
    return False


def innocent(exchanges):
    return True


def grudger(exchanges):
    return not [i for i in exchanges if not i]


def detective(exchanges):
    if len(exchanges) in [0, 2, 3]:
        return True
    elif len(exchanges) in [1]:
        return False
    elif [i for i in exchanges if not i]:
        return copy_cat(exchanges)
    else:
        return cheat(exchanges)


def alternate_strategy(inputs, strategy):
    result = []
    for n in range(len(inputs)+1):
        subset = inputs[:n]
        result.append(strategy.impl(subset))
    return result


def deviation(inputs, outputs, strategy):
    result = 0
    for n in range(len(inputs)):
        subset = inputs[:n]
        result += outputs[n] != strategy.impl(subset)
    return result / len(inputs)


class Strategy(DjangoChoices):
    copy_cat = ChoiceItem("C", impl=copy_cat)
    cheat = ChoiceItem("X", impl=cheat)
    innocent = ChoiceItem("I", impl=innocent)
    grudger = ChoiceItem("G", impl=grudger)
    detective = ChoiceItem("D", impl=detective)


# TODO add exchange time to the exchange models, make sure that it's
# sub-second, or have a better strategy


class Interaction(models.Model):
    start_time = models.DateTimeField(auto_now_add=True)
    foil_strategy = models.CharField(max_length=1, choices=Strategy.choices)
    #        default = 'D')

    def score(self):
        user_result = foil_result = 0
        for e in self.exchange_set.all():
            if e.user_trust and e.foil_trust:
                user_result += 2
                foil_result += 2
            elif e.user_trust:
                user_result -= 1
                foil_result += 3
            elif e.foil_trust:
                user_result += 3
                foil_result -= 1
            else:
                pass
        return user_result, foil_result


class Exchange(models.Model):
    interaction = models.ForeignKey(Interaction, on_delete=models.CASCADE)
    user_trust = models.BooleanField()
    foil_trust = models.BooleanField()
