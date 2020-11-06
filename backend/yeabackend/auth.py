import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session,
    url_for, jsonify, abort
)

from flask_jwt_extended import (
    create_access_token, get_jwt_identity,
    verify_jwt_in_request, jwt_required
)

from werkzeug.security import check_password_hash, generate_password_hash

from yeabackend.db import get_db
from yeabackend.request_utils import get_fields

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    """Register user without
    admin privilege
    """
    (username, password, email) = get_fields(request,
        ['username', 'password', 'email'])
    db = get_db()

    created = True
    message = 'User registered succesfully'

    if db.execute(
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
    (username, password) = get_fields(request,
        ['username', 'password'])
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
        access_token = create_access_token(identity=user['id'],expires_delta=False)
        #refresh_token = create_refresh_token(identity=user['id'])
        return jsonify(
            message='Authenticated succesfully.',
            access_token=access_token
            )

    return jsonify(
            message='Authentication failed.',
            error=error), 401

@bp.route('/logout', methods=['DELETE'])
@jwt_required
def logout():
    #TODO Eliminar token
    return jsonify(
            message='Logged out succesfully.')