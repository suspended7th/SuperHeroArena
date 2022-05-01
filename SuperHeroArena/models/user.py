from .. import db
from datetime import datetime
# from password_manager import generate_hashed_password


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20))
    salt = db.Column(db.String[22])
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    # def __init__(self, username, password=None, date_created=None):
    #     db.Model.__init__(self, username=username, date_created=date_created)
    #     self.password = generate_hashed_password(self, password)
    
    def __repr__(self):
        return '<Task %r>' % self.id