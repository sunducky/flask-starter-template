from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate
import os

# Configure app
app = Flask(__name__, )
app.config.from_object('config')
db = SQLAlchemy(app)
ma = Marshmallow(app)
secret = os.urandom(24)
migrate = Migrate(app, db)


# Register controllers
from app.auth.controller import authentication
app.register_blueprint(authentication, url_prefix='/auth')
# 
from app.users.controller import user
app.register_blueprint(user, url_prefix='/user')
#

# Error handlers
from .error_handlers import *