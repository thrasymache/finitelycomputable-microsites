import re
import pytest

from finitelycomputable import flask_dispatcher


@pytest.fixture
def client():
        flask_dispatcher.application.config['TESTING'] = True

        with flask_dispatcher.application.test_client() as client:
            yield client


def test_wsgi_info(client):
    response = client.get('/wsgi_info/')
    assert 200 == response.status_code
    assert len(response.data) > 85
    assert len(response.data) < 100

def test_helloworld(client):
    '''helloworld test that can handle adapters'''
    response = client.get('/hello_world/')
    assert 200 == response.status_code
    assert re.search(b'says "hello, world"\n', response.data)
    assert re.search(b'Flask', response.data)
