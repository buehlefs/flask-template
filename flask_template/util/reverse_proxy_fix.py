from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix


def apply_reverse_proxy_fix(app: Flask):
    """Apply the reverse proxy fix from werkzeug with the number configured in REVERSE_PROXY_COUNT."""
    r_p_count = app.config.get("REVERSE_PROXY_COUNT", 0)
    if r_p_count > 0:
        app.wsgi_app = ProxyFix(
            app.wsgi_app,
            x_for=r_p_count,
            x_host=r_p_count,
            x_port=r_p_count,
            x_prefix=r_p_count,
            x_proto=r_p_count,
        )
