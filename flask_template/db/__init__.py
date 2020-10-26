"""Module containing database cli and models."""

from flask import Flask
from sqlalchemy import event
from sqlalchemy.engine import Engine

from .db import DB, MIGRATE
from .cli import register_cli_blueprint


def register_db(app: Flask):
    """Register the sqlalchemy db and alembic migrations with the flask app."""
    if not app.config.get("SQLALCHEMY_DATABASE_URI"):
        app.config[
            "SQLALCHEMY_DATABASE_URI"
        ] = f"sqlite:///{app.instance_path}/{app.import_name}.db"

    DB.init_app(app)
    app.logger.info(f'Connected to db "{app.config["SQLALCHEMY_DATABASE_URI"]}".')

    register_cli_blueprint(app)

    MIGRATE.init_app(app, DB)

    # Apply additional config for Sqlite databases
    if app.config.get("SQLALCHEMY_DATABASE_URI", "").startswith("sqlite://"):

        @event.listens_for(Engine, "connect")
        def set_sqlite_pragma(dbapi_connection, connection_record):
            if app.config.get("SQLITE_FOREIGN_KEYS", True):
                cursor = dbapi_connection.cursor()
                cursor.execute("PRAGMA foreign_keys=ON")
                cursor.close()
