import flask

def new_dialogue(blind, journey_id=None):
    return flask.url_for(
        'idtrust.new_dialogue',
        blind=blind,
        journey_id=journey_id,
    )

def interact(pk, blind):
    return flask.url_for(
        'idtrust.interact',
        pk=pk,
        blind=blind,
    )
