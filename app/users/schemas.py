from .model import User
from .. import ma
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        load_instance = True
        exclude = ('id',)
    include_fk = True