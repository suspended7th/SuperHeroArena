from flask import render_template, redirect, request
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy        

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///main.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from .model import User

db.create_all()

from .view import index, usermanagement

if __name__ == "__main__":
    app.run(debug=True)