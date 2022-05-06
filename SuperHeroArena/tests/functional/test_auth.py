import pytest
from flask_login import current_user
from SuperHeroArena import dbconfig
from SuperHeroArena.models.user import User

# Ensure that the database is clean after each test
@pytest.fixture()
def app(app_setup):
    yield app_setup
    dbconfig.db.session.rollback()
    User.query.delete()

def test_new_user_endpoints(app, client):
    db = dbconfig.get_db()
    
    # Test that the endpoint functions properly
    response = client.get('/logout/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
    assert client.get('/login/').status_code == 200
    assert client.get('/signup/').status_code == 200
    response = client.get('/profile/')
    assert response.status_code == 302
    assert '/login' in response.headers['Location']
    
    # Test that a user can be added to the system
    response = client.post(
        '/signup/',
        data = {
            'username': 'functional',
            'password': 'functional',
            'email': 'func@test.com'
        }
    )
    assert response.status_code == 302
    data = str(client.get(response.headers['Location']).data)
    assert 'functional' in data
    assert 'func@test.com' in data
    
    # get the user form the database to use the set values in the rest of the tests
    user = User.query.filter(User.username=='functional').first()
    
    # Test that user creation fails if data is not provided
    response = client.post(
        '/signup/',
        data = {
            'username': '',
            'password': '',
            'email': ''
        }
    )
    assert response.status_code == 302
    data = str(client.get(response.headers['Location']).data)
    assert 'Username is required' in data
    assert 'Password is required' in data
    assert 'Email is required' in data
    
    # Test that the user can be retrieved
    response = client.get('/profile/')
    data = str(response.data)
    assert response.status_code == 200
    assert 'functional' in data
    assert 'func@test.com' in data
    
    # Test that the user can be updated
    response = client.post(
        '/profile/',
        data = {
            'username': 'update',
            'old_password': '',
            'new_password': '',
            'email': 'up@test.com'
        }
    )
    assert response.status_code == 200
    data = str(response.data)
    assert 'functional' not in data
    assert 'update' in data
    assert 'up@test.com' in data
    
    # Test that the password was not changed
    response = client.get('/logout/')
    assert response.status_code == 302
    assert response.headers['Location'] == '/login/'
    
    assert client.get('/profile/').status_code == 302
    
    response = client.post(
        '/login/', 
        data = {
            'username': 'update',
            'password': 'functional'
        }
    )
    assert response.status_code == 302
    assert response.headers['Location'] == '/profile/'
    
    # Test that the password can be changed
    response = client.post(
        '/profile/',
        data = {
            'username': 'updated',
            'old_password': 'functional',
            'new_password': 'updated',
            'email': 'upd@test.com'
        }
    )
    
    assert response.status_code == 200
    data = str(response.data)
    assert 'functional' not in data
    assert 'updated' in data
    assert 'upd@test.com' in data
    
    # Test that the password was changed
    response = client.get('/logout/')
    assert response.status_code == 302
    assert response.headers['Location'] == '/login/'
    
    assert client.get('/profile/').status_code == 302
    
    response = client.post(
        '/login/', 
        data = {
            'username': 'updated',
            'password': 'updated'
        }
    )
    assert response.status_code == 302
    assert response.headers['Location'] == '/profile/'
    
    # Test bad password on update
    response = client.post(
        '/profile/',
        data = {
            'username': 'functional',
            'old_password': 'functional',
            'new_password': 'updated',
            'email': 'func@test.com'
        }
    )
    
    assert response.status_code == 200
    data = str(response.data)
    assert 'functional' not in data
    assert 'updated' in data
    assert 'upd@test.com' in data
    assert 'Invalid Old Password.  User Not Updated.' in data
    
    # Test bad user credentials
    client.get('/logout/')
    response = client.post(
        '/login/',
        data = {
            'username': 'doesnotexist',
            'password': 'updated'
        }
    )
    assert response.status_code == 200
    assert 'User does not exist.  Please Create one.' in str(response.data)
    
    client.get('/logout/')
    response = client.post(
        '/login/',
        data = {
            'username': 'updated',
            'password': 'wrongpassword'
        }
    )
    assert response.status_code == 200
    assert 'Unauthenticated' in str(response.data)
