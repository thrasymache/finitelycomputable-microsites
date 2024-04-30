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

