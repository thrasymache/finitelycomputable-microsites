try:
    from falcon import testing
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
        '''helloworld test that can handle adapters'''
        response = client.simulate_get('/hello_world/')
        assert 200 == response.status_code
        assert len(response.text) > 21
        assert len(response.text) < 30
except ImportError:
    pass
