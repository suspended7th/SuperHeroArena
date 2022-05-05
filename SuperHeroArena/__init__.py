from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from dotenv import load_dotenv

load_dotenv()
       
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
        app.config.from_mapping(test_config)
        
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    from . import dbconfig
    app.app_context().push()
    dbconfig.init_db()
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from .models.user import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    from .views import auth, superHeroApi
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(superHeroApi.bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
