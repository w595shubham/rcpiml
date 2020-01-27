import json
from functools import wraps
import jwt
from flask import request
from src import app


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
            except:
                return json.dumps(['invalid authorization token']), 401, {'Content-type': 'application/json'}
            return function(*args, **kwargs)

        return wrapper

    return decorator
