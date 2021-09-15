
from hashlib import sha256

from app import db

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField


class User(db.Model):
    user = db.Column(db.String(64), primary_key=True)
    password = db.Column(db.String(64))
    authenticated = False

    def get_id(self) -> str:
        return self.user

    def is_authenticated(self) -> bool:
        return self.authenticated

    def is_active(self) -> bool:
        return True

    def is_anonymous(self) -> bool:
        return False


class LoginForm(FlaskForm):
    user = StringField()
    password = PasswordField()


def find_by_user(user: str) -> User:
    return User.query.filter_by(user=user).first()


def encrypt_password(password: str) -> str:
    return sha256(password).hexdigest()


def check_encrypted_password(hashed: str, not_hashed: str) -> bool:
    return hashed == sha256(not_hashed.encode('utf-8')).hexdigest()
