"""Module for user resources"""

from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from flask_login import current_user, login_required

from app.admin_required import admin_required
from app.models import User
from app import app, db
from app.schemas import UserSchema

user_schema = UserSchema()


class UserListResource(Resource):
    """User list API"""

    @staticmethod
    @login_required
    @admin_required
    def get():
        """Get users"""
        users = db.session.query(User).all()
        app.logger.info("Get all users")
        return user_schema.dump(users, many=True), 200

    @staticmethod
    def post():
        """Add user"""
        try:
            user = user_schema.load(request.json, session=db.session)
        except ValidationError as error:
            return {"Error": str(error)}, 400

        db.session.add(user)
        db.session.commit()
        app.logger.info(f"Added user id: {user.user_id} by user with id: {current_user.get_id()}")
        return user_schema.dump(user), 201


class UserResource(Resource):
    """User API"""

    @staticmethod
    @login_required
    def get(user_id):
        """Get user by id"""
        if current_user.user_id == user_id or current_user.is_admin:
            user = User.query.get_or_404(user_id)
            app.logger.info(f"Get user id: {user_id} by user with id: {current_user.get_id()}")
            return user_schema.dump(user)
        return {"Error": "You don't have permission to do that"}, 403

    @staticmethod
    @login_required
    def put(user_id):
        """Update a user"""
        if current_user.user_id == user_id or current_user.is_admin:
            user = db.session.query(User).filter_by(user_id=user_id).first()
            if not user:
                return {"Error": "User was not found"}, 404

            try:
                user = user_schema.load(
                    request.json, instance=user, session=db.session
                )
            except ValidationError as error:
                return {"Error": str(error)}, 400

            db.session.add(user)
            db.session.commit()
            app.logger.info(f"Updated user id: {user_id} by user with id: {current_user.get_id()}")
            return user_schema.dump(user), 200
        return {"Error": "You don't have permission to do that"}, 403

    @staticmethod
    @login_required
    def delete(user_id):
        """Delete user by id"""
        if current_user.user_id == user_id or current_user.is_admin:
            user = User.query.get_or_404(user_id)
            db.session.delete(user)
            db.session.commit()
            app.logger.info(f"Deleted user id: {user_id} by user with id: {current_user.get_id()}")
            return jsonify({
                "status": 200,
                "reason": "User is deleted"
            })
        return {"Error": "You don't have permission to do that"}, 403
