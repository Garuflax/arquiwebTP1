import pytest
from datetime import date

from conftest import get_access_headers


def test_login_required(client):
    assert client.get('/admin/users').status_code == 401

def test_admin_required(client, auth):
    access_headers = get_access_headers(auth.login())
    assert client.get('/admin/users', headers=access_headers).status_code == 403

def test_get_users_data(client, auth):
    # login with admin
    access_headers_admin = get_access_headers(
        client.post('/auth/login', json={
            'username': 'admintest', 'password': 'admintest'
        }))
    response = client.get('/admin/users', headers=access_headers_admin)
    
    users = response.get_json()
    assert len(users) == 4
    assert users[0]['username'] == 'usertest'