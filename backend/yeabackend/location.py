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

    (name, maximum_capacity) = get_fields(request.get_json())

    db = get_db()
    db.execute(
        'INSERT INTO location (name, maximum_capacity, author_id)'
        ' VALUES (?, ?, ?)',
        (name, maximum_capacity, g.user['id'])
    )
    db.commit()
    return jsonify(created=True,
                   message='Location created succesfully'), 201

@bp.route('/<int:id>', methods=['PUT','DELETE'])
def location(id):
    
    login_required()

    get_location(id)

    message = ''

    if request.method == 'PUT':
        (name, maximum_capacity) = get_fields(request.get_json())
        
        db = get_db()
        db.execute(
            'UPDATE location SET name = ?, maximum_capacity = ?'
            ' WHERE id = ?',
            (name, maximum_capacity, id)
        )
        db.commit()

        message = 'Location updated succesfully.'
    else:
        db = get_db()
        db.execute('DELETE FROM location WHERE id = ?', (id,))
        db.commit()

        message = 'Location deleted succesfully.'
    return jsonify(message=message)

def get_location(id, check_author=True):
    location = get_db().execute(
        'SELECT p.id, name, maximum_capacity, author_id'
        ' FROM location p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if location is None:
        abort(404, "Location id {0} doesn't exist.".format(id))

    if check_author and location['author_id'] != g.user['id']:
        abort(403)

    return location

def get_fields(json_data):

    fields = ['name', 'maximum_capacity']

    for field in fields:
        if field not in json_data:
            abort(400, 'Missing field: {0}.'.format(field))

    name = json_data['name']
    maximum_capacity = json_data['maximum_capacity']

    if not name:
        abort(400, 'Name is required.')

    if not maximum_capacity:
        abort(400, 'Maximum capacity is required.')

    return (name, maximum_capacity)