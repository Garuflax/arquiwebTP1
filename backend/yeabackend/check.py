from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response, jsonify, session, send_file
)

from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity,
    verify_jwt_in_request, verify_jwt_refresh_token_in_request,
    jwt_required
)

from werkzeug.exceptions import abort
from datetime import datetime

from yeabackend.db import get_db

from yeabackend.location import bp as location_bp

# from flask_qrcode import QRcode

bp = Blueprint('check', __name__)

@bp.route('/current_location', methods=['GET'])
@jwt_required
def current_location():
    db  = get_db()
    user_id = get_jwt_identity()
    location_data = db.execute(
        "SELECT * FROM user WHERE id = ?",(user_id,)).fetchone()
    return (jsonify(current_location = location_data["current_location"]))

@bp.route('/checkin', methods=['POST'])
@jwt_required
def checkin():
    user_id = get_jwt_identity()
    location_id = request.get_json()["location_id"]
    
    db = get_db()
    location_data = db.execute(
        "SELECT * FROM location WHERE id = ?",
        (location_id,)).fetchone()
    
    user_data = db.execute(
        "SELECT * FROM user WHERE id = ?",
        (user_id,)).fetchone()

    if location_data is None:
        return jsonify(message="Location doesn't exist."), 200

    if user_data["is_infected"]:
        return jsonify(message="Cannot enter, you are infected."), 200

    if location_data['people_inside'] == location_data['maximum_capacity']:
        return jsonify(message="Cannot enter, location is full."), 200

    db.execute(
        f"UPDATE location SET people_inside = people_inside + 1 WHERE id = {location_id}"
    )
    
    db.execute(
        f"UPDATE user SET current_location = {location_id}  WHERE id = {user_id}"
    )

    db.execute(
        'INSERT INTO checks (author_id, location_id, check_in_time)'
        ' VALUES (?, ?, ?)',
        (user_id, location_id, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    )

    db.commit()

    return ('')

@bp.route('/checkout', methods=['POST'])
@jwt_required
def checkout():
    
    db = get_db()
    user_id = get_jwt_identity()
    location_id = request.get_json()["location_id"]
    
    db.execute("UPDATE location SET people_inside = people_inside -1 WHERE id = ?", (location_id,))
    db.execute("UPDATE user SET current_location = NULL WHERE id = ?", (user_id,))

    db.execute(
        'UPDATE checks SET check_out_time = ?'
        ' WHERE author_id = ? AND check_out_time IS NULL',
        (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user_id)
    )
    
    db.commit()
    return ('')