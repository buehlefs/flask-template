"""CLI functions for the db module."""

from typing import cast
from flask import Flask, Blueprint, current_app
from flask.cli import with_appcontext, AppGroup
import click

from ..util.logging import get_logger

from .db import DB

# make sure all models are imported for CLI to work properly
from . import models  # noqa


DB_CLI_BLP = Blueprint("db_cli", __name__, cli_group=None)
DB_CLI = cast(AppGroup, DB_CLI_BLP.cli)  # expose as attribute for autodoc generation

DB_COMMAND_LOGGER = "db"


@DB_CLI.command("create-db")
@with_appcontext
def create_db():
    """Create all db tables."""
    create_db_function(current_app)
    click.echo("Database created.")


def create_db_function(app: Flask):
    DB.create_all()
    get_logger(app, DB_COMMAND_LOGGER).info("Database created.")


@DB_CLI.command("drop-db")
@with_appcontext
def drop_db():
    """Drop all db tables."""
    drop_db_function(current_app)
    click.echo("Database dropped.")


def drop_db_function(app: Flask):
    DB.drop_all()
    get_logger(app, DB_COMMAND_LOGGER).info("Dropped Database.")


def register_cli_blueprint(app: Flask):
    """Method to register the DB CLI blueprint."""
    app.register_blueprint(DB_CLI_BLP)
    app.logger.info("Registered blueprint.")
