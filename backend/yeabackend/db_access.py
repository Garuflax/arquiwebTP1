from flask_jwt_extended import get_jwt_identity
from werkzeug.exceptions import abort

from yeabackend.db import get_db

def get_all(table_name):
    """Get all rows from table of database and
    convert it to array of dictionaries.
    """
    c = get_db().cursor()
    c.execute('SELECT * FROM {}'.format(table_name))

    return [dict(row) for row in c]

def get_current_user():
    """Get current user from database.
    """
    return get_user_by_id(get_jwt_identity())

def get_user(identifier, value):
    """Get user from database using
    the identifier and value.
    """
    user = get_db().execute(
        'SELECT * FROM user WHERE {} = ?'.format(identifier),
        (value,)
    ).fetchone()

    return user

def get_user_by_id(id):
    """Get user from database by id.
    """
    return get_user('id', id)

def get_user_by_username(username):
    """Get user from database by
    username.
    """
    return get_user('username', username)

def get_users():
    """Get all users from database and
    convert it to array of dictionaries.
    """
    return get_all('user')

def add_user(username, password, email, is_admin):
    """Insert user to database.
    """
    db = get_db()
    db.execute(
            'INSERT INTO user (username, password, email, is_admin) VALUES (?, ?, ?, ?)',
            (username, password, email, is_admin)
        )
    db.commit()

def get_location(id, check_author=True):
    """Get location from database and check
    user is author if desired.
    """
    location = get_db().execute(
        'SELECT * FROM location WHERE id = ?',
        (id,)
    ).fetchone()

    if location is None:
        abort(404, "Location id {0} doesn't exist.".format(id))

    if check_author and location['author_id'] != get_jwt_identity():
        abort(403)

    return location

def get_locations():
    """Get all locations from database and
    convert it to array of dictionaries.
    """
    return get_all('location')

def add_location(name, maximum_capacity, latitude, longitude, author_id):
    """Insert location to database.
    """
    db = get_db()
    db.execute(
        'INSERT INTO location (name, maximum_capacity, latitude, longitude, author_id)'
        ' VALUES (?, ?, ?, ?, ?)',
        (name, maximum_capacity, latitude, longitude, author_id)
    )
    db.commit()

def enter_user_to_location(user_id, location_id, time):
    """Update tables with checkin.
    """
    db = get_db()

    db.execute(
        f"UPDATE location SET people_inside = people_inside + 1 WHERE id = {location_id}"
    )
    
    db.execute(
        f"UPDATE user SET current_location = {location_id}  WHERE id = {user_id}"
    )

    db.execute(
        'INSERT INTO checks (author_id, location_id, check_in_time)'
        ' VALUES (?, ?, ?)',
        (user_id, location_id, time)
    )

    db.commit()

def exit_user_from_location(user_id, location_id, time):
    """Update tables with checkout.
    """
    db = get_db()

    db.execute("UPDATE location SET people_inside = people_inside -1 WHERE id = ?", (location_id,))
    db.execute("UPDATE user SET current_location = NULL WHERE id = ?", (user_id,))

    db.execute(
        'UPDATE checks SET check_out_time = ?'
        ' WHERE author_id = ? AND check_out_time IS NULL',
        (time, user_id)
    )
    
    db.commit()

def add_infection(user_id):#TODO
    """Update tables with infection
    and return TODO.
    """
    db = get_db()
    db.execute(
        'UPDATE user SET is_infected = 1, being_in_risk_since = NULL'
        ' WHERE id = ?',
        (user_id,)
    )
    db.commit()

def remove_infection(user_id):
    """Update tables with discharge.
    """
    db = get_db()
    db.execute(
        'UPDATE user SET is_infected = 0'
        ' WHERE id = ?',
        (user_id,)
    )
    db.commit()