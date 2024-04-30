import re
import pytest

from finitelycomputable import helloworld_flask


@pytest.fixture
def client():
        helloworld_flask.application.config['TESTING'] = True

        with helloworld_flask.application.test_client() as client:
            yield client


def test_helloworld_flask(client):
    '''helloworld test that can handle adapters'''
    response = client.get('/')
    assert 200 == response.status_code
    assert re.search(b'says "hello, world"\n', response.data)
    assert re.search(b'Flask', response.data)

@pytest.mark.xfail
def test_helloworld_flask_exact(client):
    '''helloworld test for exact text'''
    response = client.get('/')
    assert 200 == response.status_code
    assert response.data == b'Flask says "hello, world"\n'
