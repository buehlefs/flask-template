from logging import Logger, getLogger
from flask import Flask


def get_logger(app: Flask, name: str) -> Logger:
    """Utitlity method to get a specific logger that is a child logger of the app.logger."""
    logger_name = f"{app.import_name}.{name}"
    return getLogger(logger_name)
