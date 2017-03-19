from flask import url_for
from app.exceptions import ValidationError
from . import db
from flask_sqlalchemy import SQLAlchemy


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(8), nullable=False)
    password = db.Column(db.String(32), nullable=False)
    tasks = db.relationship('Task', backref='user', lazy='dynamic')

    def __repr__(self):
        return '<User {}>'.format(self.username)

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
            'url' : url_for('api.get_task', id=self.id, _external=True),
            'user' : url_for('api.get_user', id=self.user_id, _external=True),
            'title' : self.title,
            'done' : self.done
        }
        return json_task
