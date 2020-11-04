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

bp = Blueprint('data', __name__)

@bp.route('/status', methods=['GET'])
@jwt_required
def status():
    db  = get_db()
    user_id = get_jwt_identity()
    user_data = db.execute(
        "SELECT * FROM user WHERE id = ?",(user_id,)).fetchone()
    return (jsonify(username = user_data["username"],
        current_location = user_data["current_location"],
        is_infected = user_data["is_infected"],
        being_in_risk_since = user_data["being_in_risk_since"],
        is_admin = user_data["is_admin"]
        ))

