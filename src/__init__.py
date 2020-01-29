import logging
import os
from configparser import SafeConfigParser

from flask import Flask
from flask_cors import CORS

from src.infrastructure.logging.initialize import setup_logging

config = SafeConfigParser()
config.read('config.ini')

app = Flask(__name__)
CORS(app)

app.config['SECRET_KEY'] = config.get('app', 'SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = config.get('db', 'SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_FILE'] = os.path.join(os.path.abspath(__file__ + '/../'), config.get('db', 'SQLALCHEMY_DATABASE_FILE'))
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['TOKEN_EXPIRY_MINUTES'] = 30

# Initialise logging
setup_logging()
logger = logging.getLogger(__name__)
