"""Module for creating app and db"""

from flask.cli import FlaskGroup

from app import app, db
from app import routes
from app.swagger import swaggerui_blueprint


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    """Creation of database"""
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    app.register_blueprint(swaggerui_blueprint)
    cli()
