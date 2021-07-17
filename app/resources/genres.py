"""Module for genre resources"""

from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from flask_login import current_user, login_required

from app.models import Genre, db
from app.schemas import GenreSchema

genre_schema = GenreSchema()


class GenreListResource(Resource):
    """Genre list API"""

    @staticmethod
    def get():
        """Get genres"""
        genres = db.session.query(Genre).all()
        return genre_schema.dump(genres, many=True), 200

    @staticmethod
    @login_required
    def post():
        """Add genre"""
        try:
            genre = genre_schema.load(request.json, session=db.session)
        except ValidationError as error:
            return {"Error": str(error)}, 400

        db.session.add(genre)
        db.session.commit()
        return genre_schema.dump(genre), 201


class GenreResource(Resource):
    """Genre API"""

    @staticmethod
    def get(genre_id):
        """Get genre by id"""
        genre = Genre.query.get_or_404(genre_id)
        return genre_schema.dump(genre)

    @staticmethod
    @login_required
    def put(genre_id):
        """Update a genre"""

        genre = db.session.query(Genre).filter_by(genre_id=genre_id).first()
        if not genre:
            return {"Error": "Genre was not found"}, 404

        try:
            genre = genre_schema.load(
                request.json, instance=genre, session=db.session
            )
        except ValidationError as error:
            return {"Error": str(error)}, 400

        db.session.add(genre)
        db.session.commit()
        return genre_schema.dump(genre), 200

    @staticmethod
    @login_required
    def delete(genre_id):
        """Delete genre by id"""
        genre = Genre.query.get_or_404(genre_id)
        db.session.delete(genre)
        db.session.commit()
        return jsonify({
            "status": 200,
            "reason": "Genre is deleted"
        })
