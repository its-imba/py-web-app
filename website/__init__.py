from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os.path import join
from flask_login import LoginManager
from . import models

db = SQLAlchemy()
DB_NAME = 'database.db'


def create_database(app):
    """
    Create the database if it does not exist.
    """
    db.create_all(app=app)
    print('Created DB')


def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'dkd93kshaghj429'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{join("website", DB_NAME)}'
    
    # Initialize the SQLAlchemy extension
    db.init_app(app)
    
    # Register blueprints for different parts of the application
    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Create the database tables
    with app.app_context():
        db.create_all()

    # Initialize the login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return models.User.query.get(int(id))

    return app