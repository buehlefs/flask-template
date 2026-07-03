"""Module for the root endpoint of the debug routes.
Contains the blueprint to avoid circular dependencies."""

from flask import Blueprint, render_template

DEBUG_BLP = Blueprint(
    "debug-routes", __name__, template_folder="templates", url_prefix="/debug"
)


@DEBUG_BLP.route("/")
@DEBUG_BLP.route("/index")
def index():
    return render_template("debug/index.html", title="Flask Template – Debug")
