from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, Response, jsonify, session, send_file
)
from werkzeug.exceptions import abort

from yeabackend.auth import login_required
from yeabackend.db import get_db

from yeabackend.location import bp as location_bp

# from flask_qrcode import QRcode

bp = Blueprint('check', __name__)

@bp.route('/checkin', methods=['POST'])

def checkin():
    location_id = request.get_json()["location_id"]

    db = get_db()
    location = db.execute(
        "SELECT * FROM location WHERE id = ?",
        location_id).fetchone()

    if location is None:
        abort(404, "Location doesn't exist.")

    db.execute(
        f"UPDATE location SET people_inside = people_inside + 1 WHERE id = {location_id}"
    )

    # Guardo en la sesión, el local donde se encuentra la persona

    db.commit()

    return ('')

@bp.route('/checkout', methods=['POST'])
def checkout():

    location_id = request.get_json()["location_id"]

    # if location_id != location donde se encontraba la persona: 
    #     abort(404, "Not in location.")

    db = get_db()
    db.execute("UPDATE location SET people_inside = people_inside -1 WHERE id = ?", location_id)

    db = get_db()
    db.commit()

    return ('')