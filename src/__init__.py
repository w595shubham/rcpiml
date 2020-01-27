import logging
from configparser import SafeConfigParser

from flask import Flask
from flask_cors import CORS
from werkzeug.security import generate_password_hash

from src.infrastructure.logging.initialize import setup_logging

config = SafeConfigParser()
config.read('config.ini')

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = config.get('app', 'SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('db', 'SQLALCHEMY_DATABASE_URI')
app.config['USERNAME'] = config.get('app', 'USERNAME')
app.config['PASSWORD'] = generate_password_hash(config.get('app', 'PASSWORD'), method='sha256')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialise logging
setup_logging()
logger = logging.getLogger(__name__)
