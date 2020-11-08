import pytest
from datetime import (date, datetime)
from time import sleep
from yeabackend.db import get_db
from yeabackend.inform import string_to_datetime
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
    assert b'Missing json.' in response.data
    response = client.post(url, headers=access_headers, json={})
    assert response.status_code == 400
    assert b'Missing field: date.' in response.data

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

def test_user_is_not_in_risk_if_does_not_share_space_with_infected(app, client, auth):
    # enter location with another user
    access_headers_other = get_access_headers(
        client.post('/auth/login', json={
            'username': 'othertest', 'password': 'othertest'
        }))
    client.post('/checkin', headers=access_headers_other, json={'location_id': 1})
    client.post('/checkout', headers=access_headers_other, json={'location_id': 1})
    sleep(1.0)
    access_headers = get_access_headers(auth.login())
    client.post('/checkin', headers=access_headers, json={'location_id': 1})
    client.post('/checkout', headers=access_headers, json={'location_id': 1})
    client.post('/inform/infection', headers=access_headers, json={'date': date.today()})
    with app.app_context():
        db = get_db()
        being_in_risk_since = db.execute('SELECT being_in_risk_since FROM user'
            ' WHERE id = 3').fetchone()['being_in_risk_since']
        assert being_in_risk_since is None

def test_user_gets_risk_from_most_recent_contact_with_infected(app, client, auth):
    
    access_headers = get_access_headers(auth.login())
    access_headers_other = get_access_headers(
        client.post('/auth/login', json={
            'username': 'othertest', 'password': 'othertest'
        }))
    access_headers_another = get_access_headers(
        client.post('/auth/login', json={
            'username': 'anothertest', 'password': 'anothertest'
        }))
    client.post('/checkin', headers=access_headers_another, json={'location_id': 2})
    client.post('/checkin', headers=access_headers_other, json={'location_id': 2})
    client.post('/checkout', headers=access_headers_other, json={'location_id': 2})
    client.post('/checkout', headers=access_headers_another, json={'location_id': 2})
    client.post('/checkin', headers=access_headers, json={'location_id': 1})
    client.post('/checkin', headers=access_headers_other, json={'location_id': 1})
    client.post('/checkout', headers=access_headers_other, json={'location_id': 1})
    before = datetime.now()
    sleep(1.0)
    client.post('/checkin', headers=access_headers_other, json={'location_id': 1})
    client.post('/checkout', headers=access_headers_other, json={'location_id': 1})
    client.post('/checkout', headers=access_headers, json={'location_id': 1})
    client.post('/inform/infection', headers=access_headers, json={'date': date.today()})
    client.post('/inform/infection', headers=access_headers_another, json={'date': date.today()})
    with app.app_context():
        db = get_db()
        being_in_risk_since = db.execute('SELECT being_in_risk_since FROM user'
            ' WHERE id = 3').fetchone()['being_in_risk_since']
        assert string_to_datetime(being_in_risk_since) > before

def test_user_cannot_be_in_risk_if_it_is_infected(app, client, auth):
    
    access_headers = get_access_headers(auth.login())
    client.post('/checkin', headers=access_headers, json={'location_id': 1})
    access_headers_other = get_access_headers(
        client.post('/auth/login', json={
            'username': 'othertest', 'password': 'othertest'
        }))
    client.post('/checkin', headers=access_headers_other, json={'location_id': 1})
    access_headers = get_access_headers(auth.login())
    client.post('/checkin', headers=access_headers, json={'location_id': 1})
    client.post('/checkout', headers=access_headers, json={'location_id': 1})
    client.post('/inform/infection', headers=access_headers, json={'date': date.today()})
    client.post('/checkout', headers=access_headers_other, json={'location_id': 1})
    client.post('/inform/infection', headers=access_headers_other, json={'date': date.today()})
    with app.app_context():
        db = get_db()
        users_data = db.execute('SELECT * FROM user').fetchall()
        
        assert users_data[0]['being_in_risk_since'] is None
        assert users_data[0]['is_infected']
        assert users_data[2]['being_in_risk_since'] is None
        assert users_data[2]['is_infected']