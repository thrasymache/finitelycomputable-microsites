from falcon import testing
import re
import pytest

from finitelycomputable.helloworld_falcon import application


@pytest.fixture()
def client():
    return testing.TestClient(application)

def test_helloworld_falcon(client):
    '''helloworld test that can handle adapters'''
    response = client.simulate_get('/')
    assert 200 == response.status_code
    assert re.search('says "hello, world"\n', response.text)
    assert re.search('Falcon', response.text)

@pytest.mark.xfail
def test_helloworld_falcon_exact(client):
    '''helloworld test for exact text'''
    response = client.simulate_get('/')
    assert 200 == response.status_code
    assert response.text == 'Falcon says "hello, world"\n'
