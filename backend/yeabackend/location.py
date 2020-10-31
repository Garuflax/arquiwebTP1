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

from yeabackend.db import get_db

bp = Blueprint('location', __name__, url_prefix='/location')

@bp.route('/create', methods=['POST'])
@jwt_required
def create():

    user_id = get_jwt_identity()

    (name, maximum_capacity, latitude, longitude) = get_fields(request.get_json())

    db = get_db()
    db.execute(
        'INSERT INTO location (name, maximum_capacity, latitude, longitude, author_id)'
        ' VALUES (?, ?, ?, ?, ?)',
        (name, maximum_capacity, latitude, longitude, user_id)
    )
    db.commit()
    return jsonify(created=True,
                   message='Location created succesfully'), 201

@bp.route('/<int:id>', methods=['GET','PUT','DELETE'])
@jwt_required
def location(id):

    if request.method == 'PUT':
        get_location(id)
        (name, maximum_capacity, latitude, longitude) = get_fields(request.get_json())
        
        db = get_db()
        db.execute(
            'UPDATE location SET name = ?, maximum_capacity = ?, latitude = ?, longitude = ?'
            ' WHERE id = ?',
            (name, maximum_capacity, latitude, longitude, id)
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
        people_inside = location['people_inside'],
        latitude = location['latitude'],
        longitude = location['longitude'],
        author_id=location['author_id'],
        id=location['id'],
    )

@bp.route('/all', methods=['GET'])
@jwt_required
def all():

    locations = []
    c = get_db().cursor()
    c.execute('SELECT * FROM location')

    for row in c:
        locations.append(dict(
            name=row['name'],
            maximum_capacity=row['maximum_capacity'],
            people_inside = row['people_inside'],
            latitude = row['latitude'],
            longitude = row['longitude'],
            author_id=row['author_id'],
            id=row['id']
        ))
        

    return jsonify(locations=locations)

def user_is_owner(location_id):

    user_id = get_jwt_identity()

    location = get_db().execute(
        'SELECT p.id, name, maximum_capacity, author_id'
        ' FROM location p JOIN user u ON p.author_id = u.id'
        ' WHERE p.id = ?',
        (location_id,)
    ).fetchone()

    return location['author_id'] == user_id


@bp.route("/<int:id>/qrcode", methods=["GET"])
@jwt_required
def get_qrcode(id):
    if user_is_owner(id):
        return send_file(QRcode.qrcode(id, mode="raw"), mimetype="image/png")

def get_location(id, check_author=True):

    user_id = get_jwt_identity()

    location = get_db().execute(
        'SELECT p.id, name, maximum_capacity, author_id, people_inside, latitude, longitude'
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

    fields = ['name', 'maximum_capacity', 'latitude', 'longitude']

    for field in fields:
        if field not in json_data:
            abort(400, 'Missing field: {0}.'.format(field))

    name = json_data['name']
    maximum_capacity = json_data['maximum_capacity']
    latitude = json_data['latitude']
    longitude = json_data['longitude']

    if not name:
        abort(400, 'Name is required.')

    if not maximum_capacity:
        abort(400, 'Maximum capacity is required.')

    if not latitude:
        abort(400, 'Latitude is required.')

    if not longitude:
        abort(400, 'Longitude is required.')

    return (name, maximum_capacity, latitude, longitude)

