from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__, )
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
secret = os.urandom(24)

from app.auth.model import Auth
from app.users.model import User

# 
from app.auth.controller import authentication
app.register_blueprint(authentication, url_prefix='/auth')

from .error_handlers import *