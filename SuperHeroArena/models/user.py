from datetime import datetime
from flask_login import UserMixin
from passlib.hash import bcrypt
from sqlalchemy.exc import IntegrityError

from ..dbconfig import get_db

hasher = bcrypt.using(rounds=12)

db = get_db()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(), nullable=False, unique=True)
    email = db.Column(db.String(), nullable=False, unique=True)
    password = db.Column(db.String(), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, username, email, password=None, date_created=None):
        db.Model.__init__(self, username=username, email=email, date_created=date_created)
        self.set_password(password)
        
    def set_password(self, password):
        if password:
            self.password = hasher.hash(password)
        else:
            self.password = None
    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def authenticate(self, password):
        return hasher.verify(password, self.password)
