try:
    import pytest

    from finitelycomputable import idtrust_flask
    from finitelycomputable.idtrust_db.models import (
        SqliteDatabase, IdTrustJourney, IdTrustDialog, IdTrustExchange, MODELS
    )
    from finitelycomputable.idtrust_common.strategies import Strategy

    test_db = SqliteDatabase(':memory:')

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


    @pytest.fixture
    def client():
            idtrust_flask.application.config['TESTING'] = True

            # Bind model classes to test db. Since we have a complete list of
            # all models, we do not need to recursively bind dependencies.
            test_db.bind(MODELS, bind_refs=False, bind_backrefs=False)

            # test_db.connect()
            test_db.create_tables(MODELS)
            IdTrustJourney.create(id=1)

            with idtrust_flask.application.test_client() as client:
                yield client
            test_db.drop_tables(MODELS)
            test_db.close()


    def test_get_blind_begin_200(client):
        # response = client.get('/identification_of_trust/')
        response = client.get('/')
        assert 200 == response.status_code

    def test_get_reveal_begin_200(client):
        # response = client.get('/identification_of_trust/choose_miscommunication')
        response = client.get('/choose_miscommunication')
        assert 200 == response.status_code

    def test_get_interact_404(client):
        # response = client.get('/identification_of_trust/interact/1')
        response = client.get('/interact/4')
        assert 404 == response.status_code

    def test_get_interact_200(client, dialog):
        # response = client.get('/identification_of_trust/interact/1')
        response = client.get('/interact/1')
        assert 200 == response.status_code

    def test_get_blind_continue_404(client):
        # response = client.get('/identification_of_trust/journey/2')
        response = client.get('/journey/2')
        assert 404 == response.status_code

    def test_get_blind_continue_200(client, dialog):
        # response = client.get('/identification_of_trust/journey/2')
        response = client.get('/journey/2')
        assert 200 == response.status_code

    def test_get_reveal_continue_404(client):
        response = client.get(
                #'/identification_of_trust/journey/2/choose_miscommunication')
                '/journey/2/choose_miscommunication')
        assert 404 == response.status_code

    def test_get_reveal_continue_200(client, dialog):
        response = client.get(
                #'/identification_of_trust/journey/2/choose_miscommunication')
                '/journey/2/choose_miscommunication')
        assert 200 == response.status_code

    def test_post_blind_begin_creates_interaction(client):
        assert IdTrustDialog.select().count() == 0
        # response = client.post('/identification_of_trust/',
        response = client.post('/',
                data={'user_intent': 'Trust'})
        assert response.status_code == 302
        assert IdTrustDialog.select().count() == 1

    def test_post_reveal_begin_creates_interaction(client):
        assert IdTrustDialog.select().count() == 0
        response = client.post(
            #'/identification_of_trust/journey/1/choose_miscommunication', {
            '/journey/1/choose_miscommunication', data={
                'user_intent': 'Trust',
                'user_miscommunication': 0.1,
                'foil_miscommunication': 0.1, })
        assert response.status_code == 302
        assert IdTrustDialog.select().count() == 1

    def test_post_blind_continue_creates_interaction(client):
        assert IdTrustDialog.select().count() == 0
        #response = client.post('/identification_of_trust/journey/1',
        response = client.post('/journey/1',
                data={'user_intent': 'Trust'})
        assert response.status_code == 302
        assert IdTrustDialog.select().count() == 1

    def test_post_reveal_continue_creates_interaction(client):
        assert IdTrustDialog.select().count() == 0
        #response = client.post('/identification_of_trust/', {
        response = client.post('/', data={
            'user_intent': 'Trust',
            'user_miscommunication': 0.1,
            'foil_miscommunication': 0.1,
        })
        assert response.status_code == 302
        assert IdTrustDialog.select().count() == 1

    def test_post_trust_creates_exchange(client, dialog):
        assert IdTrustExchange.select().count() == 0
        #response = client.post('/identification_of_trust/interact/1',
        response = client.post('/interact/1',
                data={'user_intent': 'Trust'})
        assert response.status_code == 200
        assert IdTrustExchange.select().count() == 1

    def test_post_distrust_creates_exchange(client, dialog):
        assert IdTrustExchange.select().count() == 0
        #response = client.post('/identification_of_trust/interact/1',
        response = client.post('/interact/1',
                data={'user_intent': 'Distrust'})
        print(response.data)
        assert response.status_code == 200
        assert IdTrustExchange.select().count() == 1

    def test_post_user_guess_sets_user_guess(client, dialog):
        assert IdTrustExchange.select().count() == 0
        #response = client.post('/identification_of_trust/interact/1',
        response = client.post('/interact/1',
                data={'user_guess': Strategy.Innocent.value})
        print(response.data)
        assert response.status_code == 200
        assert IdTrustExchange.select().count() == 0
        assert IdTrustDialog.get(id=1).user_guess == Strategy.Innocent.value

except ImportError:
    pass
