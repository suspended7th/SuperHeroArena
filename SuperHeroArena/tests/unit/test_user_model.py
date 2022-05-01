from SuperHeroArena.models.user import User
from flask_sqlalchemy import DataException
from datetime import datetime
import re

def test_new_user():
    user = User(username='test', password='test')
    # test for id 1 because this is a fresh test database
    assert user.id == 1
    assert user.username == 'test'
    assert user.date_created.date() == datetime.utcnow().date()
    # check if this matches the bcrypt standard of 60 characters
    # first 7 are version and cost info, remaining 53 are the hash and salt values
    assert re.match(r"^\$2b\$12\$[0-9a-zA-Z]{53}$", user.password)
    
def test_bad_user():
    with pytest.assertRaises(DataException):
        user = User(username=None, password='test')
