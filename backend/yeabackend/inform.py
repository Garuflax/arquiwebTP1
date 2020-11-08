from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_file, jsonify
)
from flask_jwt_extended import (
    get_jwt_identity, jwt_required
)

from flask_mail import Mail, Message

from werkzeug.exceptions import abort

from yeabackend.db import get_db
from yeabackend.db_access import (get_current_user, remove_infection)
from yeabackend.request_utils import get_fields
from yeabackend.time_utils import (current_datetime, string_to_datetime)

bp = Blueprint('inform', __name__, url_prefix='/inform')

@bp.route('/infection', methods=['POST'])
@jwt_required
def infection():

    user_id = get_jwt_identity()

    (date,) = get_fields(request, ['date'])

    db = get_db()

    user_data = get_current_user()

    if user_data['current_location']:
        return jsonify(message='User cannot be inside location'), 200
    if user_data['is_infected']:
        return jsonify(message='User already informed infection'), 200
    db.execute(
        'UPDATE user SET is_infected = 1, being_in_risk_since = NULL'
        ' WHERE id = ?',
        (user_id,)
    )
    #db.commit()

    users_in_risk = {}
    c = db.cursor()
    c.execute('SELECT * FROM checks'
        ' WHERE author_id = ?',
        (user_id,)
    )

    for row_c in c:
        d = db.cursor()
        d.execute('SELECT * FROM checks'
            ' WHERE NOT author_id = ? AND location_id = ?',
            (user_id, row_c['location_id'])
        )
        
        c_check_in_time = string_to_datetime(row_c['check_in_time'])
        c_check_out_time = string_to_datetime(row_c['check_out_time'])

        for row_d in d:
            d_check_in_time = string_to_datetime(row_d['check_in_time'])
            if row_d['check_out_time'] is None:
                d_check_out_time = current_datetime()
            else:
                d_check_out_time = string_to_datetime(row_d['check_out_time'])
            if were_together(c_check_in_time, c_check_out_time, d_check_in_time, d_check_out_time):
                in_risk_since = min(c_check_out_time, d_check_out_time)
                if row_d['author_id'] not in users_in_risk.keys():
                    users_in_risk[row_d['author_id']] = in_risk_since
                else:
                    users_in_risk[row_d['author_id']] = max(in_risk_since, users_in_risk[row_d['author_id']])
    
    mailing_data = []
    for user_in_risk_id, in_risk_since in users_in_risk.items():
        user_mailing_data = db.execute(
            'SELECT username, email FROM user WHERE id = ? AND is_infected = 0 AND (being_in_risk_since IS NULL OR being_in_risk_since < ?)',
            (user_in_risk_id, in_risk_since)
        ).fetchone()
        if user_mailing_data is not None:
            mailing_data.append(dict(user_mailing_data))
        db.execute(
            'UPDATE user SET being_in_risk_since = ?'
            ' WHERE id = ? AND is_infected = 0 AND (being_in_risk_since IS NULL OR being_in_risk_since < ?)',
            (in_risk_since, user_in_risk_id, in_risk_since)
        )
    db.commit()
    message_body = "Lamentamos informarle que usted {} está en riego de contagiado."

    mail = Mail()
    for recipient_data in mailing_data:
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

def were_together(user1_check_in, user1_check_out, user2_check_in, user2_check_out):
    return user1_check_in <= user2_check_out and user2_check_in <= user1_check_out