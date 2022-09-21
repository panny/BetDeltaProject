from flask import Flask
from BetDelta.blueprints.pages import page
from BetDelta.api.api import api

def create_app():
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_object('config.settings')
    app.config.from_pyfile('settings.py', silent=True)

    app.register_blueprint(page)
    app.register_blueprint(api)

    return app