from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_restful import Api


app = Flask(__name__)
app.config.from_object("app.config.Config")
db = SQLAlchemy(app)
migrate = Migrate(app, db)

api = Api(app)


@app.route("/")
def hello_world():
    return jsonify(hello="world")