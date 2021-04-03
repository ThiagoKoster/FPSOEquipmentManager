from flask_restx import Resource, reqparse
from flask import request

from api.repositories.equipment_repository import EquipmentRepository
from api.repositories.vessel_repository import VesselRepository
from api.restx import restX_api
from api.serializers.equipment_serializer import equipment_serializer
from api.serializers.inactivate_equipments_serializer import inactivate_equipment_serializer, InactivateEquipmentSchema
from api.business.equipment_business import EquipmentBus
from api.db import db
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest
from http import HTTPStatus

ns_equipment = restX_api.namespace('vessels')


@ns_equipment.route('/<vessel_id>/equipments')
class VesselEquipmentController(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super(VesselEquipmentController, self).__init__(api, args, kwargs)
        self._vessel_repo = VesselRepository(db)
        self._equipment_repo = EquipmentRepository(db)
        self.bus = EquipmentBus(self._vessel_repo, self._equipment_repo)

        self.post_parser = reqparse.RequestParser()
        self.post_parser.add_argument('name', required=True, type=str, help='Equipment Name cannot be blank.')
        self.post_parser.add_argument('code', required=True, type=str, help='Equipment Code cannot be blank.')
        self.post_parser.add_argument('location', required=True, type=str, help='Equipment Location cannot be blank.')

        self.put_parser = reqparse.RequestParser()
        self.put_parser.add_argument('code', required=True, type=list,
                                     help='Equipment Code cannot be blank.', location='json')

    @restX_api.expect(equipment_serializer)
    @restX_api.marshal_with(equipment_serializer, code=201)
    @restX_api.response(400, 'Bad request')
    @restX_api.response(404, 'Vessel not found')
    @restX_api.response(409, 'Equipment code already in use')
    def post(self, vessel_id):
        parse_result = self.post_parser.parse_args()
        new_equipment = self.bus.add_equipment(vessel_id, parse_result)

        return new_equipment, HTTPStatus.CREATED

    @restX_api.marshal_list_with(equipment_serializer, code=200)
    @restX_api.doc(params={'status': 'Equipment status'})
    @restX_api.response(404, 'Vessel not found')
    def get(self,  vessel_id):
        status = request.args.get('status', None)
        equipments = self.bus.get_vessel_equipments(vessel_id, status)
        return equipments, HTTPStatus.OK

    @restX_api.expect([inactivate_equipment_serializer])
    @restX_api.response(400, 'Bad request')
    @restX_api.response(204, 'Equipments deactivated successfully')
    def patch(self, vessel_id):
        request_objects = self._validate_request(request.data)
        self.bus.inactivate_equipments(vessel_id, [obj['code'] for obj in request_objects])
        return '', HTTPStatus.NO_CONTENT

    @staticmethod
    def _validate_request(data):
        try:
            return InactivateEquipmentSchema(many=True).loads(data)
        except ValidationError as e:
            raise BadRequest(e.messages)




