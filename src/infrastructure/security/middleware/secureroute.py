import json
from functools import wraps

import jwt
from flask import request

from src import app
from src.utilities.utilities import has_user_expired


def secureroute(*argument):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            token = request.headers.get("authorization", None)
            if not token:
                return json.dumps(['No authorization token provied']), 401, {'Content-type': 'application/json'}

            try:
                result = jwt.decode(token, app.config['SECRET_KEY'])
                app.config['USERNAME'] = result.get('USERNAME') if result.get('USERNAME') else 'Anonymous'

                # Check if user is not expired
                is_user_expired = has_user_expired(app.config['USERNAME'])
                if is_user_expired:
                    return json.dumps(['user account expired']), 401, {'Content-type': 'application/json'}
            except Exception as e:
                return json.dumps(['invalid authorization token']), 401, {'Content-type': 'application/json'}
            return function(*args, **kwargs)
        return wrapper
    return decorator
