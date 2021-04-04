from flask import request
from flask_restx import Resource, Namespace, fields
from marshmallow import ValidationError
from werkzeug.exceptions import BadRequest
from http import HTTPStatus
from api.models.equipment import Status
from api.repositories.equipment import EquipmentRepository
from api.repositories.vessel import VesselRepository
from api.schema.equipment import EquipmentSchema
from api.schema.inactivate_equipments import InactivateEquipmentSchema
from api.blls.equipment import EquipmentBus
from api.db import db


ns_equipment = Namespace('vessels')

# Model required by flask_restx for expect
equipment_serializer = ns_equipment.model('Equipment', {
    'id': fields.Integer(readonly=True),
    'name': fields.String(required=True, description='The equipment\'s name'),
    'code': fields.String(required=True, description='The equipment\'s code'),
    'location': fields.String(required=True, description='The equipment\'s location'),
    'status': fields.String(readonly=True, description=' The equipment\'s status',
                            enum=[x.name for x in Status], attribute='status.name')
})
# Model required by flask_restx for expect
inactivate_equipment_serializer = ns_equipment.model('InactivateEquipment', {
    'code': fields.String(required=True, description='The equipment\'s code'),
})


@ns_equipment.route('/<vessel_id>/equipments')
class EquipmentResource(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super(EquipmentResource, self).__init__(api, args, kwargs)
        self._vessel_repo = VesselRepository(db)
        self._equipment_repo = EquipmentRepository(db)
        self.bus = EquipmentBus(self._vessel_repo, self._equipment_repo)
        self.inactivate_schema = InactivateEquipmentSchema()
        self.equipment_schema = EquipmentSchema(many=True, partial=('status',))

    @ns_equipment.expect([equipment_serializer])
    @ns_equipment.marshal_list_with(equipment_serializer, code=201)
    @ns_equipment.response(400, 'Bad request')
    @ns_equipment.response(404, 'Vessel not found')
    @ns_equipment.response(409, 'Equipment code already in use')
    def post(self, vessel_id):
        """Registers new equipment for the vessel"""
        parse_result = self._validate_post_request(request.data)
        new_equipment = self.bus.add_equipment(vessel_id, parse_result)

        return new_equipment, HTTPStatus.CREATED

    @ns_equipment.marshal_list_with(equipment_serializer, code=200)
    @ns_equipment.doc(params={'status': 'Equipment status'})
    @ns_equipment.response(404, 'Vessel not found')
    def get(self,  vessel_id):
        """Get all equipments of the vessel, can be filtered by status."""
        status = request.args.get('status', None)
        equipments = self.bus.get_vessel_equipments(vessel_id, status)
        return equipments, HTTPStatus.OK

    @ns_equipment.expect([inactivate_equipment_serializer])
    @ns_equipment.response(400, 'Bad request')
    @ns_equipment.response(404, 'Vessel not found')
    @ns_equipment.response(204, 'Equipments deactivated successfully')
    def patch(self, vessel_id):
        """Inactivate equipments of the vessel"""
        request_objects = self._validate_patch_request(request.data)
        self.bus.inactivate_equipments(vessel_id, [obj['code'] for obj in request_objects])
        return '', HTTPStatus.NO_CONTENT

    def _validate_post_request(self, data):
        try:
            return self.equipment_schema.loads(data)
        except ValidationError as e:
            raise BadRequest(e.messages)

    def _validate_patch_request(self, data):
        try:
            return self.inactivate_schema.loads(data, many=True)
        except ValidationError as e:
            raise BadRequest(e.messages)




