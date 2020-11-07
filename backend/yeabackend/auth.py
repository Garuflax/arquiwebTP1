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

from yeabackend.db_access import (get_user_by_username, add_user)
from yeabackend.request_utils import get_fields

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
def register():
    """Register user without
    admin privilege
    """
    (username, password, email) = get_fields(request,
        ['username', 'password', 'email'])

    if get_user_by_username(username) is not None:
        return jsonify(created=False, 
            message='User {} is already registered.'.format(username)), 200

    add_user(username, generate_password_hash(password), email, False)

    return jsonify(created=True,
                   message='User registered succesfully.'), 201

@bp.route('/login', methods=['POST'])
def login():
    (username, password) = get_fields(request,
        ['username', 'password'])

    error = None
    user = get_user_by_username(username)

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