"""Digital Eye REST API."""

import logging

from flask import Flask
from flask_cors import CORS

import config
from database.init_db import init_db


def create_app() -> Flask:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)-7s %(name)s: %(message)s",
    )

    app = Flask(__name__)
    CORS(app)

    init_db()
    config.TELEMETRY_LOG_DIR.mkdir(parents=True, exist_ok=True)

    from api.routes import analytics, dashboard, hosts, incidents, telemetry

    for module in (telemetry, hosts, incidents, dashboard, analytics):
        app.register_blueprint(module.bp)

    return app
