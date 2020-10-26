"""Module containing JWT security features for the API."""

from copy import deepcopy
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, TypeVar, Union
from apispec.core import APISpec
from apispec.utils import deepupdate
from flask.app import Flask
from flask.globals import current_app
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_jwt_extended.view_decorators import (
    verify_jwt_in_request,
    verify_fresh_jwt_in_request,
    verify_jwt_refresh_token_in_request,
)
from flask_smorest import abort
from flask_babel import gettext
from warnings import warn
from functools import wraps

JWT = JWTManager()

"""Basic JWT security scheme."""
JWT_SCHEME = {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "The jwt access token as returned by login or refresh.",
}

"""JWT security scheme for JWT refresh tokens."""
JWT_REFRESH_SCHEME = {
    "type": "http",
    "scheme": "bearer",
    "bearerFormat": "JWT",
    "description": "The jwt refresh token as returned by login. Must only be used to get a new access token.",
}

"""Security schemes to be added to the swagger.json api documentation."""
SECURITY_SCHEMES = {
    "jwt": JWT_SCHEME,
    "jwt-refresh-token": JWT_REFRESH_SCHEME,
}


RT = TypeVar("RT")


class JWTMixin:
    """Extend Blueprint to add security documentation and jwt handling"""

    def require_jwt(
        self,
        security_scheme: Union[str, Dict[str, List[Any]]],
        *,
        fresh: bool = False,
        refresh_token: bool = False,
    ) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
        """Decorator validating jwt tokens and documenting them for openapi specification (only version 3...)."""
        if isinstance(security_scheme, str):
            security_scheme = {security_scheme: []}

        def decorator(func: Callable[..., RT]) -> Callable[..., RT]:

            verify: Callable[..., None]
            if refresh_token:
                verify = verify_jwt_refresh_token_in_request
            else:
                if fresh:
                    verify = verify_fresh_jwt_in_request
                else:
                    verify = verify_jwt_in_request

            @wraps(func)
            def wrapper(*args: Any, **kwargs) -> RT:
                try:
                    verify()
                except JWTExtendedException as exc:
                    # trap exception and emulate flask exception handling
                    # as flask only handles one exception per request
                    # but we want to raise a custom exception for jwt exceptions
                    current_app.handle_user_exception(exc)
                return func(*args, **kwargs)

            # Store doc in wrapper function
            # The deepcopy avoids modifying the wrapped function doc
            wrapper._apidoc = deepcopy(getattr(func, "_apidoc", {}))
            wrapper._apidoc.setdefault("security", []).append(security_scheme)

            return wrapper

        return decorator

    def _prepare_security_doc(
        self, doc: Dict[str, Any], doc_info: Dict[str, Any], *, spec: APISpec, **kwargs
    ):
        """Actually prepare the documentation."""
        operation: Optional[List[Dict[str, List[Any]]]] = doc_info.get("security")
        if operation:
            available_schemas: Dict[str, Any] = (
                spec.to_dict().get("components").get("securitySchemes")
            )
            for scheme in operation:
                schema_name = next(iter(scheme.keys()))
                if schema_name not in available_schemas:
                    warn(
                        f"The schema '{scheme}' is not specified in the available securitySchemes."
                    )
            doc = deepupdate(doc, {"security": operation})
        return doc


# JWT identity and claims


@dataclass
class DemoUser:
    """This class **should** be replaced by the actual user class!"""

    username: str


@JWT.user_identity_loader
def load_user_identity(user: DemoUser):
    # load the user identity (primary key) fromthe user object here
    return user.username


@JWT.user_loader_callback_loader
def loadUserObject(identity: str):
    # load the actual user object from the user identity here
    return DemoUser(identity)


# JWT errors


@JWT.user_loader_error_loader
def on_user_load_error(identity: str):
    abort(
        401,
        message=gettext(
            "The user with the id '%(userid)s' could not be loaded.", userid=identity
        ),
    )


@JWT.expired_token_loader
def on_expired_token(expired_token):
    abort(401, message=gettext("Your authentication token has expired."))


@JWT.invalid_token_loader
def on_invalid_token(message: str):
    abort(401, message=gettext("Your authentication token is invalid."))


@JWT.unauthorized_loader
def on_unauthorized(message: str):
    abort(
        401,
        message=gettext(
            "Unauthorized to access this resource without a valid api token."
        ),
    )


@JWT.needs_fresh_token_loader
def on_stale_token():
    abort(
        401,
        message=gettext(
            "Unauthorized to access this resource without a valid and fesh api token.\n"
            "Request a new fresh api token from the login resource."
        ),
    )


@JWT.revoked_token_loader
def on_revoked_token():
    abort(401, message=gettext("Your authentication token has expired."))


def register_jwt(app: Flask):
    """Register jwt manager with flask app."""
    JWT.init_app(app)
