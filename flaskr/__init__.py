from dotenv import load_dotenv
import os

load_dotenv('config.env')

from flask import Flask
from .apis import detect
from .utils.download_model import download_model

def create_app(test_config = None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = 'dev'
    )

    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    try:
        os.makedirs("tmp")
    except OSError:
        pass

    MODEL_URL = os.getenv("MODEL_URL")
    MODEL_DIR = "flaskr/model"

    if not os.path.exists(MODEL_DIR):
        download_model(MODEL_URL, MODEL_DIR)

    app.register_blueprint(detect.dt)

    return app