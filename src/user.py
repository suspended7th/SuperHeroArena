

class User(db.Model):
    def __init__(self, db):
        self.id = db.Column(db.Integer, primary_key=True)
        self.username = db.Column(db.String(20), nullable=False)
        self.password = db.Column(db.String(20), nullable=False)
        self.date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id