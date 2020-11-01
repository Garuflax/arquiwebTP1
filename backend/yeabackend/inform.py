from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, send_file, jsonify
)
from flask_jwt_extended import (
    get_jwt_identity, jwt_required
)

from werkzeug.exceptions import abort

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

    # Obtener locaciones donde estuvo la persona

    # Obtener personas que hayan estado ahí en el tiempo

    # Poner a esas personas en estado de riesgo e informar via mail
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

