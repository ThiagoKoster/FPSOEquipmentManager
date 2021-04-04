from flask import Flask, Blueprint
from flask_restx import Api
from api.ma import ma
from api.db import db
from api.resources.vessel import ns_vessel
from api.resources.equipment import ns_equipment


def create_app(db_uri):
    app = Flask(__name__)
    blueprint = Blueprint('api', __name__, url_prefix='/api')
    restx_api = Api(blueprint, version='1,0',
                    doc='/doc',
                    title='FPSO Equipment Manager',
                    description='Backend to manage different equipment of an FPSO '
                                '(Floating Production, Storage and Offloading)')
    app.register_blueprint(blueprint)

    app.config['RESTX_ERROR_404_HELP'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_uri}'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    restx_api.add_namespace(ns_vessel)
    restx_api.add_namespace(ns_equipment)

    db.init_app(app)
    ma.init_app(app)
    db.create_all(app=app)
    return app


if __name__ == '__main__':
    app = create_app('FPSOEquipmentManager.db')

    app.run()
