import pytest
from SuperHeroArena import dbconfig
from SuperHeroArena.models.user import User

# Ensure that the database is clean after each test
@pytest.fixture()
def app(app_setup):
    yield app_setup
    User.query.delete()

def test_new_user_endpoints(app, client):
    db = dbconfig.get_db()
    
    
    # Test that the list endpoint functions properly
    assert client.get('/usermanagement/').status_code == 200
    
    # Test that a user can be added to the system
    response = client.post(
        '/usermanagement/',
        data = {
            'username': 'functional',
            'password': 'functional'
        }
    )
    data = str(response.data)
    assert response.status_code == 200
    assert 'functional' in data
    
    # get the user form the database to use the set values in the rest of the tests
    user = User.query.filter(User.username=='functional').first()
    old_user_password = user.password
    
    # Test that user creation fails if data is not provided
    response = client.post(
        '/usermanagement/',
        data = {
            'username': '',
            'password': 'functional'
        }
    )
    data = str(response.data)
    assert response.status_code == 200
    assert 'Username is required' in data
    assert 'Password is required' not in data
    
    response = client.post(
        '/usermanagement/',
        data = {
            'username': 'functional',
            'password': ''
        }
    )
    data = str(response.data)
    assert response.status_code == 200
    assert 'Username is required' not in data
    assert 'Password is required' in data
    
    response = client.post(
        '/usermanagement/',
        data = {
            'username': '',
            'password': ''
        }
    )
    data = str(response.data)
    assert response.status_code == 200
    assert 'Username is required' in data
    assert 'Password is required' in data
    
    # Test that the user can be logged in
    response = client.post(
        '/usermanagement/{}/login/'.format(user.id),
        data = {
            'password': 'unauthenticated'
        }
    )
    data = str(response.data)
    assert response.status_code == 200
    assert 'Unauthenticated' in data
    
    response = client.post(
        '/usermanagement/{}/login/'.format(user.id),
        data = {
            'password': 'functional'
        }
    )
    assert response.status_code == 200
    assert 'Successful login' in str(response.data)
    
    # Test that the user can be retrieved by itself
    update_url = '/usermanagement/{}/'.format(user.id)
    
    response = client.get(update_url)
    data = str(response.data)
    assert response.status_code == 200
    assert 'functional' in data
    
    # Test that the user can be updated
    response = client.post(
        update_url,
        data = {
            'username': 'updated',
            'password': 'updated'
        }
    )
    assert response.status_code == 200
    data = str(response.data)
    assert 'functional' not in data
    assert 'updated' in data
    assert old_user_password not in data
    
    
    # Test that the user can be logged in after update
    response = client.post(
        update_url + 'login/',
        data = {
            'password': 'unauthenticated'
        }
    )
    assert response.status_code == 200
    assert 'Unauthenticated' in str(response.data)
    
    response = client.post(
        update_url + 'login/',
        data = {
            'password': 'updated'
        }
    )
    assert response.status_code == 200
    assert 'Successful login' in str(response.data)
    
    # Test that the user can be deleted
    old_user_password = user.password
    response = client.get(update_url + 'delete/')
    data = str(response.data)
    assert response.status_code == 200
    assert 'functional' not in data
    assert 'updated' in data
    
    response = client.post(update_url + 'delete/')
    assert response.status_code == 200
    data = str(response.data)
    assert 'functional' not in data
    assert 'updated' not in data
    assert old_user_password not in data
    
    
    # Test that endpoints return 404 if the user doesn't exist
    assert client.get(update_url).status_code == 404
    assert client.get(update_url + 'delete/').status_code == 404
    assert client.post(update_url + 'login/', data={'password': 'updated'}).status_code == 404
