import pytest

from flask import g, session
from yeabackend.db import get_db
from conftest import get_access_headers


def test_register(client, app):
    
    response = client.post(
        '/auth/register', json={'username': 'a', 'password': 'a', 'email': 'a@test.com'}
    )
    assert response.status_code == 201

    with app.app_context():
        assert get_db().execute(
            "select * from user where username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'password', 'email','message'), (
    ('', '', '',b'Invalid field: username.'),
    ('a', '', '',b'Invalid field: password.'),
    ('a', 'a', '',b'Invalid field: email.'),
    ('usertest', 'usertest', 'a@test.com',b'already registered'),
))
def test_register_validate_input(client, username, password, email, message):
    response = client.post(
        '/auth/register',
        json={'username': username, 'password': password, 'email': email}
    )
    assert message in response.data

def test_login(client, auth):
    assert client.post('/auth/login', json={
        'username': 'usertest', 'password': 'usertest'
    }).status_code == 200
    response = auth.login()
    assert 'access_token' in response.get_json()

@pytest.mark.parametrize(('username', 'password', 'message'), (
    ('a', 'usertest', 'Incorrect username.'),
    ('usertest', 'a', 'Incorrect password.'),
))
def test_login_validate_input(auth, username, password, message):
    response = auth.login(username, password)
    json_data = response.get_json()
    assert message == json_data['error']
    assert 'Authentication failed.' == json_data['message']

def test_cannot_logout_missing_headers(client, auth):
    response = auth.logout(None)
    assert response.status_code == 401
    assert response.get_json() == {'msg': "Missing Authorization Header"}

def test_logout(client, auth):
    access_headers = get_access_headers(auth.login())

    response = auth.logout(access_headers)
    assert response.status_code == 200