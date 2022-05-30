# from app.auth.model import *
# from app.users.model import *
# from app.auth.schemas import *

from pprint import pprint
from .models import *
from .schemas import *

from app import db

# Fetch all data from the database
# users = User.query.all()
# auths = Auth.query.all()


# drop all tables and recreate them
db.drop_all()
db.create_all()


# Save data to the database
# Create new Auth object
auth = Auth(
    password='password',
    email='test@test.com',
    role='admin'
)
auth.save()
# Create new User object
user = User(
    firstname='test',
    lastname='test',
    email=auth.email,
    phone='1234567890',
    avatar='default.jpg',
    auth=auth
)
user.save()

# Fetch first auth object from the database
xauth = Auth.query.first()
print(xauth.user)
print('----------------')
print(AuthSchema().dump(xauth))
# print(auth.user)