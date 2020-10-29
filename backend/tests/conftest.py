import os
import tempfile

import pytest
from yeabackend import create_app
from yeabackend.db import get_db, init_db

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')

def get_access_headers(login_response):
    access_token = login_response.get_json()['access_token']
    return {'Authorization': 'Bearer {}'.format(access_token)}

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='usertest', password='usertest'):
        return self._client.post(
            '/auth/login',
            json={'username': username, 'password': password}
        )

    def logout(self, access_headers):
        return self._client.delete('/auth/logout', headers=access_headers)

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        get_db().executescript(_data_sql)

    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def auth(client):
    return AuthActions(client)