from flask import current_app

from . import db

import click

def get_db():
    return db

def init_db():
    db.init_app(current_app)
    from .models.user import User
    db.create_all(app=current_app)
