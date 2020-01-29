import json
import sqlite3
from datetime import datetime
from functools import wraps
import jwt
from flask import request
from src import app, logger
from src.constants import sql_object


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


def has_user_expired(username):
    # Check if user is expired or not
    logger.info("Check if user is expired or not")

    # Create database connection with sqlite database
    conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_FILE'])
    cursor = conn.cursor()
    fetch_query = sql_object.GET_USER_DETAIL_BY_NAME.format(username, datetime.now())
    logger.info("GET_CAR_PART_CATEGORIES query %s", fetch_query)

    # Execute query and fetch result
    cursor.execute(fetch_query)
    result_set = cursor.fetchall()
    return result_set.__len__() == 0 if True else False