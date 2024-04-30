import re
import pytest
from webtest import TestApp as Client

from finitelycomputable.helloworld_morepath import application

def test_helloworld_morepath():
    '''helloworld test that can handle adapters'''
    c = Client(application)
    response = c.get('/')
    assert 200 == response.status_code
    assert re.search('says "hello, world"\n', response.text)
    assert re.search('Morepath', response.text)

@pytest.mark.xfail
def test_helloworld_morepath_exact():
    '''helloworld test for exact text'''
    c = Client(application)
    response = c.get('/')
    assert 200 == response.status_code
    assert response.text == 'Morepath says "hello, world"\n'
