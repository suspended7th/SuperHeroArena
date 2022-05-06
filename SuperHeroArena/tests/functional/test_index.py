import pytest

@pytest.fixture()
def app(app_setup):
    yield app_setup
    
def test_index(app, client):
    response = client.get('/')
    assert response.status_code == 200