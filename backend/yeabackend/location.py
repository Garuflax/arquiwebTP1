from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_file, jsonify
)
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity,
    verify_jwt_in_request, verify_jwt_refresh_token_in_request,
    jwt_required
)

from flask_qrcode import QRcode

from werkzeug.exceptions import abort

from yeabackend.request_utils import get_fields
from yeabackend.db_access import (get_location, get_locations, add_location)

bp = Blueprint('location', __name__, url_prefix='/location')

@bp.route('/create', methods=['POST'])
@jwt_required
def create():

    user_id = get_jwt_identity()

    (name, maximum_capacity, latitude, longitude) = get_fields(request,
        ['name', 'maximum_capacity', 'latitude', 'longitude'])

    add_location(name, maximum_capacity, latitude, longitude, user_id)

    return jsonify(created=True,
                   message='Location created succesfully'), 201

@bp.route('/<int:id>', methods=['GET'])
@jwt_required
def location(id):
    
    location = get_location(id, False)
    return jsonify(dict(location))

@bp.route('/all', methods=['GET'])
@jwt_required
def all():
      
    return jsonify(locations=get_locations())

@bp.route("/<int:id>/qrcode", methods=["GET"])
@jwt_required
def get_qrcode(id):
    get_location(id, True)
    return send_file(QRcode.qrcode(id, mode="raw"), mimetype="image/png")
