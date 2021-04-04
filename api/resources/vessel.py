from flask import request
from flask_restx import Resource, Namespace, fields
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest
from api.repositories.vessel_repository import VesselRepository
from api.resources.equipment import equipment_serializer
from api.schema.vessel import VesselSchema
from api.blls.vessel import VesselBus
from api.db import db

ns_vessel = Namespace('vessels', description='Endpoint for operations related to vessel object')

# Model required by flask_restx for expect
vessel = ns_vessel.model('Vessel', {
    'id': fields.Integer(readonly=True),
    'code': fields.String(required=True, description='The vessel\'s code'),
    'equipments': fields.List(fields.Nested(equipment_serializer), readonly=True)
})


@ns_vessel.route('')
class VesselResource(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super(VesselResource, self).__init__(api, args, kwargs)
        self._vessel_repo = VesselRepository(db)
        self.bus = VesselBus(self._vessel_repo)
        self.schema = VesselSchema()

    @ns_vessel.expect(vessel)
    @ns_vessel.marshal_with(vessel, code=201)
    @ns_vessel.response(400, 'Bad request')
    @ns_vessel.response(409, 'Vessel Code already in use')
    def post(self):
        vessel_req = self._validate_post_request(request.data)
        new_vessel = self.bus.add(vessel_req['code'])
        return new_vessel, 201

    @ns_vessel.marshal_list_with(vessel)
    def get(self):
        return self.bus.get_vessels()

    def _validate_post_request(self, data):
        try:
            return self.schema.loads(data)
        except ValidationError as e:
            raise BadRequest(e.messages)


