"""Module containing debug routes index page."""

from flask import render_template, current_app
from .root import DEBUG_BLP



@DEBUG_BLP.route("/routes")
def routes():
    """Render all registered routes."""
    output = []
    for rule in current_app.url_map.iter_rules():

        line = {
            "endpoint": rule.endpoint,
            "methods": ", ".join(rule.methods),
            "url": rule.rule,
        }
        output.append(line)
    output.sort(key=lambda x: x["url"])
    return render_template(
        "debug/routes/all.html", title="Flask Template – Routes", routes=output
    )
