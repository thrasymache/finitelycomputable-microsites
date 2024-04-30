import re
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
    c = Client(application)
    response = c.get('/hello_world/')
    assert 200 == response.status_code
    assert re.search('says "hello, world"\n', response.text)
    assert re.search('Morepath', response.text)
