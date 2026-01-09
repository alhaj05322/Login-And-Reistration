from flask import Flask
from .config import Config
from .extensions import db
import os


def create_app(config_class: type = Config):

    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object(config_class)
     #create the instnce folder
    os.makedirs(app.instance_path,exist_ok=True)
    db.init_app(app)

    @app.get("/")
    def home():
        return "Welcome flask"


    return app
