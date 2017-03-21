from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from config import config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    db.init_app(app)

    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint)

    # add index
    from .index import add_index
    add_index(app, app.route("/"))

    return app
