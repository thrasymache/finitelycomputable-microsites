try:
    from falcon import testing
    import re
    import pytest

    from finitelycomputable.falcon_addroute import application


    @pytest.fixture
    def client():
        return testing.TestClient(application)


    def test_wsgi_info(client):
        response = client.simulate_get('/wsgi_info/')
        assert 200 == response.status_code
        assert len(response.text) > 85
        assert len(response.text) < 100

    def test_helloworld(client):
        response = client.simulate_get('/hello_world/')
        assert 200 == response.status_code
        assert re.search('says "hello, world"\n', response.text)
        assert re.search('Falcon', response.text)
except ImportError:
    pass
