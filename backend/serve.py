#!/usr/bin/env python3
from flask import Flask

from views import jobs
from utils import Config
from jobs_queue import queue


def register_blueprints(app):
    app.register_blueprint(jobs.blueprint, url_prefix="/api/jobs")


def make_app(cfg_path):
    app = Flask("AsyncPage")
    app.cfg = Config()
    app.cfg.load_from_yaml(cfg_path)

    # Assign queue to app
    app.queue = queue

    register_blueprints(app)

    return app


def main():
    app = make_app("config.yml")
    app.run(host=app.cfg.get("app.server.host"),
            port=app.cfg.get("app.server.port"),
            debug=app.cfg.get("app.server.debug"))


if __name__ == "__main__":
    main()
