"""Module containing all API schemas for the authentication API."""

import marshmallow as ma
from ...util import MaBaseSchema

__all__ = [
    "AuthRootSchema",
    "LoginPostSchema",
    "LoginTokensSchema",
    "AccessTokenSchema",
    "UserSchema",
]


class AuthRootSchema(MaBaseSchema):
    login = ma.fields.Url(required=True, allow_none=False, dump_only=True)
    refresh = ma.fields.Url(required=True, allow_none=False, dump_only=True)
    whoami = ma.fields.Url(required=True, allow_none=False, dump_only=True)


class LoginPostSchema(MaBaseSchema):
    username = ma.fields.String(required=True, allow_none=False)
    password = ma.fields.String(required=True, allow_none=False, load_only=True)


class LoginTokensSchema(MaBaseSchema):
    access_token = ma.fields.String(required=True, allow_none=False, dump_only=True)
    refresh_token = ma.fields.String(required=True, allow_none=False, dump_only=True)


class AccessTokenSchema(MaBaseSchema):
    access_token = ma.fields.String(required=True, allow_none=False, dump_only=True)


class UserSchema(MaBaseSchema):
    username = ma.fields.String(required=True, allow_none=False)
