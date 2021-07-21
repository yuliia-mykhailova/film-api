"""Module for login"""

from flask import request, jsonify
from flask_login import login_user, logout_user
from flask_restful import Resource

from app.models import User
from app.auth import load_user


class LoginResource(Resource):
    """Login user"""

    @staticmethod
    def post():
        """Login user"""
        email = request.json['email']
        password = request.json['password']
        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify(
                {"status": 401, "reason": "Wrong email"}
            )
        if password != user.password:
            return jsonify(
                {"status": 401, "reason": "Wrong password"}
            )
        login_user(user)
        return jsonify(
            {"result": 200, "message": "Successful login"}
        )


class LogoutResource(Resource):
    """Logout user"""

    @staticmethod
    def post():
        """Logout user"""
        logout_user()
        return jsonify(
            {"result": 200, "message": "Successful logout"}
        )
