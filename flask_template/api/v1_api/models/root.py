"""Module containing all API schemas for the root API endpoint."""

import marshmallow as ma
from ...util import MaBaseSchema

__all__ = [
    "RootSchema",
]


class RootSchema(MaBaseSchema):
    auth = ma.fields.Url(required=True, allow_none=False, dump_only=True)
