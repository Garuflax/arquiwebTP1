from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response, jsonify, session, send_file
)

from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity,
    verify_jwt_in_request, verify_jwt_refresh_token_in_request,
    jwt_required
)

from werkzeug.exceptions import abort

from yeabackend.db_access import get_current_user

bp = Blueprint('data', __name__)

@bp.route('/status', methods=['GET'])
@jwt_required
def status():
    return (jsonify(dict(get_current_user())))

