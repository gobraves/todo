from flask import url_for, current_app
from app.exceptions import ValidationError
from . import db
from . import api
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired, BadSignature
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(8), nullable=False)
    password_hash = db.Column(db.String(32), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def generate_auth_token(self, expiration=600):
        s = Serializer(api.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(api.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None  # valid token, but expired
        except BadSignature:
            return None  # invalid token
        user = User.query.get(data['id'])
        return user

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('confirm') != self.id:
            return False
        self.confirmed = True
        db.session.add(self)
        return True

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def to_json(self):
        json_user = {
            'url': url_for('api.get_user', id=self.id, _external=True),
            'tasks': url_for('api.get_user_tasks', id=self.id, _external=True)
        }
        return json_user


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Intefer, primary_key=True, nullable=False)
    user_id = db.Column(db.Interger, db.ForeignKey(User.id, ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(32), nullable=False)
    done = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return '<Task {}>'.format(self.title)
    
    @staticmethod
    def from_json(task):
        title = task.get('title')
        if title is None or title == '':
            raise ValidationError('task does not have a title')
        return Task(title=title)

    def to_json(self):
        json_task = {
            'url': url_for('api.get_task', id=self.id, _external=True),
            'user': url_for('api.get_user', id=self.user_id, _external=True),
            'title': self.title,
            'done': self.done
        }
        return json_task
