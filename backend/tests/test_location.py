import pytest
from yeabackend.db import get_db

def test_login_required(client):
    assert client.post('/location/create').status_code == 401
    assert client.get('/location/all').status_code == 401
    assert client.get('/location/1').status_code == 401
    assert client.put('/location/1').status_code == 401
    assert client.delete('/location/1').status_code == 401

def test_author_required(app, client, auth):
    # change the location author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE location SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # current user can't modify other user's location
    assert client.put('/location/1', json={'name': 'updated', 'maximum_capacity': 5}).status_code == 403
    assert client.delete('/location/1').status_code == 403

def test_exists_required(client, auth):
    auth.login()
    assert client.get('/location/2').status_code == 404
    assert client.put('/location/2', json={'name': 'updated', 'maximum_capacity': 5}).status_code == 404
    assert client.delete('/location/2').status_code == 404

def test_create(client, auth, app):
    auth.login()
    assert client.post(
            '/location/create',
            json={'name': 'created', 'maximum_capacity': 10}
        ).status_code == 201

    with app.app_context():
        db = get_db()
        count = db.execute('SELECT COUNT(id) FROM location').fetchone()[0]
        assert count == 2

def test_get(client, auth, app):
    auth.login()
    response = client.get('/location/1')
    assert response.status_code == 200
    json_data = response.get_json()
    
    assert 'test location' == json_data['name']
    assert 10 == json_data['maximum_capacity']
    assert 1 == json_data['author_id']
    assert 1 == json_data['id']

def test_author_not_required(client, auth, app):
    # change the location author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE location SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # current user can get other user's location
    assert client.get('/location/1').status_code == 200

def test_update(client, auth, app):
    auth.login()
    client.put('/location/1', json={'name': 'updated', 'maximum_capacity': 5})

    with app.app_context():
        db = get_db()
        location = db.execute('SELECT * FROM location WHERE id = 1').fetchone()
        assert location['name'] == 'updated'
        assert location['maximum_capacity'] == 5

@pytest.mark.parametrize(('name', 'maximum_capacity', 'error'), (
    ('', 10, b'Name is required.'),
    ('created', 0, b'Maximum capacity is required.'),
))
def test_create_update_validate(client, auth, name, maximum_capacity, error):
    auth.login()
    response = client.post('/location/create', json={'name': name, 'maximum_capacity': maximum_capacity})
    assert error in response.data
    response = client.put('/location/1', json={'name': name, 'maximum_capacity': maximum_capacity})
    assert error in response.data

def test_create_update_check_fields(client, auth):
    auth.login()
    error = b'Missing field: name.'
    response = client.post('/location/create', json={'maximum_capacity': 0})
    assert error in response.data
    error = b'Missing field: maximum_capacity.'
    response = client.put('/location/1', json={'name': 'name'})
    assert error in response.data

def test_delete(client, auth, app):
    auth.login()
    response = client.delete('/location/1')

    with app.app_context():
        db = get_db()
        location = db.execute('SELECT * FROM location WHERE id = 1').fetchone()
        assert location is None

def test_all(client, auth, app):
    auth.login()
    response = client.get('/location/all')
    assert response.status_code == 200
    json_data = response.get_json()
    locations = json_data['locations']
    assert 1 == len(locations)

    location = locations[0]
    assert 'test location' == location['name']
    assert 10 == location['maximum_capacity']
    assert 1 == location['author_id']
    assert 1 == location['id']