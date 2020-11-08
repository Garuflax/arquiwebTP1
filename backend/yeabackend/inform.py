from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_file, jsonify
)
from flask_jwt_extended import (
    get_jwt_identity, jwt_required
)

from flask_mail import Mail, Message

from werkzeug.exceptions import abort

from yeabackend.db_access import (get_current_user, add_infection, remove_infection)
from yeabackend.request_utils import get_fields
from yeabackend.time_utils import (current_datetime, string_to_datetime)

bp = Blueprint('inform', __name__, url_prefix='/inform')

@bp.route('/infection', methods=['POST'])
@jwt_required
def infection():

    user_id = get_jwt_identity()

    (date,) = get_fields(request, ['date'])

    user_data = get_current_user()

    if user_data['current_location']:
        return jsonify(message='User cannot be inside location'), 200
    if user_data['is_infected']:
        return jsonify(message='User already informed infection'), 200
    users_to_inform = add_infection(user_id)

    message_body = "Lamentamos informarle que usted {} está en riego de contagiado."

    mail = Mail()
    for recipient_data in users_to_inform:
        username = recipient_data["username"]
        email = recipient_data["email"]
        msg = Message(
                message_body.format(username), 
                sender="from@example.com",
                recipients=[email],)
        mail.send(msg)

    return jsonify(message='Infection reported succesfully'), 200

@bp.route('/discharge', methods=['POST'])
@jwt_required
def discharge():
    
    user_id = get_jwt_identity()

    (date,) = get_fields(request, ['date'])

    user_data = get_current_user()

    if not user_data['is_infected']:
        return jsonify(message='User is not infected'), 200

    remove_infection(user_id)
    return jsonify(message='Discharge reported succesfully'), 200