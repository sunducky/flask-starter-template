from flask import jsonify
from .. import db, app
import datetime
import bcrypt
import jwt

class Auth(db.Model):
    __tablename__ = 'authentication'
    id = db.Column(db.Integer, primary_key=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(120), nullable=False) # admin, user
    created_at = db.Column(db.DateTime, nullable=False, default=db.func.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=db.func.now(), onupdate=db.func.now())
    user = db.relationship('User', back_populates='auth', lazy=True, uselist=False)
    token = ''

    def __init__(self, **kwargs) -> None:
        self.email = kwargs.get('email')
        self.password = kwargs.get('password')
        self.role = kwargs.get('role')
        super().__init__()

    def save(self):
        try:
            self.hash_password()
            db.session.add(self)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({'message': 'An error occurred'}), 500

    @classmethod
    def get_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter_by(email=email).first()
    
    @classmethod
    def get_by_role(cls, role):
        return cls.query.filter_by(role=role).all()
    
    def hash_password(self):
        self.password = bcrypt.hashpw(self.password.encode('utf8'), bcrypt.gensalt()).decode('utf8')

    def verify_password(self, password):
        return bcrypt.checkpw(password.encode('utf8'), self.password.encode('utf8'))

    def generate_token(self):
        try:
            payload = {
                'exp': app.config.get('JWT_REFRESH_TOKEN_EXPIRES'),
                'iat': datetime.datetime.utcnow(),
                'sub': self.id,
                'role': self.role
            }
            return jwt.encode(
                payload,
                app.config.get('JWT_SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e