import pytest
from yeabackend.db import get_db

@pytest.mark.parametrize('path', (
    '/location/create',
    '/location/update',
    ))
def test_login_required(client, path):
    response = client.post(path)
    assert response.status_code == 401

def test_author_required(app, client, auth):
    # change the post author to another user
    with app.app_context():
        db = get_db()
        db.execute('UPDATE location SET author_id = 2 WHERE id = 1')
        db.commit()

    auth.login()
    # current user can't modify other user's post
    assert client.post('/location/update', json={'id': 1, 'name': 'updated', 'maximum_capacity': 5}).status_code == 403

@pytest.mark.parametrize('path', (
    '/location/update',
))
def test_exists_required(client, auth, path):
    auth.login()
    assert client.post(path, json={'id': 2, 'name': 'updated', 'maximum_capacity': 5}).status_code == 404

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

def test_update(client, auth, app):
    auth.login()
    client.post('/location/update', json={'id': 1, 'name': 'updated', 'maximum_capacity': 5})

    with app.app_context():
        db = get_db()
        location = db.execute('SELECT * FROM location WHERE id = 1').fetchone()
        assert location['name'] == 'updated'
        assert location['maximum_capacity'] == 5

@pytest.mark.parametrize(('path', 'name', 'maximum_capacity', 'error'), (
    ('/location/create', '', 10, b'Name is required.'),
    ('/location/create', 'created', 0, b'Maximum capacity is required.'),
    ('/location/update', '', 10, b'Name is required.'),
    ('/location/update', 'created', 0, b'Maximum capacity is required.'),
))
def test_create_update_validate(client, auth, path, name, maximum_capacity, error):
    auth.login()
    response = client.post(path, json={'id': 1, 'name': name, 'maximum_capacity': maximum_capacity})
    assert error in response.data