from flask_restx import Resource
from api.restx import api
from api.db import db

ns_healthcheck = api.namespace('healthcheck', description='Checks the status of the application')

@ns_healthcheck.route('/')
class HelloWorld(Resource):
    def get(self):
        return {'dbStatus': self.check_db()}

    def check_db(self):
        try:
            db.session.execute('SELECT 1')
            return True
        except Exception as e:
            return False


