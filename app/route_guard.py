from jwt import ExpiredSignatureError, InvalidSignatureError

from flask import jsonify, request
import jwt
import os


from functools import wraps

secret = os.urandom(24)

def requires_user_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"message": "Missing Authorization Header"}), 401
        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, secret, algorithms=["HS256"])
            user_id = payload['sub']
            role = payload['role']
            # check role
            if role != 'user':
                return jsonify({"message": "Unauthorized to perform action"}), 401
        except ExpiredSignatureError:
            return jsonify({"message": "Expired or Invalid Token"}), 401
        except InvalidSignatureError:
            return jsonify({"message": "Malformed Token"}), 401
        return f(user_id, *args, **kwargs)
    return decorated

def required_admin_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header:
            return jsonify({"message": "Missing Authorization Header"}), 401
        try:
            token = auth_header.split(' ')[1]
            payload = jwt.decode(token, secret, algorithms=["HS256"])
            user_id = payload['sub']
            role = payload['role']
            # check role
            if role != 'admin':
                return jsonify({"message": "Unauthorized to perform action"}), 401
        except ExpiredSignatureError:
            return jsonify({"message": "Expired or Invalid Token"}), 401
        except InvalidSignatureError:
            return jsonify({"message": "Malformed Token"}), 401
        return f(user_id, *args, **kwargs)
    return decorated