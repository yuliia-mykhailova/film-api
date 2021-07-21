"""Module for project schemas"""

from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.models import User, Director, Genre, Film


class UserSchema(SQLAlchemyAutoSchema):
    """Schema for User model"""
    class Meta:
        """Meta class"""
        model = User
        exclude = ["user_id"]
        load_instance = True
        load_only = ("password",)


class DirectorSchema(SQLAlchemyAutoSchema):
    """Schema for Director model"""
    class Meta:
        """Meta class"""
        model = Director
        load_instance = True
        include_fk = True


class GenreSchema(SQLAlchemyAutoSchema):
    """Schema for Genre model"""
    class Meta:
        """Meta class"""
        model = Genre
        load_instance = True


class FilmSchema(SQLAlchemyAutoSchema):
    """Schema for Film model"""
    class Meta:
        """Meta class"""
        model = Film
        exclude = ["film_id"]
        load_instance = True
        include_fk = True
