import pytest
from finitelycomputable.idtrust_db.models import (
    SqliteDatabase, IdTrustJourney, IdTrustDialog, IdTrustExchange, MODELS
)
from finitelycomputable.idtrust_common.strategies import Strategy


db_for_tests = SqliteDatabase(':memory:')

@pytest.fixture
def db():
    # Bind model classes to test db. Since we have a complete list of
    # all models, we do not need to recursively bind dependencies.
    db_for_tests.bind(MODELS, bind_refs=False, bind_backrefs=False)

    # db_for_tests.connect()
    db_for_tests.create_tables(MODELS)
    IdTrustJourney.create(id=1)
    yield db_for_tests
    db_for_tests.drop_tables(MODELS)
    db_for_tests.close()


@pytest.fixture
def journey():
    return IdTrustJourney.create(id=2)


@pytest.fixture
def dialog(journey):
    return IdTrustDialog.create(
        id=1,
        journey_id=journey.id,
        foil_strategy='C',
        user_miscommunication=0.0,
        foil_miscommunication=0.0,
    )

def assert_no_dialogs_or_exchanges():
    assert IdTrustDialog.select().count() == 0
    assert IdTrustExchange.select().count() == 0

def assert_one_dialog_no_exchanges():
    assert IdTrustDialog.select().count() == 1
    assert IdTrustExchange.select().count() == 0

def assert_one_dialog_and_trust_exchange():
    assert IdTrustDialog.select().count() == 1
    assert IdTrustExchange.select().count() == 1
    assert IdTrustExchange.get(id=1).user_intent == True

def assert_one_dialog_and_distrust_exchange():
    assert IdTrustDialog.select().count() == 1
    assert IdTrustExchange.select().count() == 1
    assert IdTrustExchange.get(id=1).user_intent == False

def assert_no_user_guess():
    assert IdTrustDialog.get(id=1).user_guess == ''

def assert_set_user_guess():
    assert IdTrustDialog.get(id=1).user_guess == Strategy.Innocent.value
