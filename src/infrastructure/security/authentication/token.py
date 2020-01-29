import datetime
import sqlite3

import jwt
from flask import Blueprint, request, make_response
from flask_restplus import Api, Resource
from werkzeug.security import check_password_hash
from src import app, logger
from src.constants import sql_object

mod = Blueprint('token', __name__)
auth1 = Api(mod)


@auth1.route('/token')
class Token(Resource):
    def get(self):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        # Check if user is expired or not
        logger.info("Check if user is expired or not")

        # Create database connection with sqlite database
        conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_FILE'])
        cursor = conn.cursor()
        fetch_query = sql_object.GET_USER_PASSWORD.format(auth.username)
        logger.info("GET_USER_PASSWORD query %s", fetch_query)

        # Execute query and fetch result
        cursor.execute(fetch_query)
        result_set = cursor.fetchall()

        if result_set.__len__() > 0 and result_set[0].__len__() > 0 and check_password_hash(result_set[0][0], auth.password):
            token = jwt.encode({'USERNAME': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=app.config['TOKEN_EXPIRY_MINUTES'])}, app.config['SECRET_KEY'])
            return make_response({'token': token.decode('UTF-8')}, 200, {'WWW-Authenticate': 'Basic realm="Login required!"'})
        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
