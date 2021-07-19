"""Module for project models"""

import re
from datetime import datetime

from flask_login import UserMixin
from sqlalchemy.orm import validates

from app import db


class User(db.Model, UserMixin):
    """User model"""
    __tablename__ = "user"

    user_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)

    def get_id(self) -> int:
        """Returns id of user"""
        return self.user_id

    @validates('email')
    def validate_email(self, email):
        """Validate an email address"""
        if not email:
            raise AssertionError('No email address')
        if not re.match(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', email):
            raise AssertionError('Wrong email address format')
        return email

    @validates('password')
    def validate_email(self, password):
        """Validate an email address"""
        if not password:
            raise AssertionError('No password')
        if len(password) < 6:
            raise AssertionError('Too short password')
        return password


class Director(db.Model):
    """Director model"""
    __tablename__ = "director"

    director_id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    def __init__(self, **kwargs):
        super(Director, self).__init__(**kwargs)


class Genre(db.Model):
    """Genre model"""
    __tablename__ = "genre"

    genre_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

    def __init__(self, **kwargs):
        super(Genre, self).__init__(**kwargs)


FilmGenre = db.Table(
    "film_genre",
    db.Column("film_id", db.Integer, db.ForeignKey("film.film_id"), primary_key=True),
    db.Column("genre_id", db.Integer, db.ForeignKey("genre.genre_id"), primary_key=True),
)


class Film(db.Model):
    """Film model"""
    __tablename__ = "film"

    film_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    release_date = db.Column(db.DateTime, default=datetime.now())
    description = db.Column(db.Text, nullable=True)
    rate = db.Column(db.Integer, nullable=False)
    poster = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.user_id"), nullable=False)
    user = db.relationship("User", backref="user_films")
    director_id = db.Column(db.Integer, db.ForeignKey("director.director_id"), nullable=True)
    director = db.relationship("Director", backref="director_films")
    genres = db.relationship("Genre", secondary=FilmGenre, backref="film_genre")

    def __init__(self, **kwargs):
        super(Film, self).__init__(**kwargs)

    @validates('rate')
    def validate_email(self, rate):
        """Validate rate of a film"""
        if not rate:
            raise AssertionError('No rate of film')
        if rate < 0 or rate > 10:
            raise AssertionError('Wrong rate format')
        return rate
