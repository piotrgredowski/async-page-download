#!/usr/bin/env python3
from flask import Flask

from views import jobs


def register_blueprints(app):
    app.register_blueprint(jobs.blueprint, url_prefix="/api/jobs")


def make_app():
    app = Flask("Asyncpage")

    register_blueprints(app)

    return app


def main():
    app = make_app()
    app.run(host="0.0.0.0",
            port="8191",
            debug=True)


if __name__ == "__main__":
    main()
