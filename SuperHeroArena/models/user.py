from .. import db
from datetime import datetime
from passlib.hash import bcrypt

hasher = bcrypt.using(rounds=12)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20))
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __init__(self, username, password=None, date_created=None):
        db.Model.__init__(self, username=username, date_created=date_created)
        self.password = hasher.hash(password)

    
    def __repr__(self):
        return '<User {}>'.format(self.username)

    def authenticate(self, password):
        return hasher.verify(password, self.password)
