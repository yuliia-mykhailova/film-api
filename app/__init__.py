"""Module for app initialization"""

import logging
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_login import LoginManager
from flask_swagger_ui import get_swaggerui_blueprint

from app.swagger import swaggerui_blueprint

app = Flask(__name__)
app.secret_key = '1234'
app.config.from_object("app.config.Config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
app.register_blueprint(swaggerui_blueprint)
login_manager.init_app(app)
logging.basicConfig(level=logging.INFO, filename="film_api.log", filemode="a",
                    format='%(asctime)s:%(levelname)s:%(message)s')


api = Api(app)


@app.route('/static/<path:path>')
def send_static(path):
    """Swagger redirection"""
    return send_from_directory('static', path)
