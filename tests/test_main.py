import os
import pytest

os.environ['PYTHONPATH'] = '/Users/samhiscox/py-web-app:' + os.environ.get('PYTHONPATH', '')

from website import create_app

def test_create_app():
    app = create_app()
    assert app is not None
    # Add additional assertions for app configuration if needed

def test_app_execution():
    app = create_app()
    app.config['DEBUG'] = True  # Set debug mode explicitly for testing
    assert app.debug is True
    assert app.config['DEBUG'] is True

def test_app_debug_mode():
    app = create_app()
    assert app.debug is True

def test_app_secret_key():
    app = create_app()
    assert app.config['SECRET_KEY'] == 'dkd93kshaghj429'

def test_app_db_uri():
    app = create_app()
    expected_uri = 'sqlite:///' + os.path.join(os.path.dirname(app.root_path), 'backend', 'database.db')
    assert app.config['SQLALCHEMY_DATABASE_URI'] == expected_uri

def test_database_initialization():
    app = create_app()
    with app.app_context():
        from website import db
        assert db.engine is not None
        # Add additional assertions for database initialization if needed

def test_blueprint_registration():
    app = create_app()
    assert 'views' in app.blueprints
    assert 'auth' in app.blueprints
    # Add additional assertions for blueprint registration if needed

def test_login_manager_initialization():
    app = create_app()
    assert app.login_manager is not None
    assert app.login_manager.login_view == 'auth.login'
    # Add additional assertions for login manager initialization if needed

if __name__ == '__main__':
    pytest.main()
