from datetime import datetime

def current_datetime():
    return datetime.now()

def current_datetime_string():
    return datetime_to_string(current_datetime())

def string_to_datetime(ts):
    return datetime.strptime(ts, '%Y-%m-%d %H:%M:%S')

def datetime_to_string(ts):
    return ts.strftime('%Y-%m-%d %H:%M:%S')