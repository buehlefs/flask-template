"""Root module containing the flask app factory."""

from os import environ, makedirs
from pathlib import Path
from typing import Any, Dict, Optional, cast
from logging import Logger, Formatter, Handler, WARNING, getLogger
from logging.config import dictConfig

from flask.app import Flask
from flask.config import Config
from flask.cli import FlaskGroup
from flask.logging import default_handler
from flask_cors import CORS

from json import load as load_json
from toml import load as load_toml

import click

from .util.config import ProductionConfig, DebugConfig
from . import babel
from . import db
from . import api
from .api import jwt


# change this to change tha flask app name and the config env var prefix
# must not contain any spaces!
APP_NAME = __name__
CONFIG_ENV_VAR_PREFIX = APP_NAME.upper().replace("-", "_").replace(" ", "_")


def create_app(test_config: Optional[Dict[str, Any]] = None):
    """Flask app factory."""
    # create and configure the app
    app = Flask(APP_NAME, instance_relative_config=True)

    # Start Loading config #################

    # load defaults
    config = cast(Config, app.config)
    flask_env = cast(Optional[str], config.get("ENV"))
    if flask_env == "production":
        config.from_object(ProductionConfig)
    elif flask_env == "development":
        config.from_object(DebugConfig)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        config.from_pyfile("config.py", silent=True)
        # also try to load json config
        config.from_file("config.json", load=load_json, silent=True)
        # also try to load toml config
        config.from_file("config.toml", load=load_toml, silent=True)
        # load config from file specified in env var
        config.from_envvar(f"{CONFIG_ENV_VAR_PREFIX}_SETTINGS", silent=True)
        # TODO load some config keys directly from env vars
    else:
        # load the test config if passed in
        config.from_mapping(test_config)

    # End Loading config #################

    # Configure logging
    log_config = cast(Optional[Dict[Any, Any]], config.get("LOG_CONFIG"))
    if log_config:
        # Apply full log config from dict
        dictConfig(log_config)
    else:
        # Apply smal log config to default handler
        log_severity = max(0, config.get("DEFAULT_LOG_SEVERITY", WARNING))
        # use percent for backwards compatibility in case of errors
        log_format_style = cast(str, config.get("DEFAULT_LOG_FORMAT_STYLE", "%"))
        log_format = cast(Optional[str], config.get("DEFAULT_LOG_FORMAT"))
        date_format = cast(Optional[str], config.get("DEFAULT_LOG_DATE_FORMAT"))
        if log_format:
            formatter = Formatter(log_format, style=log_format_style, datefmt=date_format)
            default_logging_handler = cast(Handler, default_handler)
            default_logging_handler.setFormatter(formatter)
            default_logging_handler.setLevel(log_severity)
            root = getLogger()
            root.addHandler(default_logging_handler)
            app.logger.removeHandler(default_logging_handler)

    logger: Logger = app.logger
    logger.info(
        f"Configuration loaded. Possible config locations are: 'config.py', 'config.json', Environment: '{CONFIG_ENV_VAR_PREFIX}_SETTINGS'"
    )

    if config.get("SECRET_KEY") == "debug_secret":
        logger.error(
            'The configured SECRET_KEY="debug_secret" is unsafe and must not be used in production!'
        )

    # ensure the instance folder exists
    try:
        makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Begin loading extensions and routes

    babel.register_babel(app)

    db.register_db(app)

    jwt.register_jwt(app)
    api.register_root_api(app)

    # allow cors requests everywhere (CONFIGURE THIS TO YOUR PROJECTS NEEDS!)
    CORS(app)

    if config.get("DEBUG", False):
        # Register debug routes when in debug mode
        from .util.debug_routes import register_debug_routes

        register_debug_routes(app)

    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """Cli entry point for autodoc tooling."""
    pass
