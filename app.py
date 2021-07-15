from flask.cli import FlaskGroup

from app import app, db


cli = FlaskGroup(app)

# from app import routes


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    cli()