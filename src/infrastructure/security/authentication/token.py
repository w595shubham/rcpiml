import datetime

import jwt
from flask import Blueprint, request, make_response
from flask_restplus import Api, Resource
from werkzeug.security import check_password_hash
from src import app

mod = Blueprint('token', __name__)
auth = Api(mod)


@auth.route('/token')
class Token(Resource):
    def get(self):
        auth = request.authorization

        if not auth or not auth.username or not auth.password:
            return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})

        if app.config['USERNAME'] == auth.username and check_password_hash(app.config['PASSWORD'], auth.password):
            token = jwt.encode(
                {'USERNAME': auth.username, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
                app.config['SECRET_KEY'])

            return make_response({'token': token.decode('UTF-8')}, 200,
                                 {'WWW-Authenticate': 'Basic realm="Login required!"'})

        return make_response('Could not verify', 401, {'WWW-Authenticate': 'Basic realm="Login required!"'})
