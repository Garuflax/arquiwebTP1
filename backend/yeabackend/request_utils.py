from werkzeug.exceptions import abort

def get_fields(request, fields):
    """Get field values from json of request
    and checking that it has the requested
    fields and are valid.
    """

    if not request.is_json:
        abort(400, 'Missing json.')

    json_data = request.get_json()

    return extract_fields(json_data, fields)

def extract_fields(json_data, fields):
    """Get dictionary fields values as an array.
    In case of missing or invalid field a
    HTTP code 400 is sent.
    """
    values = []
    for field in fields:
        if field not in json_data:
            abort(400, 'Missing field: {0}.'.format(field))
        if not json_data[field]:
            abort(400, 'Invalid field: {0}.'.format(field))
        values.append(json_data[field])
    
    return values