"""Module for film resources"""

from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy import desc

from app import db, app
from app.models import Film, Director, Genre, User
from app.schemas import FilmSchema

film_schema = FilmSchema()


class FilmListResource(Resource):
    """Film list API"""

    @staticmethod
    def get():
        """Get films"""
        films = Film.query.all()
        film_list = []
        for film in films:
            director = Director.query.filter_by(director_id=film.director_id).first()
            if director is None:
                director = 'unknown'
            else:
                director = film.director_id
            film_genre = []
            if film.genres:
                for genre in film.genres:
                    film_genre.append(genre.name)
            film_list.append({
                'film_id': film.film_id,
                'name': film.name,
                'rate': film.rate,
                'release_date': film.release_date,
                'description': film.description,
                'director': director,
                'user': film.user_id,
                'film_genres': film_genre
            })
        return jsonify(film_list)

    @staticmethod
    def post():
        """Add film"""
        data = request.json
        film = Film()

        film.user_id = data["user_id"]
        film.rate = data["rate"]
        film.description = data["description"]
        film.name = data["name"]
        film.poster = data["poster"]
        film.release_date = data["release_date"]
        film.director_id = data["director_id"]
        for genre_id in data["genres"]:
            film.genres.append(Genre.query.get_or_404(genre_id))
        try:
            db.session.add(film)
            db.session.commit()
        except ValidationError as error:
            return {"Error": str(error)}, 400

        return film_schema.dump(film), 201


class FilmResource(Resource):
    """Film API"""

    @staticmethod
    def get(film_id):
        """Get film by id"""
        film = Film.query.get_or_404(film_id)
        return film_schema.dump(film)

    @staticmethod
    def put(film_id):
        """Update a film"""

        film = Film.query.filter_by(film_id=film_id).first()
        data = request.json

        if not film:
            return {"Error": "Film was not found"}, 404

        film.user_id = data["user_id"]
        film.rate = data["rate"]
        film.description = data["description"]
        film.name = data["name"]
        film.poster = data["poster"]
        film.release_date = data["release_date"]
        film.director_id = data["director_id"]
        for genre_id in data["genres"]:
            film.genres.append(Genre.query.get_or_404(genre_id))
        try:
            db.session.add(film)
            db.session.commit()
        except ValidationError as error:
            return {"Error": str(error)}, 400

        return film_schema.dump(film), 201

    @staticmethod
    def delete(film_id) -> Resource:
        """Delete film by id"""
        film = Film.query.get_or_404(film_id)
        db.session.delete(film)
        db.session.commit()
        return jsonify({
            "status": 200,
            "reason": "Film is deleted"
        })