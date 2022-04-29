from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Task %r>' % self.id

db.create_all()

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')
    
@app.route('/usermanagement/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def user_mamagement():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        try:
            db.session.add(user)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding the user"
    else:
        users = User.query.order_by(User.date_created).all()
        return render_template('usermanagement.html', users=users)

if __name__ == "__main__":
    app.run(debug=True)