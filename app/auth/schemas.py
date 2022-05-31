from .. import ma
from .model import Auth        
class AuthSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Auth
        exclude = ('password', 'created_at', 'updated_at', 'email')
        load_instance = True
    user = ma.Nested('UserSchema', many=False)
