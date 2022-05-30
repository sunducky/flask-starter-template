from flask import jsonify
from .. import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(120), nullable=False)
    lastname = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(120), nullable=False, default='default.jpg')
    auth_id = db.Column(db.Integer, db.ForeignKey('authentication.id'))
    auth = db.relationship('Auth', back_populates='user', lazy=True, uselist=False)
    
    def __init__(self, **kwargs) -> None:
        self.firstname = kwargs.get('firstname')
        self.lastname = kwargs.get('lastname')
        self.email = kwargs.get('email')
        self.phone = kwargs.get('phone')
        self.avatar = kwargs.get('avatar')
        self.auth_id = kwargs.get('auth_id')
        super().__init__()

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({'message': 'An error occurred'}), 500
    
    @classmethod
    def get_by_phone(cls, phone):
        return cls.query.filter_by(phone=phone).first()
    
    @classmethod
    def get_by_auth_id(cls, auth_id):
        return cls.query.filter_by(auth_id=auth_id).first()