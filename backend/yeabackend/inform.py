from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_file, jsonify
)
from flask_jwt_extended import (
    get_jwt_identity, jwt_required
)

from werkzeug.exceptions import abort
from datetime import datetime

from yeabackend.db import get_db

bp = Blueprint('inform', __name__, url_prefix='/inform')

@bp.route('/infection', methods=['POST'])
@jwt_required
def infection():

    user_id = get_jwt_identity()

    try:
        date = request.get_json()['date']
    except Exception as e:
        abort(400, 'Date is required.')

    db = get_db()

    user_data = get_user_data(user_id, db)

    if user_data['current_location']:
        return jsonify(message='User cannot be inside location'), 200
    if user_data['is_infected']:
        return jsonify(message='User already informed infection'), 200
    db.execute(
        'UPDATE user SET is_infected = 1'
        ' WHERE id = ?',
        (user_id,)
    )
    db.commit()

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
                d_check_out_time = datetime.now()
            else:
                d_check_out_time = string_to_datetime(row_d['check_out_time'])
            if were_together(c_check_in_time, c_check_out_time, d_check_in_time, d_check_out_time):
                in_risk_since = min(c_check_out_time, d_check_out_time)
                if row_d['author_id'] not in users_in_risk.keys():
                    users_in_risk[row_d['author_id']] = in_risk_since
                else:
                    users_in_risk[row_d['author_id']] = max(in_risk_since, users_in_risk[row_d['author_id']])

    for user_in_risk_id, in_risk_since in users_in_risk.items():
        db.execute(
            'UPDATE user SET being_in_risk_since = ?'
            ' WHERE id = ? AND (being_in_risk_since IS NULL OR being_in_risk_since < ?)',
            (in_risk_since, user_in_risk_id, in_risk_since)
        )
        db.commit()
        # TODO Informar via mail
        # FIXME se puede estar infectado y en riesgo. ¿Queremos eso?

    return jsonify(message='Infection reported succesfully'), 200

@bp.route('/discharge', methods=['POST'])
@jwt_required
def discharge():
    
    user_id = get_jwt_identity()

    try:
        date = request.get_json()['date']
    except Exception as e:
        abort(400, 'Date is required.')

    db = get_db()

    user_data = get_user_data(user_id, db)

    if not user_data['is_infected']:
        return jsonify(message='User is not infected'), 200

    db.execute(
        'UPDATE user SET is_infected = 0'
        ' WHERE id = ?',
        (user_id,)
    )
    db.commit()
    return jsonify(message='Discharge reported succesfully'), 200

def get_user_data(user_id, db):
    return db.execute(
        'SELECT is_infected, current_location FROM user'
        ' WHERE id = ?',
        (user_id,)
    ).fetchone()

def were_together(user1_check_in, user1_check_out, user2_check_in, user2_check_out):
    return user1_check_in <= user2_check_out and user2_check_in <= user1_check_out

def string_to_datetime(ts):
    return datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')