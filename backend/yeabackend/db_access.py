from flask_jwt_extended import get_jwt_identity
from werkzeug.exceptions import abort

from yeabackend.db import get_db

def get_location(id, check_author=True):

    location = get_db().execute(
        'SELECT * FROM location WHERE id = ?',
        (id,)
    ).fetchone()

    if location is None:
        abort(404, "Location id {0} doesn't exist.".format(id))

    if check_author and location['author_id'] != get_jwt_identity():
        abort(403)

    return location