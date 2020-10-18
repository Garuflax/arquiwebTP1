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

@bp.route('/update', methods=['POST'])
def update():

    login_required()

    json_data = request.get_json()

    #TODO better sanitation
    #if 'name' not in json_data or 'maximum_capacity' not in json_data or 'id' not in json_data:
    #       return abort(400, 'Missing field.')

    name = json_data['name']
    maximum_capacity = json_data['maximum_capacity']
    id = json_data['id']

    location = get_db().execute(
        'SELECT p.id, name, maximum_capacity, author_id'
        ' FROM location p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if location is None:
        abort(404, "Location id {0} doesn't exist.".format(id))

    check_author=True
    if check_author and location['author_id'] != g.user['id']:
        abort(403)

    if not name:
        abort(400, 'Name is required.')

    if not maximum_capacity:
        abort(400, 'Maximum capacity is required.')

    db = get_db()
    db.execute(
        'UPDATE location SET name = ?, maximum_capacity = ?'
        ' WHERE id = ?',
        (name, maximum_capacity, id)
    )
    db.commit()
    return jsonify(message='Location updated succesfully')