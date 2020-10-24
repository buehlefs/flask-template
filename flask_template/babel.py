"""Module for setting up Babel support for flask app."""

from typing import Optional
from flask import Flask, request
from flask_babel import Babel, refresh as flask_babel_refresh
from werkzeug.datastructures import LanguageAccept


SUPPORTED_LOCALES = ["de", "en"]

BABEL = Babel()


@BABEL.localeselector
def get_locale():
    # try to guess the language from the user accept
    # header the browser transmits. We support de/en. The best match wins.
    return request.accept_languages.best_match(SUPPORTED_LOCALES)


def inject_lang_from_header():
    """Inject the language defined in the custom 'lang' Hader into the accepted
    languages of the request if present.

    This method can be used in a before request callback to read the custom
    header and use that to inject tha language into the request.
    """
    lang: Optional[str] = request.headers.get("lang")
    if lang:
        # inject language from custom header as first choice into request
        values = (lang, 10), *request.accept_languages
        request.accept_languages = LanguageAccept(values)
        # Force refresh to make sure that the change is applied
        flask_babel_refresh()


def register_babel_with_app(app: Flask):
    """Register babel to enable translations for this app."""
    BABEL.init_app(app)
