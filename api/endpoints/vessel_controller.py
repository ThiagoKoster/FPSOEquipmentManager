from flask_restx import Resource
from api.restx import api
from flask_restx import reqparse
from werkzeug.exceptions import Conflict
from api.serializers.vessel_serializer import vessel_serializer
from api.business.vessel import VesselBus

ns_vessel = api.namespace('vessel', description='Endpoint for operations related to vessel object')


@ns_vessel.route('/')
class VesselController(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super(VesselController, self).__init__(api, args, kwargs)
        self.bus = VesselBus()
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('code', required=True, type=str, help='Vessel Code cannot be blank.')

    @api.expect(vessel_serializer)
    @api.marshal_with(vessel_serializer, code=201)
    @api.response(400, 'Bad request')
    @api.response(409, 'Vessel Code already in use')
    def post(self):
        request = self.parser.parse_args()
        new_vessel = self.bus.add(request.code)

        if new_vessel is None:
            raise Conflict("Vessel Code already exists in database")
        return new_vessel, 201
