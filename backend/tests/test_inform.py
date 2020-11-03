import pytest
from datetime import date
from yeabackend.db import get_db
from conftest import get_access_headers


def test_login_required(client):
    assert client.post('/inform/infection').status_code == 401
    assert client.post('/inform/discharge').status_code == 401

@pytest.mark.parametrize(('url'), (
    ('/inform/infection'),
    ('/inform/discharge')
))
def test_date_required(client, auth, url):
    access_headers = get_access_headers(auth.login())
    response = client.post(url, headers=access_headers)
    assert response.status_code == 400
    assert b'Date is required.' in response.data

def test_cannot_inform_infection_inside_location(app, client, auth):
    access_headers = get_access_headers(auth.login())
    
    client.post('/checkin', headers=access_headers, json={'location_id': 1})
    assert client.post('/inform/infection', headers=access_headers, json={'date': date.today()}).status_code == 200
    with app.app_context():
        db = get_db()
        is_infected = db.execute('SELECT is_infected FROM user'
            ' WHERE id = 1').fetchone()['is_infected']
        assert not is_infected

def test_cannot_inform_infection_if_user_already_informed(app, client, auth):
    access_headers = get_access_headers(auth.login())
    
    client.post('/inform/infection', headers=access_headers, json={'date': date.today()})
    response = client.post('/inform/infection', headers=access_headers, json={'date': date.today()})
    assert response.status_code == 200
    assert response.get_json()['message'] == 'User already informed infection'
    with app.app_context():
        db = get_db()
        is_infected = db.execute('SELECT is_infected FROM user'
            ' WHERE id = 1').fetchone()['is_infected']
        assert is_infected

def test_cannot_discharge_if_user_is_not_infected(app, client, auth):
    access_headers = get_access_headers(auth.login())
    
    response = client.post('/inform/discharge', headers=access_headers, json={'date': date.today()})
    assert response.status_code == 200
    assert response.get_json()['message'] == 'User is not infected'
    with app.app_context():
        db = get_db()
        is_infected = db.execute('SELECT is_infected FROM user'
            ' WHERE id = 1').fetchone()['is_infected']
        assert not is_infected

def test_infection(app, client, auth):
    access_headers = get_access_headers(auth.login())
    
    assert client.post('/inform/infection', headers=access_headers, json={'date': date.today()}).status_code == 200
    with app.app_context():
        db = get_db()
        is_infected = db.execute('SELECT is_infected FROM user'
            ' WHERE id = 1').fetchone()['is_infected']
        assert is_infected

def test_discharge(app, client, auth):
    access_headers = get_access_headers(auth.login())
    
    client.post('/inform/infection', headers=access_headers, json={'date': date.today()})
    assert client.post('/inform/discharge', headers=access_headers, json={'date': date.today()}).status_code == 200
    with app.app_context():
        db = get_db()
        is_infected = db.execute('SELECT is_infected FROM user'
            ' WHERE id = 1').fetchone()['is_infected']
        assert not is_infected

def test_user_is_in_risk_if_shares_space_with_infected(app, client, auth):
    # enter location with another user
    access_headers_other = get_access_headers(
        client.post('/auth/login', json={
            'username': 'othertest', 'password': 'othertest'
        }))
    client.post('/checkin', headers=access_headers_other, json={'location_id': 1})
    access_headers = get_access_headers(auth.login())
    client.post('/checkin', headers=access_headers, json={'location_id': 1})
    client.post('/checkout', headers=access_headers, json={'location_id': 1})
    client.post('/inform/infection', headers=access_headers, json={'date': date.today()})
    with app.app_context():
        db = get_db()
        being_in_risk_since = db.execute('SELECT being_in_risk_since FROM user'
            ' WHERE id = 3').fetchone()['being_in_risk_since']
        assert being_in_risk_since is not None