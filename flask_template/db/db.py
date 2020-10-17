"""Module to hold DB constant to avoid circular imports."""

from sqlalchemy.schema import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


DB: SQLAlchemy = SQLAlchemy(
    metadata=MetaData(
        naming_convention={
            "pk": "pk_%(table_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "ix": "ix_%(table_name)s_%(column_0_name)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(column_0_name)s",
        }
    )
)

# Model constant to be importable directly
MODEL = DB.Model

MIGRATE = Migrate()
