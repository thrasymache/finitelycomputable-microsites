from falcon import testing, MEDIA_URLENCODED
import re
import pytest

from finitelycomputable.idtrust_app_falcon import application
from finitelycomputable.idtrust_common.helpers_for_tests import *
from finitelycomputable.idtrust_db.helpers_for_tests import *


class Client(object):
    def __init__(self, application):
        self.base = testing.TestClient(application)
    def get(self, url):
        return self.base.get(url)
    def post(self, url, data=None):
        body = '&'.join([f'{key}={value}' for key, value in data.items()])
        return self.base.post(url, body=body, content_type=MEDIA_URLENCODED)

@pytest.fixture
def client(db):
    return Client(application)

def test_get_blind_begin_200(client):
    assert_no_dialogs_or_exchanges()
    response = client.get(home_blind_url)
    assert 200 == response.status_code
    assert_no_dialogs_or_exchanges()
    assert re.search('<a href="/choose_miscommunication">', response.text)

def test_get_reveal_begin_200(client):
    assert_no_dialogs_or_exchanges()
    response = client.get(home_reveal_url)
    assert 200 == response.status_code
    assert_no_dialogs_or_exchanges()
    assert re.search('<a href="/">', response.text)

def test_get_interaction_404(client):
    assert_no_dialogs_or_exchanges()
    response = client.get(interaction_url)
    assert 404 == response.status_code
    assert_no_dialogs_or_exchanges()

def test_get_interaction_200(client, dialog):
    assert_one_dialog_no_exchanges()
    response = client.get(interaction_url)
    assert 200 == response.status_code
    assert_one_dialog_no_exchanges()
    assert re.search('<a href="/">', response.text)
    assert re.search('<a href="/journey/2">', response.text)

def test_get_interaction_reveal_404(client):
    assert_no_dialogs_or_exchanges()
    response = client.get(interaction_reveal_url)
    assert 404 == response.status_code
    assert_no_dialogs_or_exchanges()

def test_get_interaction_reveal_200(client, dialog):
    assert_one_dialog_no_exchanges()
    response = client.get(interaction_reveal_url)
    assert 200 == response.status_code
    assert_one_dialog_no_exchanges()
    assert re.search('<a href="/choose_miscommunication">', response.text)
    assert re.search('<a href="/journey/2/choose_miscommunication">',
            response.text)

def test_get_journey_2_blind_404(client):
    assert_no_dialogs_or_exchanges()
    response = client.get(journey_2_blind_url)
    assert 404 == response.status_code
    assert_no_dialogs_or_exchanges()

def test_get_journey_2_blind_200(client, dialog):
    assert_one_dialog_no_exchanges()
    response = client.get(journey_2_blind_url)
    assert 200 == response.status_code
    assert_one_dialog_no_exchanges()
    assert re.search('<a href="/journey/2/choose_miscommunication">',
            response.text)

def test_get_journey_2_reveal_404(client):
    assert_no_dialogs_or_exchanges()
    response = client.get(journey_2_reveal_url)
    assert 404 == response.status_code
    assert_no_dialogs_or_exchanges()

def test_get_journey_2_reveal_200(client, dialog):
    assert_one_dialog_no_exchanges()
    response = client.get(journey_2_reveal_url)
    assert 200 == response.status_code
    assert_one_dialog_no_exchanges()
    assert re.search('<a href="/journey/2">', response.text)

def test_post_home_blind_trust_creates_interaction(client):
    assert_no_dialogs_or_exchanges()
    response = client.post(home_blind_url, data=trust_data)
    assert response.status_code == 302
    assert_one_dialog_and_trust_exchange()
    assert response.headers['Location'] == '/interact/1'

def test_post_home_blind_distrust_creates_interaction(client):
    assert_no_dialogs_or_exchanges()
    response = client.post(home_blind_url, data=distrust_data)
    assert response.status_code == 302
    assert_one_dialog_and_distrust_exchange()
    assert response.headers['Location'] == '/interact/1'

def test_post_home_reveal_trust_creates_dialog(client):
    assert_no_dialogs_or_exchanges()
    response = client.post(home_reveal_url, data=reveal_trust_data)
    assert response.status_code == 302
    assert_one_dialog_and_trust_exchange()
    assert response.headers['Location'] == \
        '/interact/1/reveal_miscommunication'

def test_post_home_blind_reveal_distrust_creates_dialog(client):
    assert_no_dialogs_or_exchanges()
    response = client.post(home_blind_url, data=reveal_distrust_data)
    assert response.status_code == 302
    assert_one_dialog_and_distrust_exchange()
    assert response.headers['Location'] == '/interact/1'

def test_post_home_blind_reveal_trust_creates_dialog(client):
    assert_no_dialogs_or_exchanges()
    response = client.post(home_blind_url, data=reveal_trust_data)
    assert response.status_code == 302
    assert_one_dialog_and_trust_exchange()
    assert response.headers['Location'] == '/interact/1'

def test_post_home_reveal_distrust_creates_dialog(client):
    assert_no_dialogs_or_exchanges()
    response = client.post(home_reveal_url, data=reveal_distrust_data)
    assert response.status_code == 302
    assert_one_dialog_and_distrust_exchange()
    assert response.headers['Location'] == \
        '/interact/1/reveal_miscommunication'

def test_post_journey_reveal_trust_creates_dialog(client):
    assert_no_dialogs_or_exchanges()
    response = client.post(journey_reveal_url, data=reveal_trust_data)
    assert response.status_code == 302
    assert_one_dialog_and_trust_exchange()
    assert response.headers['Location'] == \
        '/interact/1/reveal_miscommunication'

def test_post_journey_reveal_distrust_creates_dialog(client):
    assert_no_dialogs_or_exchanges()
    response = client.post(journey_reveal_url, data=reveal_distrust_data)
    assert response.status_code == 302
    assert_one_dialog_and_distrust_exchange()
    assert response.headers['Location'] == \
        '/interact/1/reveal_miscommunication'

def test_post_journey_blind_trust_creates_dialog(client):
    assert_no_dialogs_or_exchanges()
    response = client.post(journey_blind_url, data=trust_data)
    assert response.status_code == 302
    assert_one_dialog_and_trust_exchange()
    assert response.headers['Location'] == '/interact/1'

def test_post_journey_blind_distrust_creates_dialog(client):
    assert_no_dialogs_or_exchanges()
    response = client.post(journey_blind_url, data=distrust_data)
    assert response.status_code == 302
    assert_one_dialog_and_distrust_exchange()
    assert response.headers['Location'] == '/interact/1'

def test_post_interaction_trust_creates_exchange(client, dialog):
    assert_one_dialog_no_exchanges()
    response = client.post(interaction_url, data=trust_data)
    assert response.status_code == 200
    assert_one_dialog_and_trust_exchange()
    assert re.search('<a href="/">', response.text)
    assert re.search('<a href="/journey/2">', response.text)

def test_post_interaction_distrust_creates_exchange(client, dialog):
    assert_one_dialog_no_exchanges()
    response = client.post(interaction_url, data=distrust_data)
    assert response.status_code == 200
    assert_one_dialog_and_distrust_exchange()
    assert re.search('<a href="/">', response.text)
    assert re.search('<a href="/journey/2">', response.text)

def test_post_interaction_user_guess_sets_user_guess(client, dialog):
    assert_one_dialog_no_exchanges()
    assert_no_user_guess()
    response = client.post(interaction_url, data=user_guess_data)
    assert response.status_code == 200
    assert_one_dialog_no_exchanges()
    assert_set_user_guess()
    assert re.search('<a href="/">', response.text)
    assert re.search('<a href="/journey/2">', response.text)

def test_post_interaction_reveal_trust_creates_exchange(client, dialog):
    assert_one_dialog_no_exchanges()
    response = client.post(interaction_reveal_url, data=trust_data)
    assert response.status_code == 200
    assert_one_dialog_and_trust_exchange()
    assert re.search('<a href="/choose_miscommunication">', response.text)
    assert re.search('<a href="/journey/2/choose_miscommunication">',
            response.text)

def test_post_interaction_reveal_distrust_creates_exchange(client, dialog):
    assert_one_dialog_no_exchanges()
    response = client.post(interaction_reveal_url, data=distrust_data)
    assert response.status_code == 200
    assert_one_dialog_and_distrust_exchange()
    assert re.search('<a href="/choose_miscommunication">', response.text)
    assert re.search('<a href="/journey/2/choose_miscommunication">',
            response.text)

def test_post_interaction_reveal_user_guess_sets_user_guess(client, dialog):
    assert_one_dialog_no_exchanges()
    assert_no_user_guess()
    response = client.post(interaction_reveal_url, data=user_guess_data)
    assert response.status_code == 200
    assert_one_dialog_no_exchanges()
    assert_set_user_guess()
    assert re.search('<a href="/choose_miscommunication">', response.text)
    assert re.search('<a href="/journey/2/choose_miscommunication">',
            response.text)
