from enum import Enum, unique
import random

@unique
class Strategy(Enum):
    Copy_cat = "C"
    Cheat = "X"
    Innocent = "I"
    Grudger = "G"
    Detective = "D"

    @classmethod
    #@property
    def choices(cls):
        return [(j.value, j.name, ) for j in cls]

def impl(enum_val):
    if enum_val == Strategy.Copy_cat.value:
        return copy_cat
    elif enum_val == Strategy.Cheat.value:
        return cheat
    elif enum_val == Strategy.Innocent.value:
        return innocent
    elif enum_val == Strategy.Grudger.value:
        return grudger
    elif enum_val == Strategy.Detective.value:
        return detective
    else:
        raise KeyError(f'Unrecognized enum_val: {enum_val}')
    
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


def effect(intent, miscommunication):
    return intent ^ bool(miscommunication > random.random())

def trust_list_display(trust_list):
    return ", ".join(["Trust" if t else "Distrust" for t in trust_list])
