from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify
)
from flask_jwt_extended import (
    create_access_token, create_refresh_token, get_jwt_identity,
    verify_jwt_in_request, verify_jwt_refresh_token_in_request,
    jwt_required
)

from werkzeug.exceptions import abort

#from yeabackend.auth import login_required
from yeabackend.db import get_db

bp = Blueprint('location', __name__, url_prefix='/location')

@bp.route('/create', methods=['POST'])
@jwt_required
def create():

    user_id = get_jwt_identity()
    #login_required()

    (name, maximum_capacity) = get_fields(request.get_json())

    db = get_db()
    db.execute(
        'INSERT INTO location (name, maximum_capacity, author_id)'
        ' VALUES (?, ?, ?)',
        (name, maximum_capacity, user_id)
    )
    db.commit()
    return jsonify(created=True,
                   message='Location created succesfully'), 201

@bp.route('/<int:id>', methods=['GET','PUT','DELETE'])
@jwt_required
def location(id):
    
    #login_required()

    if request.method == 'PUT':
        get_location(id)
        (name, maximum_capacity) = get_fields(request.get_json())
        
        db = get_db()
        db.execute(
            'UPDATE location SET name = ?, maximum_capacity = ?'
            ' WHERE id = ?',
            (name, maximum_capacity, id)
        )
        db.commit()

        return jsonify(message='Location updated succesfully.')
    elif request.method == 'DELETE':
        get_location(id)

        db = get_db()
        db.execute('DELETE FROM location WHERE id = ?', (id,))
        db.commit()

        return jsonify(message='Location deleted succesfully.')
    
    location = get_location(id, False)
    return jsonify(name=location['name'],
        maximum_capacity=location['maximum_capacity'],
        author_id=location['author_id'],
        id=location['id'],
        people_inside = location['people_inside']
    )

@bp.route('/all', methods=['GET'])
@jwt_required
def all():
    
    #login_required()

    locations = []
    c = get_db().cursor()
    c.execute('SELECT * FROM location')

    for row in c:
        locations.append(dict(
            name=row['name'],
            maximum_capacity=row['maximum_capacity'],
            author_id=row['author_id'],
            id=row['id']
        ))
        

    return jsonify(locations=locations)

def get_location(id, check_author=True):

    user_id = get_jwt_identity()

    location = get_db().execute(
        'SELECT p.id, name, maximum_capacity, author_id, people_inside'
        ' FROM location p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (id,)
    ).fetchone()

    if location is None:
        abort(404, "Location id {0} doesn't exist.".format(id))

    if check_author and location['author_id'] != user_id:
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