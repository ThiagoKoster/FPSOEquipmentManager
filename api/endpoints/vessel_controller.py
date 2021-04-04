from flask_restx import Resource
from api.repositories.vessel_repository import VesselRepository
from api.restx import restX_api
from flask_restx import reqparse
from api.serializers.vessel_serializer import vessel_serializer
from api.business.vessel_business import VesselBus
from api.db import db
ns_vessel = restX_api.namespace('vessels', description='Endpoint for operations related to vessel object')


@ns_vessel.route('')
class VesselController(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super(VesselController, self).__init__(api, args, kwargs)
        self._vessel_repo = VesselRepository(db)
        self.bus = VesselBus(self._vessel_repo)
        self.parser = reqparse.RequestParser()
        self.parser.add_argument('code', required=True, type=str, help='Vessel Code cannot be blank.')

    @restX_api.expect(vessel_serializer)
    @restX_api.marshal_with(vessel_serializer, code=201)
    @restX_api.response(400, 'Bad request')
    @restX_api.response(409, 'Vessel Code already in use')
    def post(self):
        request = self.parser.parse_args()
        new_vessel = self.bus.add(request.code)
        return new_vessel, 201

    @restX_api.marshal_list_with(vessel_serializer)
    def get(self):
        return self.bus.get_vessels()


