#!/usr/bin/env python3
from flask import Flask

from views import jobs
from lib import Config


def register_blueprints(app):
    app.register_blueprint(jobs.blueprint, url_prefix="/api/jobs")


def make_app():
    app = Flask("Asyncpage")
    app.cfg = Config()
    app.cfg.load_from_yaml("config.yml")

    register_blueprints(app)

    return app


def main():
    app = make_app()
    app.run(host=app.cfg.get("app.server.host"),
            port=app.cfg.get("app.server.port"),
            debug=True)


if __name__ == "__main__":
    main()
