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

if __name__ == '__main__':
    pytest.main()
