from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response, jsonify, session, send_file
)

from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity,
    verify_jwt_in_request, verify_jwt_refresh_token_in_request,
    jwt_required
)

from werkzeug.exceptions import abort

from yeabackend.db_access import (get_current_user, get_location, enter_user_to_location, exit_user_from_location)
from yeabackend.request_utils import get_fields
from yeabackend.time_utils import current_datetime_string
from yeabackend.location import bp as location_bp

# from flask_qrcode import QRcode

bp = Blueprint('check', __name__)

@bp.route('/checkin', methods=['POST'])
@jwt_required
def checkin():
    user_id = get_jwt_identity()
    (location_id,) = get_fields(request, ['location_id'])

    location_data = get_location(location_id, False)
    
    user_data = get_current_user()

    if user_data['current_location'] is not None:
        return jsonify(success=False, message="You are already in a location."), 200

    if user_data["is_infected"]:
        return jsonify(success=False, message="Cannot enter, you are infected."), 200

    if location_data['people_inside'] == location_data['maximum_capacity']:
        return jsonify(success=False, message="Cannot enter, location is full."), 200

    enter_user_to_location(user_id, location_id, current_datetime_string())

    return jsonify(success=True, message="Checkin successful.")

@bp.route('/checkout', methods=['POST'])
@jwt_required
def checkout():
    
    user_id = get_jwt_identity()
    (location_id,) = get_fields(request, ['location_id'])

    user_data = get_current_user()

    if user_data['current_location'] != location_id:
        return jsonify(success=False, message="Not current location."), 200
    
    exit_user_from_location(user_id, location_id, current_datetime_string())

    return jsonify(success=True, message="Checkout successful.")