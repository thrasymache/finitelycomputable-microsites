import pytest
from webtest import TestApp as Client

from finitelycomputable.helloworld_morepath import application

def test_helloworld_morepath():
    '''helloworld test that can handle adapters'''
    c = Client(application)
    response = c.get('/')
    assert 200 == response.status_code
    assert len(response.body) > 21
    assert len(response.body) < 30

@pytest.mark.xfail
def test_helloworld_morepath_exact():
    '''helloworld test for exact text'''
    c = Client(application)
    response = c.get('/')
    assert 200 == response.status_code
    assert response.body == b'Morepath says "hello, world"\n'
