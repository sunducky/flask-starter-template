from flask import Blueprint, jsonify, request
from flask_marshmallow import pprint


from .model import Auth
from ..users.model import User
from .schemas import AuthSchema
from ..users.schemas import UserSchema
from .dto import NewUserDTO

authentication = Blueprint('authentication', __name__)

@authentication.post('/login')
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    auth = Auth.get_by_email(email)
    print(auth.password)
    if auth and auth.verify_password(password):
        # get token
        token = auth.generate_token()
        data = AuthSchema().dump(auth)
        data['token'] = token
        return jsonify(data), 200
    else:
        return jsonify({'message': 'Login failed'}), 401


@authentication.post('/signup')
def signup():
    # data = request.json
    data = NewUserDTO().load(request.json) #validating the data
    auth = Auth(**data)
    user = User(**data)
    user.auth = auth
    auth.save()
    user.save()
    data = Auth.get_by_email(auth.email)
    print(data)
    return jsonify(AuthSchema().dump(data)), 200
