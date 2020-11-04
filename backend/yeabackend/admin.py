from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response, jsonify, session, send_file
)

from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity,
    verify_jwt_in_request, verify_jwt_refresh_token_in_request,
    jwt_required
)

from werkzeug.exceptions import abort

from yeabackend.db import get_db

bp = Blueprint('admin', __name__)

@bp.route('/admin/users', methods=['GET'])
@jwt_required
def get_users_data():
    # Checkear que efectivamente es el admin
    db  = get_db()
    users_data = db.execute(
        "SELECT * FROM user"
    )
    return jsonify([dict(row) for row in users_data.fetchall()])


@bp.route('/admin/locations', methods=['GET'])
@jwt_required
def get_locations_data():
    # Checkear que efectivamente es el admin
    db  = get_db()
    locations_data = db.execute(
        "SELECT * FROM location"
    )
    # print(locations_data)
    return jsonify([dict(row) for row in locations_data.fetchall()])