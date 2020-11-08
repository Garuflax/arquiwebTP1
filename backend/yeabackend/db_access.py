from flask_jwt_extended import get_jwt_identity
from werkzeug.exceptions import abort

from yeabackend.db import get_db
from yeabackend.time_utils import (string_to_datetime, datetime_to_string)

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

def add_infection(user_id):
    """Update tables with infection,
    set users in risk that correspond
    and return those users.
    """
    users_reached = {}
    db = get_db()
    c = db.cursor()
    c.execute('SELECT * FROM checks'
        ' WHERE author_id = ?',
        (user_id,)
    )

    for row_c in c:
        d = db.cursor()
        d.execute('SELECT * FROM checks'
            ' WHERE NOT author_id = ? AND location_id = ? AND check_in_time <= ? AND (check_out_time IS NULL OR ? <= check_out_time)',
            (user_id, row_c['location_id'], row_c['check_out_time'], row_c['check_in_time'])
        )
        
        c_check_in_time = string_to_datetime(row_c['check_in_time'])
        c_check_out_time = string_to_datetime(row_c['check_out_time'])

        for row_d in d:
            d_check_in_time = string_to_datetime(row_d['check_in_time'])
            if row_d['check_out_time'] is None:
                d_check_out_time = c_check_out_time
            else:
                d_check_out_time = string_to_datetime(row_d['check_out_time'])
    
            in_risk_since = min(c_check_out_time, d_check_out_time)
            if row_d['author_id'] not in users_reached.keys():
                users_reached[row_d['author_id']] = in_risk_since
            else:
                users_reached[row_d['author_id']] = max(in_risk_since, users_reached[row_d['author_id']])

    informed_users = []
    informed_users_id = []
    c = db.cursor()
    c.execute('SELECT * FROM user WHERE id IN (%s) AND is_infected = 0' % placeholders(len(users_reached)),
        list(users_reached.keys()))
    for row_c in c:
        if row_c['being_in_risk_since'] is None or string_to_datetime(row_c['being_in_risk_since']) < users_reached[row_c['id']]:
            informed_users.append(dict(row_c))
            informed_users_id.append(row_c['id'])
            db.execute('UPDATE user SET being_in_risk_since = ? WHERE id = ?',
                (datetime_to_string(users_reached[row_c['id']]), row_c['id'])
            )
    db.execute(
        'UPDATE user SET is_infected = 1, being_in_risk_since = NULL'
        ' WHERE id = ?',
        (user_id,)
    )
    db.commit()
    return informed_users

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

def placeholders(amount):
    """Get placeholders for SQL query.
    """
    return ', '.join('?' * amount)