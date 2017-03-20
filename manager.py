#!/usr/bin/env python
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://neo:1023@localhost/todo'
db = SQLAlchemy(app)





if __name__ == '__main__':
    app.run()