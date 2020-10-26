"""
Module containing Debug Methods and sites.

This Module should only be loaded in debug Mode.
"""

from flask.app import Flask
from . import root  # noqa
from . import routes  # noqa


def register_debug_routes(app: Flask):
    """Register the debug routes blueprint with the flask app."""
    if not app.config["DEBUG"]:
        app.logger.warning("This Module should only be loaded if DEBUG mode is active!")
        raise Warning("This Module should only be loaded if DEBUG mode is active!")
    app.register_blueprint(root.DEBUG_BLP)
