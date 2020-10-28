import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session,
    url_for, jsonify, abort
)

from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity,
    verify_jwt_in_request, verify_jwt_refresh_token_in_request
)

from werkzeug.security import check_password_hash, generate_password_hash

from yeabackend.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    """Register user without
    admin privilege
    """
    json_data = request.get_json()
    username = json_data['username']
    password = json_data['password']
    email = json_data['email']
    db = get_db()

    created = True
    message = 'User registered succesfully'

    if not username:
        abort(400, 'Username is required.')
    elif not password:
        abort(400, 'Password is required.')
    elif not email:
        abort(400, 'Email is required.')
    elif db.execute(
        'SELECT id FROM user WHERE username = ?', (username,)
    ).fetchone() is not None:
        created = False
        message = 'User {} is already registered.'.format(username)

    if created:
        db.execute(
            'INSERT INTO user (username, password, email, is_admin) VALUES (?, ?, ?, ?)',
            (username, generate_password_hash(password), email, False)
        )
        db.commit()

    return jsonify(created=created,
                   message=message), 201

@bp.route('/login', methods=['POST'])
def login():
    json_data = request.get_json()
    username = json_data['username']
    password = json_data['password']
    db = get_db()
    error = None
    user = db.execute(
        'SELECT * FROM user WHERE username = ?', (username,)
    ).fetchone()

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error is None:
        #session.clear()
        #session['user_id'] = user['id']
        access_token = create_access_token(identity=user['id'],expires_delta=False)
        refresh_token = create_refresh_token(identity=user['id'])
        return jsonify(
            message='Authenticated succesfully.',
            is_admin=user['is_admin'],
            accessToken=access_token,
            refreshToken=refresh_token)

    return jsonify(
            message='Authentication failed.',
            error=error), 401

@bp.route('/logout', methods=['POST'])
def logout():
    #session.clear()#TODO check if it logged in
    return jsonify(
            message='Logged out succesfully.')


# @bp.before_app_request
# def load_logged_in_user():

#     #user_id = session.get('user_id')
    
#     if user_id is None:
#         g.user = None
#     else:
#         g.user = get_db().execute(
#             'SELECT * FROM user WHERE id = ?', (user_id,)
#         ).fetchone()

def login_required():
    
    if g.user is None:
        abort(401, 'It is required to be logged in.')
    