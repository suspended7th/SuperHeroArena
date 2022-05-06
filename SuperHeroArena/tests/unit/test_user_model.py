from datetime import datetime
from sqlalchemy.exc import IntegrityError

import pytest
import re

from SuperHeroArena.models.user import User
from SuperHeroArena import dbconfig

# Ensure that the database is clean after each test
@pytest.fixture()
def app(app_setup):
    yield app_setup
    dbconfig.db.session.rollback()
    User.query.delete()

def test_new_user(app):
    user =  User(username='test', password='test', email='test@test.com')
    db = dbconfig.get_db()
    
    try:
        db.session.add(user)
        db.session.commit()
    except BaseException as err:
        print("There was an issue adding the user\n" + str(err))
    
    user = User.query.filter(User.username=='test').first()
    
    assert str(user) == '<User test>'
    # test for id 1 because this is a fresh test database
    assert user.id == 1
    assert user.username == 'test'
    assert user.date_created.date() == datetime.utcnow().date()
    assert user.email == 'test@test.com'
    # check if this matches the bcrypt standard of 60 characters
    # first 7 are version and cost info, remaining 53 are the hash and salt values
    assert re.match(r"^\$2b\$12\$[0-9a-zA-Z./]{53}$", user.password)
    
    # Test that the authenticate method works
    assert user.authenticate('test')
    
def test_bad_user(app):
    db = dbconfig.get_db()
    db.session.commit()
    db.session.flush()
    
    # Test that missing data causes errors
    with pytest.raises(IntegrityError):
        user = User(username=None, password='test', email='test@test.com')
        db.session.add(user)
        db.session.commit()
        db.session.flush()
    db.session.rollback()
    with pytest.raises(IntegrityError):
        user = User(username='test', password=None, email='test@test.com')
        db.session.add(user)
        db.session.commit()
        db.session.flush()
    db.session.rollback()
    with pytest.raises(IntegrityError):
        user = User(username='test', password='test', email=None)
        db.session.add(user)
        db.session.commit()
        db.session.flush()
    db.session.rollback()
    
    # Ensure that no bad users were added to the database
    assert len(User.query.all()) == 0
        
    # Test that duplicate data throws errors
    user =  User(username='test', password='test', email='test@test.com')
    try:
        db.session.add(user)
        db.session.commit()
    except BaseException as err:
        print("There was an issue adding the user\n" + str(err))
    with pytest.raises(IntegrityError):
        user = User(username='test', password='test', email='test2@test.com')
        db.session.add(user)
        db.session.commit()
        db.session.flush()
    db.session.rollback()
    with pytest.raises(IntegrityError):
        user = User(username='test2', password='test', email='test@test.com')
        db.session.add(user)
        db.session.commit()
        db.session.flush()
