from marshmallow import Schema, fields, validates
import re
from .model import Auth
from ..users.model import User

class NewUserDTO(Schema):
    email = fields.Email(required=True)
    password = fields.Str(required=True)
    role = fields.Str(required=True)
    firstname = fields.Str(required=True)
    lastname = fields.Str(required=True)
    phone = fields.Str(required=True)
    avatar = fields.Str(required=False)

    @validates('phone')
    def validate_phone(self, value):
        # check if phone number exists
        if User.get_by_phone(value):
            raise ValueError('Phone number already exists')

        import phonenumbers
        try:
            phone = phonenumbers.parse(value, None)
            if not phonenumbers.is_valid_number(phone):
                raise ValueError('Invalid phone number')
        except:
            raise ValueError('Invalid phone number')

    
    @validates('firstname')
    def validate_firstname(self, value):
        if len(value) < 2:
            raise ValueError('First name must be at least 2 characters')
    
    @validates('lastname')
    def validate_lastname(self, value):
        if len(value) < 2:
            raise ValueError('Last name must be at least 2 characters')

    # Validate the password
    @validates('password')
    def validate_password(self, value):
        if len(value) < 6:
            raise ValueError("Password must be at least 6 characters long")
        # check if password contains at least one upper case letter
        if not any(char.isupper() for char in value):
            raise ValueError("Password must contain at least one upper case letter")
        # check if password contains at least one lower case letter
        if not any(char.islower() for char in value):
            raise ValueError("Password must contain at least one lower case letter")
        # check if password contains at least one digit
        if not any(char.isdigit() for char in value):
            raise ValueError("Password must contain at least one digit")
        # check if password contains at least one special character
        if not any(char in '!@#$%^&*()_+-=[]{};:,./<>?\|' for char in value):
            raise ValueError("Password must contain at least one special character")
    
    @validates('role')
    def validate_role(self, value):
        if value not in ['admin', 'user']:
            raise ValueError("Role must be either 'admin' or 'user'")
    
    @validates('email')
    def validate_email(self, value):
        if re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', value) is None:
            raise ValueError("Email is not valid")
        if Auth.query.filter_by(email=value).first():
            raise ValueError("Email already in use")