"""Module containing the authentication API of the v1 API."""

from .models.auth import AccessTokenSchema, UserSchema
from typing import Dict
from flask.helpers import url_for
from flask.views import MethodView
from dataclasses import dataclass
from http import HTTPStatus
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    current_user,
)

from .root import API_V1
from .models import AuthRootSchema, LoginPostSchema, LoginTokensSchema
from ..jwt import DemoUser


@dataclass
class AuthRootData:
    login: str
    refresh: str
    whoami: str


@dataclass
class LoginTokensData:
    access_token: str
    refresh_token: str


@dataclass
class RefreshedTokenData:
    access_token: str


@API_V1.route("/auth/")
class AuthRootView(MethodView):
    """Root endpoint for all authentication resources."""

    @API_V1.response(HTTPStatus.OK, AuthRootSchema())
    def get(self):
        """Get the urls for the authentication api."""
        return AuthRootData(
            login=url_for("api-v1.LoginView", _external=True),
            refresh=url_for("api-v1.RefreshView", _external=True),
            whoami=url_for("api-v1.WhoamiView", _external=True),
        )


@API_V1.route("/auth/login/")
class LoginView(MethodView):
    """Login endpoint to retrieve api tokens."""

    @API_V1.arguments(
        LoginPostSchema(),
        location="json",
        description="The login credentials of the user.",
    )
    @API_V1.response(HTTPStatus.OK, LoginTokensSchema())
    def post(self, credentials: Dict[str, str]):
        """Login with the user credentials to receive a access and refresh token pair.

        The access token can be used for all authorized api endpoints.
        The refresh token can only be used with the refresh endpoint to get a new access token.
        """
        identity = DemoUser(credentials.get("username", "guest"))
        return LoginTokensData(
            access_token=create_access_token(identity=identity),
            refresh_token=create_refresh_token(identity=identity),
        )


@API_V1.route("/auth/refresh/")
class RefreshView(MethodView):
    """Refresh endpoint to retrieve new api access tokens."""

    @API_V1.response(HTTPStatus.OK, AccessTokenSchema())
    @API_V1.require_jwt("jwt-refresh-token", refresh_token=True)
    def post(self, credentials: Dict[str, str]):
        """Get a new access token.

        This method requires the jwt refresh token!
        """
        identity = current_user
        return RefreshedTokenData(
            access_token=create_access_token(identity=identity, fresh=True),
        )


@API_V1.route("/auth/whoami/")
class WhoamiView(MethodView):
    """Whoami endpoint to test the api token and get the current user info."""

    @API_V1.response(HTTPStatus.OK, UserSchema())
    @API_V1.require_jwt("jwt", optional=True)
    def get(self):
        """Get the user object of the current user."""
        return current_user
