import pytest
from yeabackend.db import get_db

@pytest.mark.parametrize('path', (
    '/location/create',
    ))
def test_login_required(client, path):
    response = client.post(path)
    assert response.status_code == 401

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

@pytest.mark.parametrize(('path', 'name', 'maximum_capacity', 'error'), (
    ('/location/create', '', 10, b'Name is required.'),
    ('/location/create', 'created', 0, b'Maximum capacity is required.'),
))
def test_create_update_validate(client, auth, path, name, maximum_capacity, error):
    auth.login()
    response = client.post(path, json={'name': name, 'maximum_capacity': maximum_capacity})
    assert error in response.data