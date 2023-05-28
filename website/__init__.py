"""
This is the website module.
"""
import os
from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

DB_NAME = 'database.db'
db = SQLAlchemy()

def create_app():
    """
    Creates and configures the Flask application & database.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dkd93kshaghj429'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Specify the file path for the database within the backend directory
    database_path = os.path.join(os.path.dirname(app.root_path), 'backend', DB_NAME)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{database_path}'

    db.init_app(app)

    with app.app_context():
        from . import models  # Imported models here to avoid circular import
        db.create_all()

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    app.debug = True

    return app
