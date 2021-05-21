"""Module to hold DB constant to avoid circular imports."""

from typing import Type, cast
from flask_sqlalchemy.model import DefaultMeta, Model
from sqlalchemy.schema import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm.decl_api import registry


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
MODEL = cast(Type[Model], DB.Model)
if type(MODEL) is not DefaultMeta or not issubclass(MODEL, Model):
    raise Warning(
        f"Please update the type cast of db.MODEL to reflect the current type {type(MODEL)}."
    )

# only for sqlalchemy 1.4!
REGISTRY = cast(registry, MODEL.registry)

MIGRATE = Migrate()
