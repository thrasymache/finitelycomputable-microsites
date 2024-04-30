import re
import pytest

from finitelycomputable import idtrust_app_flask
from finitelycomputable.idtrust_common.helpers_for_tests import *
from finitelycomputable.idtrust_db.helpers_for_tests import *


@pytest.fixture
def client(db):
    idtrust_app_flask.application.config['TESTING'] = True
    return idtrust_app_flask.application.test_client()

