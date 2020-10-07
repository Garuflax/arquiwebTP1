import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session,
    url_for, jsonify, abort
)
from werkzeug.security import check_password_hash, generate_password_hash

from yeabackend.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    """Register user without
    admin privilege
    """
    username = request.form['username']
    password = request.form['password']
    db = get_db()

    created = True
    message = 'User registered succesfully'

    #json_data = request.get_json()   TODO decide if we are going to use
    #email = json_data['email']       Forms or JSON
    #password = json_data['password']

    if not username:
        abort(400, 'Username is required.')
    elif not password:
        abort(400, 'Password is required.')
    elif db.execute(
        'SELECT id FROM user WHERE username = ?', (username,)
    ).fetchone() is not None:
        created = False
        message = 'User {} is already registered.'.format(username)

    if created:
        db.execute(
            'INSERT INTO user (username, password, is_admin) VALUES (?, ?, ?)',
            (username, generate_password_hash(password), False)
        )
        db.commit()

    return jsonify(created=created,
                   message=message)