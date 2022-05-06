from flask_sqlalchemy import SQLAlchemy

import os
import pytest
import tempfile

import SuperHeroArena

# Fixture to set up the app and database for use in all tests.  
# Should be configured per test module to clean the database
@pytest.fixture(scope='session')
def app_setup():
    db_dir = os.getcwd()
    db_fd, db_path = tempfile.mkstemp(dir=db_dir)
    SuperHeroArena.db = SQLAlchemy()
    app = SuperHeroArena.create_app({'SQLALCHEMY_DATABASE_URI': 'sqlite:///{}'.format(db_path), 
                      'TESTING': True})
    
    yield app
    
    os.close(db_fd)
    os.unlink(db_path)
    
@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
