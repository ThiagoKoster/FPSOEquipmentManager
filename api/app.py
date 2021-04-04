from flask import Flask
from api.restx import restX_api
from api.db import config_db
from api.endpoints.vessel_controller import ns_vessel
from api.endpoints.equipment_controller import ns_equipment


def create_app(db_uri):
    app = Flask(__name__)
    app.config['RESTX_ERROR_404_HELP'] = False
    config_db(app, db_uri)

    restX_api.init_app(app)
    restX_api.add_namespace(ns_vessel)
    restX_api.add_namespace(ns_equipment)
    return app


def main():
    app = create_app('test.db')
    app.run()


if __name__ == '__main__':
    main()
