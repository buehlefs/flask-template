"""Module containing utilities for flask smorest APIs."""
from typing import Any
from .jwt import JWTMixin
from flask_smorest import Blueprint
import marshmallow as ma


class SecurityBlueprint(Blueprint, JWTMixin):
    """Blueprint that is aware of jwt tokens and how to document them.

    Use this Blueprint if you want to document security requirements for your api.
    """

    def __init__(self, *args: Any, **kwargs):
        super().__init__(*args, **kwargs)
        self._prepare_doc_cbks.append(self._prepare_security_doc)


def camelcase(s: str) -> str:
    """Turn a string from python snake_case into camelCase."""
    parts = iter(s.split("_"))
    return next(parts) + "".join(i.title() for i in parts)


class MaBaseSchema(ma.Schema):
    """Base schema that automatically changes python snake case to camelCase in json."""

    # Uncomment to get ordered output
    # class Meta:
    #    ordered: bool = True

    def on_bind_field(self, field_name: str, field_obj: ma.fields.Field):
        field_obj.data_key = camelcase(field_obj.data_key or field_name)
