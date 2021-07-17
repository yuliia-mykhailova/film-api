"""Module for project schemas"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema

from app.models import User, Director, Genre, Film


class UserSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = User
        exclude = ["user_id"]
        load_instance = True
        load_only = ("password",)


class DirectorSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Director
        load_instance = True
        include_fk = True


class GenreSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Genre
        load_instance = True


class FilmSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Film
        exclude = ["film_id"]
        load_instance = True
        include_fk = True

