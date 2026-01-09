from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os


def create_app(config_class: type = Config):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_class)


    return app
