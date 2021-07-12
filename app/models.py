"""Module for project models"""

from datetime import datetime

from app import db


class User(db.Model):
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)


class Director(db.Model):
    __tablename__ = "director"

    director_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def __init__(self, **kwargs):
        super(Director, self).__init__(**kwargs)


class Genre(db.Model):
    __tablename__ = "genre"

    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, **kwargs):
        super(Genre, self).__init__(**kwargs)


class Film(db.Model):
    __tablename__ = "film"

    film_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.DateTime, default=datetime.now())
    description = db.Column(db.Text, nullable=True)
    rate = db.Column(db.Numeric(2, 2), nullable=False)
    poster = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    director_id = db.Column(db.Integer, db.ForeignKey("director.director_id"), nullable=True)
    
    def __init__(self, **kwargs):
        super(Film, self).__init__(**kwargs)


class FilmGenre(db.Model):
    __tablename__ = "film_genre"

    film_id = db.Column(db.Integer,  db.ForeignKey("film.film_id"), primary_key=True)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.genre_id"), primary_key=True)
    
    def __init__(self, **kwargs):
        super(FilmGenre, self).__init__(**kwargs)
