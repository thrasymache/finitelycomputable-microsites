import pytest

from finitelycomputable import flask_blueprints


@pytest.fixture
def client():
        flask_blueprints.application.config['TESTING'] = True

        with flask_blueprints.application.test_client() as client:
            yield client


def test_wsgi_info(client):
    response = client.get('/wsgi_info/')
    assert 200 == response.status_code
    assert len(response.data) > 100
    assert len(response.data) < 115

def test_helloworld(client):
    '''helloworld test that can handle adapters'''
    response = client.get('/hello_world/')
    assert 200 == response.status_code
    assert len(response.data) > 21
    assert len(response.data) < 30

