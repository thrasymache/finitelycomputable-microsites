from datetime import datetime
from peewee import *
from finitelycomputable.idtrust_common import logic
from finitelycomputable.idtrust_common.strategies import Strategy

database = SqliteDatabase('db.sqlite3')


class BaseModel(Model):
    class Meta:
        database = database

class IdTrustJourney(BaseModel):
    start_time = DateTimeField(default=datetime.utcnow)

    def results(self):
        return logic.results(self.idtrustdialog_set)

    class Meta:
        table_name = 'id_trust_journey'

class IdTrustDialog(BaseModel):
    foil_miscommunication = FloatField()
    foil_strategy = CharField(choices=Strategy.choices())
    journey = ForeignKeyField(column_name='journey_id', field='id', model=IdTrustJourney)
    start_time = DateTimeField(default=datetime.utcnow)
    user_guess = CharField(default='', choices=Strategy.choices())
    user_miscommunication = FloatField()

    def score(self):
        return logic.score(self.idtrustexchange_set)
    def exchange_count(self):
        return len(self.idtrustexchange_set)
    def get_user_guess_display(self):
        return Strategy(self.user_guess).name
    def get_foil_strategy_display(self):
        return Strategy(self.foil_strategy).name
    def get_absolute_url(self):
        # temporarily safe reverse dependency: currently idtrust-flask-peewee
        # is the only package that needs this one, so we can expect flask to be
        # installed. This will not always be true.
        import flask
        return flask.url_for(
            'idtrust.interact',
            pk=self.id,
            blind=True,
        )

    class Meta:
        table_name = 'id_trust_dialog'

class IdTrustExchange(BaseModel):
    foil_effect = BooleanField()
    foil_intent = BooleanField()
    interaction = ForeignKeyField(column_name='interaction_id', field='id', model=IdTrustDialog)
    user_effect = BooleanField()
    user_intent = BooleanField()

    class Meta:
        table_name = 'id_trust_exchange'

MODELS = [IdTrustJourney, IdTrustDialog, IdTrustExchange]
