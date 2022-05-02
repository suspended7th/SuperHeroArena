import pytest

from SuperHeroArena.models.user import User
from SuperHeroArena import dbconfig
from sqlalchemy.exc import IntegrityError
from datetime import datetime
import re

# Ensure that the database is clean after each test
@pytest.fixture()
def app(app_setup):
    yield app_setup
    User.query.delete()

def test_new_user(app):
    user =  User(username='test', password='test')
    db = dbconfig.get_db()
    
    print(user)
    print(user.id)
    print(user.username)
    print(user.password)
    print(user.date_created)
    
    try:
        db.session.add(user)
        db.session.commit()
    except BaseException as err:
        print("There was an issue adding the user\n" + str(err))
    
    user = User.query.filter(User.username=='test').first()
    print(user)
    print(user.id)
    print(user.username)
    print(user.password)
    print(user.date_created)
    
    assert str(user) == '<User test>'
    # test for id 1 because this is a fresh test database
    assert user.id == 1
    assert user.username == 'test'
    assert user.date_created.date() == datetime.utcnow().date()
    # check if this matches the bcrypt standard of 60 characters
    # first 7 are version and cost info, remaining 53 are the hash and salt values
    assert re.match(r"^\$2b\$12\$[0-9a-zA-Z./]{53}$", user.password)
    
def test_bad_user(app):
    with pytest.raises(IntegrityError):
        user = User(username=None, password='test')
