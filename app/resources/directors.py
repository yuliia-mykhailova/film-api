"""Module for director resources"""

from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from flask_login import current_user, login_required

from app.admin_required import admin_required
from app.models import Director, db
from app.schemas import DirectorSchema

director_schema = DirectorSchema()


class DirectorListResource(Resource):
    """Director list API"""

    @staticmethod
    def get():
        """Get directors"""
        directors = db.session.query(Director).all()
        return director_schema.dump(directors, many=True), 200

    @staticmethod
    @login_required
    @admin_required
    def post():
        """Add director"""
        try:
            director = director_schema.load(request.json, session=db.session)
        except ValidationError as error:
            return {"Error": str(error)}, 400

        db.session.add(director)
        db.session.commit()
        return director_schema.dump(director), 201


class DirectorResource(Resource):
    """Director API"""

    @staticmethod
    def get(director_id):
        """Get director by id"""
        director = Director.query.get_or_404(director_id)
        return director_schema.dump(director)

    @staticmethod
    @login_required
    @admin_required
    def put(director_id):
        """Update a director"""

        director = db.session.query(Director).filter_by(director_id=director_id).first()
        if not director:
            return {"Error": "Director was not found"}, 404

        try:
            director = director_schema.load(
                request.json, instance=director, session=db.session
            )
        except ValidationError as error:
            return {"Error": str(error)}, 400

        db.session.add(director)
        db.session.commit()
        return director_schema.dump(director), 200

    @staticmethod
    @login_required
    @admin_required
    def delete(director_id):
        """Delete director by id"""
        director = Director.query.get_or_404(director_id)
        db.session.delete(director)
        db.session.commit()
        return jsonify({
            "status": 200,
            "reason": "Director is deleted"
        })
