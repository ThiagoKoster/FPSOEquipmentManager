from flask_restx import Resource,Api
from api.restx import api

ns_healthcheck = api.namespace('healthcheck', description='Checks the status of the application')

@ns_healthcheck.route('/')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}