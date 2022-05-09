import pytest, re

from SuperHeroArena import dbconfig
from SuperHeroArena.models.user import User


@pytest.fixture()
def app(app_setup):
    yield app_setup
    dbconfig.db.session.rollback()
    User.query.delete()
    dbconfig.db.session.commit()

    
def test_battle(app, client):
    # login to access these endpoints
    response = client.post(
        '/signup/',
        data={
            'username': 'functional',
            'password': 'functional',
            'email': 'func@test.com'
        }
    )
    assert response.status_code == 302
    data = str(client.get(response.headers['Location']).data)
    assert 'functional' in data
    assert 'func@test.com' in data
    
    # Test that a battle can be started with a hero
    response = client.post(
        '/battle/',
        data={
            'hero': 'Spider-Man',
            'score': '0',
            'hp': '300'    
        }
    )
    assert response.status_code == 200
    data = str(response.data)
    assert len(re.findall(r'<img\s', data)) == 2
    assert len(re.findall(r'value=\"Spider-Man\"', data)) == 2
    
    # Test that a battle can be started with a villain
    response = client.post(
        '/battle/',
        data={
            'hero': 'Thanos',
            'score': '0',
            'hp': '300'    
        }
    )
    assert response.status_code == 200
    data = str(response.data)
    assert len(re.findall(r'<img\s', data)) == 2
    assert len(re.findall(r'value=\"Thanos\"', data)) == 2
    
