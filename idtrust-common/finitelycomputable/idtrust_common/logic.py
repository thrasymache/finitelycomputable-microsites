def score(exchange_set):
    user_result = foil_result = 0
    for e in exchange_set:
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


def results(dialog_set):
    total_exchanges = correct_guesses = completed_dialogs = 0
    for d in dialog_set:
        if d.user_guess:
            completed_dialogs += 1
            correct_guesses += d.user_guess == d.foil_strategy
            total_exchanges += d.exchange_count()
    if not completed_dialogs:
        return {}
    return {
        'correct_guesses': correct_guesses,
        'completed_dialogs': completed_dialogs,
        'mean_exchanges':
            format(total_exchanges / completed_dialogs, ".1f"),
        'total_exchanges': total_exchanges }
