from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
       
db = SQLAlchemy()

def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SQLALCHEMY_DATABASE_URI='sqlite:///main.db',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SECRET_KEY='dev'
    )
    
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_object(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import dbconfig
    app.app_context().push()
    dbconfig.init_db()
    
    from .views import usermanagement
    
    app.register_blueprint(usermanagement.bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
