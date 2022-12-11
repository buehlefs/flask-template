"""Module containing default config values."""
from os import urandom
from logging import WARNING, INFO

from .sqlalchemy_config import SQLAchemyProductionConfig, SQLAchemyDebugConfig
from .smorest_config import SmorestProductionConfig, SmorestDebugConfig


class ProductionConfig(SQLAchemyProductionConfig, SmorestProductionConfig):
    ENV = "production"
    SECRET_KEY = urandom(32)

    REVERSE_PROXY_COUNT = 0

    DEBUG = False
    TESTING = False

    JSON_SORT_KEYS = False
    JSONIFY_PRETTYPRINT_REGULAR = False

    LOG_CONFIG = None  # if set this is preferred

    DEFAULT_LOG_SEVERITY = WARNING
    DEFAULT_LOG_FORMAT_STYLE = "{"
    DEFAULT_LOG_FORMAT = "{asctime} [{levelname:^7}] [{module:<30}] {message}    <{funcName}, {lineno}; {pathname}>"
    DEFAULT_LOG_DATE_FORMAT = None


class DebugConfig(ProductionConfig, SQLAchemyDebugConfig, SmorestDebugConfig):
    ENV = "development"
    DEBUG = True
    SECRET_KEY = "debug_secret"  # FIXME make sure this NEVER! gets used in production!!!

    DEFAULT_LOG_SEVERITY = INFO
