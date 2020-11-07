import pytest
from datetime import date
from yeabackend.db import get_db
from conftest import get_access_headers


def test_login_required(client):
    assert client.post('/checkin').status_code == 401
    assert client.post('/checkout').status_code == 401

def test_cannot_checkin_to_location_that_does_not_exist(app, client, auth):
    access_headers = get_access_headers(auth.login())
    
    response = client.post('/checkin', headers=access_headers, json={'location_id': 8})
    assert response.status_code == 404
    assert b"Location id 8 doesn't exist." in response.data
    
    with app.app_context():
        db = get_db()
        current_location = db.execute('SELECT current_location FROM user'
            ' WHERE id = 1').fetchone()['current_location']
        assert current_location is None
        checks_amount = db.execute('SELECT COUNT(id) FROM checks').fetchone()[0]
        assert checks_amount == 0

def test_cannot_checkin_if_user_is_infected(app, client, auth):
    access_headers = get_access_headers(auth.login())
    
    client.post('/inform/infection', headers=access_headers, json={'date': date.today()})
    response = client.post('/checkin', headers=access_headers, json={'location_id': 1})
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json['message'] == "Cannot enter, you are infected."
    assert not response_json['success']
    with app.app_context():
        db = get_db()
        current_location = db.execute('SELECT current_location FROM user'
            ' WHERE id = 1').fetchone()['current_location']
        assert current_location is None
        checks_amount = db.execute('SELECT COUNT(id) FROM checks').fetchone()[0]
        assert checks_amount == 0

def test_cannot_checkin_if_user_is_already_in_a_location(app, client, auth):
    access_headers = get_access_headers(auth.login())
    
    client.post('/checkin', headers=access_headers, json={'location_id': 1})
    response = client.post('/checkin', headers=access_headers, json={'location_id': 2})
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json['message'] == "You are already in a location."
    assert not response_json['success']
    with app.app_context():
        db = get_db()
        current_location = db.execute('SELECT current_location FROM user'
            ' WHERE id = 1').fetchone()['current_location']
        assert current_location == 1
        checks_amount = db.execute('SELECT COUNT(id) FROM checks').fetchone()[0]
        assert checks_amount == 1

def test_cannot_checkin_to_maxed_location(app, client, auth):
    # enter location with another user
    access_headers_other = get_access_headers(
        client.post('/auth/login', json={
            'username': 'othertest', 'password': 'othertest'
        }))
    client.post('/checkin', headers=access_headers_other, json={'location_id': 7})
    access_headers = get_access_headers(auth.login())
    
    response = client.post('/checkin', headers=access_headers, json={'location_id': 7})
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json['message'] == "Cannot enter, location is full."
    assert not response_json['success']
    with app.app_context():
        db = get_db()
        current_location = db.execute('SELECT current_location FROM user'
            ' WHERE id = 1').fetchone()['current_location']
        assert current_location is None
        checks_data = db.execute('SELECT * FROM checks').fetchall()
        assert len(checks_data) == 1
        assert checks_data[0]['author_id'] == 3

def test_cannot_checkout_if_user_is_not_in_location(app, client, auth):
    access_headers = get_access_headers(auth.login())
    
    response = client.post('/checkout', headers=access_headers, json={'location_id': 1})
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json['message'] == "Not current location."
    assert not response_json['success']
    with app.app_context():
        db = get_db()
        current_location = db.execute('SELECT current_location FROM user'
            ' WHERE id = 1').fetchone()['current_location']
        assert current_location is None
        checks_amount = db.execute('SELECT COUNT(id) FROM checks').fetchone()[0]
        assert checks_amount == 0

def test_checkin(app, client, auth):
    access_headers = get_access_headers(auth.login())

    response = client.post('/checkin', headers=access_headers, json={'location_id': 1})
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json['message'] == "Checkin successful."
    assert response_json['success']

    with app.app_context():
        db = get_db()
        user_data = db.execute('SELECT * FROM user'
            ' WHERE id = 1').fetchone()
        assert user_data['current_location'] == 1
        people_inside_location = db.execute('SELECT people_inside FROM location'
            ' WHERE id = 1').fetchone()['people_inside']
        assert people_inside_location == 1
        check_data = db.execute('SELECT * FROM checks'
            ' WHERE author_id = 1').fetchone()
        assert check_data['location_id'] == 1
        assert check_data['check_in_time'] is not None
        assert check_data['check_out_time'] is None
    
def test_checkout(app, client, auth):
    access_headers = get_access_headers(auth.login())

    client.post('/checkin', headers=access_headers, json={'location_id': 1})
    response = client.post('/checkout', headers=access_headers, json={'location_id': 1})
    response_json = response.get_json()
    assert response.status_code == 200
    assert response_json['message'] == "Checkout successful."
    assert response_json['success']

    with app.app_context():
        db = get_db()
        user_data = db.execute('SELECT * FROM user'
            ' WHERE id = 1').fetchone()
        assert user_data['current_location'] is None
        people_inside_location = db.execute('SELECT people_inside FROM location'
            ' WHERE id = 1').fetchone()['people_inside']
        assert people_inside_location == 0
        check_data = db.execute('SELECT * FROM checks'
            ' WHERE author_id = 1').fetchone()
        assert check_data['location_id'] == 1
        assert check_data['check_in_time'] is not None
        assert check_data['check_out_time'] is not None