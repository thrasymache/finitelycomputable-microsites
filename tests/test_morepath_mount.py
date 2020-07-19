import pytest
from webtest import TestApp as Client

from finitelycomputable.morepath_mount import application


def test_wsgi_info():
    c = Client(application)
    response = c.get('/wsgi_info/')
    assert 200 == response.status_code
    assert len(response.text) > 85
    assert len(response.text) < 100

def test_helloworld_morepath():
    '''helloworld test that can handle adapters'''
    c = Client(application)
    response = c.get('/hello_world/')
    assert 200 == response.status_code
    assert len(response.body) > 21
    assert len(response.body) < 30
