import pytest
from yeabackend.db import get_db
from conftest import get_access_headers

def test_login_required(client):
    assert client.post('/location/create').status_code == 401
    assert client.get('/location/all').status_code == 401
    assert client.get('/location/1').status_code == 401
    assert client.get('/location/1/qrcode').status_code == 401

def test_exists_required(client, auth):
    access_headers = get_access_headers(auth.login())
    
    assert client.get('/location/8', headers=access_headers).status_code == 404

def test_author_required(app, client, auth):
    # change the location author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE location SET author_id = 2 WHERE id = 1')
        db.commit()

    access_headers = get_access_headers(auth.login())
    # current user can't get other user's location qr
    assert client.get('/location/1/qrcode', headers=access_headers).status_code == 403

def test_create(client, auth, app):
    access_headers = get_access_headers(auth.login())
    assert client.post(
            '/location/create',
            headers=access_headers,
            json={'name': 'created', 'maximum_capacity': 10, 'latitude': 5.0, 'longitude': 10.0}
        ).status_code == 201

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM location').fetchone()[0]
        assert count == 8

def test_get(client, auth, app):
    access_headers = get_access_headers(auth.login())
    response = client.get('/location/1', headers=access_headers)
    assert response.status_code == 200
    json_data = response.get_json()
    
    assert 'test location 1' == json_data['name']
    assert 10 == json_data['maximum_capacity']
    assert 31.0 == json_data['latitude']
    assert 61.0 == json_data['longitude']
    assert 1 == json_data['author_id']
    assert 1 == json_data['id']

def test_author_not_required(client, auth, app):
    # change the location author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE location SET author_id = 2 WHERE id = 1')
        db.commit()

    access_headers = get_access_headers(auth.login())
    # current user can get other user's location
    assert client.get('/location/1', headers=access_headers).status_code == 200

@pytest.mark.parametrize(('name', 'maximum_capacity', 'latitude', 'longitude','error'), (
    ('', 10, 5.0, 10.0, b'Invalid field: name.'),
    ('created', 0, 5.0, 10.0, b'Invalid field: maximum_capacity.'),
    ('created', 10, 0.0, 10.0, b'Invalid field: latitude.'),
    ('created', 10, 5.0, 0.0, b'Invalid field: longitude.'),
))
def test_create_validate(client, auth, name, maximum_capacity, latitude, longitude, error):
    access_headers = get_access_headers(auth.login())
    response = client.post('/location/create', headers=access_headers, json={'name': name, 'maximum_capacity': maximum_capacity, 'latitude': latitude, 'longitude': longitude})
    assert response.status_code == 400
    assert error in response.data

@pytest.mark.parametrize(('json','error'), (
    ({'maximum_capacity': 10, 'latitude': 5.0, 'longitude': 10.0}, b'Missing field: name.'),
    ({'name': 'name', 'latitude': 5.0, 'longitude': 10.0}, b'Missing field: maximum_capacity.'),
    ({'name': 'name', 'maximum_capacity': 10, 'longitude': 10.0}, b'Missing field: latitude.'),
    ({'name': 'name', 'maximum_capacity': 10, 'latitude': 5.0}, b'Missing field: longitude.'),
))
def test_create_check_fields(client, auth, json, error):
    access_headers = get_access_headers(auth.login())

    response = client.post('/location/create', headers=access_headers, json=json)
    assert response.status_code == 400
    assert error in response.data

def test_all(client, auth, app):
    access_headers = get_access_headers(auth.login())
    response = client.get('/location/all', headers=access_headers)
    assert response.status_code == 200
    json_data = response.get_json()
    locations = json_data['locations']
    assert 7 == len(locations)

    location = locations[0]
    assert 'test location 1' == location['name']
    assert 10 == location['maximum_capacity']
    assert 31.0 == location['latitude']
    assert 61.0 == location['longitude']
    assert 1 == location['author_id']
    assert 1 == location['id']

def test_qrcode(client, auth):
    access_headers = get_access_headers(auth.login())
    response = client.get('/location/1/qrcode', headers=access_headers)
    assert response.status_code == 200
    assert response.mimetype == "image/png"
