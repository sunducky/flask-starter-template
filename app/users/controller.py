from flask import Blueprint, jsonify, request
from flask_marshmallow import pprint

from app.route_guard import requires_user_auth


from .model import User
from .schemas import UserSchema
from ..users.schemas import UserSchema

user = Blueprint('user', __name__)

# get current logged in user
@user.get('/')
@requires_user_auth
def get_current_user(auth_id):
    user = User.get_by_auth_id(auth_id)
    data = UserSchema().dump(user)
    data['role'] = user.auth.role
    return jsonify(data), 200