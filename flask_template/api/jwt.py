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
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from flask_smorest import Api, abort
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
        optional: bool = False,
        refresh_token: bool = False,
    ) -> Callable[[Callable[..., RT]], Callable[..., RT]]:
        """Decorator validating jwt tokens and documenting them for openapi specification (only version 3...)."""
        if isinstance(security_scheme, str):
            security_scheme = {security_scheme: []}

        def decorator(func: Callable[..., RT]) -> Callable[..., RT]:

            # map to names that are less likely to have collisions with user defined arguments!
            _jwt_optional = optional
            _jwt_fresh = fresh
            _jwt_refresh_token = refresh_token

            @wraps(func)
            def wrapper(*args: Any, **kwargs) -> RT:
                try:
                    verify_jwt_in_request(
                        fresh=_jwt_fresh,
                        optional=_jwt_optional,
                        refresh=_jwt_refresh_token,
                    )
                except JWTExtendedException as exc:
                    # trap exception and emulate flask exception handling
                    # as flask only handles one exception per request
                    # but we want to raise a custom exception for jwt exceptions
                    return current_app.handle_user_exception(exc)
                return func(*args, **kwargs)

            # Store doc in wrapper function
            # The deepcopy avoids modifying the wrapped function doc
            wrapper._apidoc = deepcopy(getattr(func, "_apidoc", {}))
            security_schemes = wrapper._apidoc.setdefault("security", [])
            if _jwt_optional:
                # also add empty security scheme for optional jwt tokens
                security_schemes.append({})
            security_schemes.append(security_scheme)

            return wrapper

        return decorator

    def _prepare_security_doc(
        self,
        doc: Dict[str, Any],
        doc_info: Dict[str, Any],
        *,
        api: Api,
        app: Flask,
        spec: APISpec,
        method: str,
        **kwargs,
    ):
        """Actually prepare the documentation."""
        operation: Optional[List[Dict[str, List[Any]]]] = doc_info.get("security")
        if operation:
            available_schemas: Dict[str, Any] = (
                spec.to_dict().get("components").get("securitySchemes")
            )
            for scheme in operation:
                if not scheme:
                    continue  # encountered empty schema for optional security
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


@JWT.user_lookup_loader
def loadUserObject(jwt_header: dict, jwt_payload: dict):
    # load the actual user object from the user identity here
    identity: Optional[str] = jwt_payload.get("sub")
    if not identity:
        raise KeyError("Could not find user Identity!")
    return DemoUser(identity)


# JWT errors


@JWT.user_lookup_error_loader
def on_user_load_error(jwt_header: dict, jwt_payload: dict):
    identity: Optional[str] = jwt_payload.get("sub")
    abort(
        401,
        message=gettext(
            "The user with the id '%(userid)s' could not be loaded.", userid=identity
        ),
    )


@JWT.expired_token_loader
def on_expired_token(jwt_header: dict, jwt_payload: dict):
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
def on_stale_token(jwt_header: dict, jwt_payload: dict):
    abort(
        401,
        message=gettext(
            "Unauthorized to access this resource without a valid and fesh api token.\n"
            "Request a new fresh api token from the login resource."
        ),
    )


@JWT.revoked_token_loader
def on_revoked_token(jwt_header: dict, jwt_payload: dict):
    abort(401, message=gettext("Your authentication token has expired."))


def register_jwt(app: Flask):
    """Register jwt manager with flask app."""
    JWT.init_app(app)
