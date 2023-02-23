"""Module to hold DB constant to avoid circular imports."""

from typing import Type, cast

from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_sqlalchemy.model import Model
from sqlalchemy.orm import DeclarativeBase, registry
from sqlalchemy.schema import MetaData


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
MODEL = cast(Type[DeclarativeBase], DB.Model)
if not issubclass(MODEL, Model):
    raise Warning(
        f"Please update the type cast of db.MODEL to reflect the current type {type(MODEL)}."
    )

# remove this if you do not use the `REGISTRY.mapped_as_dataclass` decorator
REGISTRY: registry = MODEL.registry

MIGRATE = Migrate()
