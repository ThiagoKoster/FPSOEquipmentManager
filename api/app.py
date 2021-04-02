from flask import Flask
from api.restx import api
from api.db import config_db
from api.endpoints.healthcheck import ns_healthcheck
from api.endpoints.vessel_controller import ns_vessel


def create_app(db_uri):
    app = Flask(__name__)

    config_db(app, db_uri)
    api.init_app(app)
    api.add_namespace(ns_healthcheck)
    api.add_namespace(ns_vessel)
    return app


def main():
    app = create_app('test.db')
    app.run()


if __name__ == '__main__':
    main()
