from flask import Blueprint, Flask, render_template

LICENSE_BLP = Blueprint("licenses", __name__, url_prefix="/licenses")


@LICENSE_BLP.route("/")
def show_licenses():
    """Route for displaying licenses of dependencies."""
    return render_template("included_licenses.html")


def register_licenses(app: Flask):
    app.register_blueprint(LICENSE_BLP)
