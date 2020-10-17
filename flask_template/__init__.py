from os import environ, path, makedirs
from pathlib import Path
from secrets import token_urlsafe
from typing import Any, Dict, Optional
from logging import Logger, Formatter, WARNING, getLogger
from logging.config import dictConfig

from flask import Flask
from flask.logging import default_handler

from .util.config import ProductionConfig, DebugConfig
from . import db


def create_app(test_config: Optional[Dict[str, Any]] = None):
    """Flask app factory."""
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    # Start Loading config #################

    # load defaults
    flask_env = app.config.get("ENV")
    if flask_env == "production":
        app.config.from_object(ProductionConfig)
    elif flask_env == "development":
        app.config.from_object(DebugConfig)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
        # also try to load json config
        app.config.from_json("config.json", silent=True)
        # load config from file specified in env var
        app.config.from_envvar(f"{__name__}_SETTINGS", silent=True)
        # TODO load some config keys directly from env vars
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # End Loading config #################

    # Configure logging
    log_config: Optional[Dict] = app.config.get("LOG_CONFIG")
    if log_config:
        # Apply full log config from dict
        dictConfig(log_config)
    else:
        # Apply smal log config to default handler
        log_severity = max(0, app.config.get("DEFAULT_LOG_SEVERITY", WARNING))
        log_format_style = app.config.get(
            "DEFAULT_LOG_FORMAT_STYLE", "%"
        )  # use percent for backwards compatibility in case of errors
        log_format = app.config.get("DEFAULT_LOG_FORMAT")
        date_format = app.config.get("DEFAULT_LOG_DATE_FORMAT")
        if log_format:
            formatter = Formatter(log_format, style=log_format_style, datefmt=date_format)
            default_handler.setFormatter(formatter)
            default_handler.setLevel(log_severity)
            root = getLogger()
            root.addHandler(default_handler)
            app.logger.removeHandler(default_handler)

    logger: Logger = app.logger
    logger.info("Configuration loaded.")

    if app.config.get("SECRET_KEY") == "debug_secret":
        logger.error(
            'The configured SECRET_KEY="debug_secret" is unsafe and must not be used in production!'
        )

    # ensure the instance folder exists
    try:
        makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass

    # Begin loading extensions and routes

    db.register_db_in_app(app)

    return app
