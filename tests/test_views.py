from website.models import Note, User # Import the Note and User models
from website import create_app, db


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 302  # Redirect to login page for unauthenticated users

    response = client.get(response.headers['Location'])
    assert response.status_code == 200  # Successful response
    assert b'Login' in response.data  # Check for the login form


