"""Module containing the root endpoint of the v1 API."""

from dataclasses import dataclass
from flask.helpers import url_for
from flask.views import MethodView
from http import HTTPStatus
from ..util import SecurityBlueprint as SmorestBlueprint
from .models import RootSchema


API_V1 = SmorestBlueprint(
    "api-v1", "API v1", description="Version 1 of the API.", url_prefix="/api/v1"
)


@dataclass()
class RootData:
    auth: str


@API_V1.route("/")
class RootView(MethodView):
    """Root endpoint of the v1 api."""

    @API_V1.response(HTTPStatus.OK, RootSchema())
    def get(self):
        """Get the urls of the next endpoints of the v1 api to call."""
        return RootData(auth=url_for("api-v1.AuthRootView", _external=True))
