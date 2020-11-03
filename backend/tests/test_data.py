import pytest
from datetime import date
from yeabackend.db import get_db
from conftest import get_access_headers


def test_login_required(client):
    assert client.get('/status').status_code == 401

def test_status(client, auth):
    access_headers = get_access_headers(auth.login())
    
    response = client.get('/status', headers=access_headers)
    assert response.status_code == 200
    user_data = response.get_json()
    assert 'usertest' == user_data['username']
    assert 0 == user_data['is_admin']
    assert 0 == user_data['is_infected']
    assert None == user_data['being_in_risk_since']
    assert None == user_data['current_location']