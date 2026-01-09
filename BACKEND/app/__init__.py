from flask import Flask
from app.config import Config
from app.extensions import db
import os


def create_app(config_class: type = Config):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_class)
    db.init_app(app)

    @app.get("/")
    def home():
        return "Welcome flask"


    return app
