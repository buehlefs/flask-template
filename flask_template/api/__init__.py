"""Module containing all API related code of the project."""

from typing import Dict
from flask import Flask
from flask.helpers import url_for
from flask.views import MethodView
import marshmallow as ma
from flask_smorest import Api, Blueprint as SmorestBlueprint
from http import HTTPStatus
from .util import MaBaseSchema
from .v1_api import API_V1
from .jwt import SECURITY_SCHEMES

"""A single API instance. All api versions should be blueprints."""
ROOT_API = Api(spec_kwargs={"title": "API Root", "version": "v1"})


class VersionsRootSchema(MaBaseSchema):
    title = ma.fields.String(required=True, allow_none=False, dump_only=True)
    v1 = ma.fields.Url(required=True, allow_none=False, dump_only=True)


ROOT_ENDPOINT = SmorestBlueprint(
    "api-root",
    "root",
    url_prefix="/api",
    description="The API endpoint pointing towards all api versions.",
)


@ROOT_ENDPOINT.route("/")
class RootView(MethodView):
    @ROOT_ENDPOINT.response(HTTPStatus.OK, VersionsRootSchema())
    def get(self) -> Dict[str, str]:
        """Get the Root API information containing the links to all versions of this api."""
        return {
            "title": ROOT_API.spec.title,
            "v1": url_for("api-v1.RootView", _external=True),
        }


def register_root_api(app: Flask):
    """Register the API with the flask app."""
    ROOT_API.init_app(app)

    # register security schemes in doc
    for name, scheme in SECURITY_SCHEMES.items():
        ROOT_API.spec.components.security_scheme(name, scheme)

    # register API blueprints (only do this after the API is registered with flask!)
    ROOT_API.register_blueprint(ROOT_ENDPOINT)
    ROOT_API.register_blueprint(API_V1)
