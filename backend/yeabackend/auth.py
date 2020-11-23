import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session,
    url_for, jsonify, abort
)

from flask_jwt_extended import (
    create_access_token, get_jwt_identity,
    verify_jwt_in_request, jwt_required,
    get_jti, get_raw_jwt
)

from werkzeug.security import check_password_hash, generate_password_hash

from yeabackend import (revoked_store, ACCESS_EXPIRES)
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
    print("Asd")

    (username, password) = get_fields(request,['username', 'password'])

    print("Asd")
    print(username)
    print(password)

    error = None
    user = get_user_by_username(username)

    if user is None:
        error = 'Incorrect username.'
    elif not check_password_hash(user['password'], password):
        error = 'Incorrect password.'

    if error is None:
        access_token = create_access_token(identity=user['id'])
        
        # Store the tokens in redis with a status of not currently revoked. We
        # can use the `get_jti()` method to get the unique identifier string for
        # each token. We can also set an expires time on these tokens in redis,
        # so they will get automatically removed after they expire. We will set
        # everything to be automatically removed shortly after the token expires
        access_jti = get_jti(encoded_token=access_token)
        revoked_store.set(access_jti, 'false', ACCESS_EXPIRES * 1.2)

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
    jti = get_raw_jwt()['jti']
    revoked_store.set(jti, 'true', ACCESS_EXPIRES * 1.2)
    return jsonify(
            message='Logged out succesfully.')