from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api
from flask_login import LoginManager


app = Flask(__name__)
app.secret_key = '1234'
app.config.from_object("app.config.Config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

api = Api(app)


@app.route("/")
def hello_world():
    return jsonify(hello="world")