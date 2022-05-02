from ..dbconfig import get_db
from datetime import datetime
from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError

hasher = bcrypt.using(rounds=12)

db = get_db()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False)
    password = db.Column(db.String())
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, username, password=None, date_created=None):
        if not username:
            raise IntegrityError('Username cannot be null', None, None)
        db.Model.__init__(self, username=username, date_created=date_created)
        self.set_password(password)
        
    def set_password(self, password):
        self.password = hasher.hash(password)

    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def authenticate(self, password):
        return hasher.verify(password, self.password)
