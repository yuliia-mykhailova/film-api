from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError

from app.models import User, db
from app.schemas import UserSchema

user_schema = UserSchema()


class UserListResource(Resource):
    """User list API"""

    @staticmethod
    def get():
        """Get users"""
        users = db.session.query(User).all()
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
        return user_schema.dump(user), 201


class UserResource(Resource):
    """User API"""

    @staticmethod
    def get(user_id):
        """Get user by id"""
        user = User.query.get_or_404(user_id)
        return user_schema.dump(user)

    @staticmethod
    def put(user_id):
        """Update a user"""

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
        return user_schema.dump(user), 200

    @staticmethod
    def delete(user_id):
        """Delete user by user_id"""
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return jsonify({
            "status": 200,
            "reason": "User is deleted"
        })
