"""Module for film resources"""

from flask import request, jsonify
from flask_restful import Resource
from marshmallow import ValidationError
from sqlalchemy import desc
from flask_login import current_user, login_required

from app import db, app
from app.models import Film, Director, Genre, User
from app.schemas import FilmSchema

film_schema = FilmSchema()
ROWS_PER_PAGE = 10


class FilmListResource(Resource):
    """Film list API"""

    @staticmethod
    def get():
        """
        Get films
        Filter by: director, genre, year_from, year_to
        Partial search by name
        """
        page = request.args.get('page', default=1, type=int)
        director = request.args.get('director', type=str)
        genre = request.args.get('genre', type=str)
        year_from = request.args.get('year_from', type=str)
        year_to = request.args.get('year_to', type=str)
        search = request.args.get('search', type=str)
        sort_rate = request.args.get('sort_rate', default='desc', type=str)
        sort_date = request.args.get('sort_date', default='desc', type=str)

        films = Film.query

        # Filter by director
        if director:
            if director == 'unknown':
                films = films.filter(Film.director_id.is_(None))
            else:
                searched_director = Director.query \
                    .filter(Director.first_name.ilike(f"{director[:director.index(' ')]}")) \
                    .filter(Director.last_name.ilike(f"{director[director.index(' ') + 1:]}")) \
                    .first()
                if not searched_director:
                    return {"Error": "Wrong director name"}, 404
                else:
                    films = films.filter(Film.director == searched_director)

        # Filter by genre
        if genre:
            searched_genre = Genre.query.filter(
                Genre.name.ilike(f"{genre}")).first()
            if not searched_genre:
                return {"Error": "Wrong genre name"}, 404
            else:
                films = films.filter(Film.genres.contains(searched_genre))

        # Filter by year_from, year_to
        if year_from:
            films = films.filter(Film.release_date >= f"{year_from}-01-01")
        if year_to:
            films = films.filter(Film.release_date <= f"{year_to}-12-31")

        # Search by name of film
        if search:
            films = films.filter(Film.name.ilike(f"%{search}%"))

        # Sorting
        if sort_rate == 'asc' and sort_date == 'asc':
            films = films.order_by(Film.rate, Film.release_date)
        elif sort_rate == 'desc' and sort_date == 'asc':
            films = films.order_by(Film.rate.desc(), Film.release_date)
        elif sort_rate == 'asc' and sort_date == 'desc':
            films = films.order_by(Film.rate, Film.release_date.desc())
        elif sort_rate == 'desc' and sort_date == 'desc':
            films = films.order_by(Film.rate.desc(), Film.release_date.desc())

        # Paginate and reformat
        films = films.paginate(page=page, per_page=ROWS_PER_PAGE)
        paginated_films = films.items
        film_list = []
        for film in paginated_films:
            # director = Director.query.filter(director_id=film.director_id).first()
            if not film.director_id:
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
        return jsonify(200, film_list)

    @staticmethod
    @login_required
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
    @login_required
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
    @login_required
    def delete(film_id) -> Resource:
        """Delete film by id"""
        film = Film.query.get_or_404(film_id)
        db.session.delete(film)
        db.session.commit()
        return jsonify({
            "status": 200,
            "reason": "Film is deleted"
        })
