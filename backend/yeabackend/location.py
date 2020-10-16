from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from werkzeug.exceptions import abort

from yeabackend.auth import login_required
from yeabackend.db import get_db

bp = Blueprint('location', __name__, url_prefix='/location')

@bp.route('/create', methods=['POST'])
def create():

    login_required()

    json_data = request.get_json()
    name = json_data['name']
    maximum_capacity = json_data['maximum_capacity']

    if not name:
        abort(400, 'Name is required.')

    if not maximum_capacity:
        abort(400, 'Maximum capacity is required.')

    db = get_db()
    db.execute(
        'INSERT INTO location (name, maximum_capacity, author_id)'
        ' VALUES (?, ?, ?)',
        (name, maximum_capacity, g.user['id'])
    )
    db.commit()
    return jsonify(created=True,
                   message='Location created succesfully'), 201